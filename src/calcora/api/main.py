from __future__ import annotations

import importlib.resources
import os
import sys
from pathlib import Path

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import Response
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
except Exception as e:  # noqa: BLE001
    raise RuntimeError(
        "FastAPI is not installed. Install with: pip install 'calcora[api]'"
    ) from e

from ..bootstrap import default_engine
from ..renderers.json_renderer import JsonRenderer


class MatrixRequest(BaseModel):
    matrix: str
    format: str = "json"
    verbosity: str = "detailed"


class MatrixMultiplyRequest(BaseModel):
    matrix_a: str
    matrix_b: str
    format: str = "json"
    verbosity: str = "detailed"


app = FastAPI(title="Calcora API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://calcoralive.netlify.app",
        "http://localhost:5173",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "*"  # Allow all origins for demo purposes
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _web_path(name: str):
    """Get path to web resources, works both in development and PyInstaller bundle."""
    # Check if running in PyInstaller bundle
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running in PyInstaller bundle
        base_path = Path(sys._MEIPASS) / "calcora" / "web"
        if name == ".":
            return base_path
        return base_path / name
    else:
        # Running in normal Python environment
        return importlib.resources.files("calcora.web").joinpath(name)


app.mount(
    "/static",
    StaticFiles(directory=str(_web_path("."))),
    name="static",
)


@app.get("/")
def ui():
    web_file = _web_path("index.html")
    if isinstance(web_file, Path):
        content = web_file.read_text(encoding="utf-8")
    else:
        content = web_file.read_text(encoding="utf-8")
    return Response(content=content, media_type="text/html")


@app.get("/health")
def health():
    return {"status": "ok"}


# Unified compute endpoint for frontend
@app.post("/api/compute")
def compute(request: dict):
    """Unified compute endpoint that handles all operations.
    
    Accepts JSON body with:
    - operation: 'differentiate', 'matrix_multiply', 'matrix_determinant', etc.
    - expression: the expression or matrix
    - variable: (for differentiate) variable to differentiate
    - verbosity: 'concise', 'detailed', or 'teacher'
    - matrix_b: (for multiply) second matrix
    """
    operation = request.get("operation")
    expression = request.get("expression", "")
    variable = request.get("variable", "x")
    verbosity = request.get("verbosity", "detailed")
    matrix_b = request.get("matrix_b")
    
    if not operation:
        return {"error": "Missing 'operation' parameter"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        if operation == "differentiate":
            result = engine.run(operation="differentiate", expression=expression, variable=variable)
        elif operation.startswith("matrix_"):
            if operation == "matrix_multiply" and matrix_b:
                result = engine.run(operation=operation, expression=expression, matrix_b=matrix_b)
            else:
                result = engine.run(operation=operation, expression=expression)
        else:
            return {"error": f"Unknown operation: {operation}"}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = JsonRenderer()
    rendered = renderer.render(result=result, format="json", verbosity=verbosity)
    return Response(content=rendered, media_type="application/json")


@app.get("/differentiate")
def differentiate(expr: str, variable: str = "x", order: int = 1, format: str = "json", verbosity: str = "detailed"):
    """Differentiate an expression with respect to a variable.
    
    Args:
        expr: Mathematical expression (e.g., 'sin(x**2)')
        variable: Variable to differentiate with respect to (default: 'x')
        order: Order of derivative (1 for first derivative, 2 for second, etc.; default: 1)
        format: Output format ('json' or 'text')
        verbosity: Detail level ('concise', 'detailed', or 'teacher')
    
    Returns:
        Differentiation result with step-by-step explanation
    """
    if not expr or not expr.strip():
        return {"error": "Missing required parameter 'expr'. Example: ?expr=sin(x**2)"}
    
    if not variable or not variable.strip():
        return {"error": "Variable parameter cannot be empty"}
    
    if order < 1:
        return {"error": f"Order must be at least 1, got {order}"}
    
    if order > 10:
        return {"error": f"Order must be at most 10, got {order}"}
    
    if verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="differentiate", expression=expr, variable=variable, order=order)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=format)
    if renderer is None:
        renderer = JsonRenderer()
        format = "json"

    rendered = renderer.render(result=result, format=format, verbosity=verbosity)
    media_type = "application/json" if format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/multiply")
def matrix_multiply(req: MatrixMultiplyRequest):
    """Multiply two matrices with step-by-step explanation.
    
    Args:
        req: Request body with matrix_a, matrix_b, format, verbosity
    
    Returns:
        Matrix multiplication result with step-by-step explanation
    """
    if not req.matrix_a or not req.matrix_a.strip():
        return {"error": "Missing required parameter 'matrix_a'. Example: [[1,2],[3,4]]"}
    
    if not req.matrix_b or not req.matrix_b.strip():
        return {"error": "Missing required parameter 'matrix_b'. Example: [[5,6],[7,8]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_multiply", expression=req.matrix_a, matrix_b=req.matrix_b)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/determinant")
def matrix_determinant(req: MatrixRequest):
    """Calculate the determinant of a square matrix with step-by-step explanation.
    
    Args:
        req: Request body with matrix, format, verbosity
    
    Returns:
        Determinant value with step-by-step explanation
    """
    if not req.matrix or not req.matrix.strip():
        return {"error": "Missing required parameter 'matrix'. Example: [[1,2],[3,4]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_determinant", expression=req.matrix)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/inverse")
def matrix_inverse(req: MatrixRequest):
    """Calculate the inverse of a square matrix with step-by-step explanation.
    
    Args:
        req: Request body with matrix, format, verbosity
    
    Returns:
        Inverse matrix with step-by-step explanation
    """
    if not req.matrix or not req.matrix.strip():
        return {"error": "Missing required parameter 'matrix'. Example: [[1,2],[3,4]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_inverse", expression=req.matrix)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/rref")
def matrix_rref(req: MatrixRequest):
    """Transform a matrix to Reduced Row Echelon Form (RREF) with step-by-step row operations.
    
    Args:
        req: Request body with matrix, format, verbosity
    
    Returns:
        RREF matrix with step-by-step row operations
    """
    if not req.matrix or not req.matrix.strip():
        return {"error": "Missing required parameter 'matrix'. Example: [[1,2,3],[4,5,6]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_rref", expression=req.matrix)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/eigenvalues")
def matrix_eigenvalues(req: MatrixRequest):
    """Calculate eigenvalues and eigenvectors of a square matrix with step-by-step explanation.
    
    Args:
        req: Request body with matrix, format, verbosity
    
    Returns:
        Eigenvalues and eigenvectors with step-by-step explanation
    """
    if not req.matrix or not req.matrix.strip():
        return {"error": "Missing required parameter 'matrix'. Example: [[1,2],[3,4]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_eigenvalues", expression=req.matrix)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)


@app.post("/matrix/lu")
def matrix_lu(req: MatrixRequest):
    """Perform LU decomposition with partial pivoting: PA = LU.
    
    Args:
        req: Request body with matrix, format, verbosity
    
    Returns:
        P, L, U matrices with step-by-step explanation
    """
    if not req.matrix or not req.matrix.strip():
        return {"error": "Missing required parameter 'matrix'. Example: [[1,2],[3,4]]"}
    
    if req.verbosity not in ("concise", "detailed", "teacher"):
        return {"error": f"Invalid verbosity '{req.verbosity}'. Valid options: concise, detailed, teacher"}
    
    engine = default_engine(load_entry_points=True)
    
    try:
        result = engine.run(operation="matrix_lu", expression=req.matrix)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    renderer = engine.registry.get_renderer(format=req.format)
    if renderer is None:
        renderer = JsonRenderer()

    rendered = renderer.render(result=result, format=req.format, verbosity=req.verbosity)
    media_type = "application/json" if req.format == "json" else "text/plain"
    return Response(content=rendered, media_type=media_type)
