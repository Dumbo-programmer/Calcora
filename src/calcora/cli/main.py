from __future__ import annotations

from enum import Enum

try:
    import typer
except Exception as e:  # noqa: BLE001
    raise RuntimeError("Typer is not installed. Install with: pip install 'calcora[cli]'") from e

from ..bootstrap import default_engine

app = typer.Typer(add_completion=False, help="Calcora CLI: offline, explainable computation.")


class VerbosityLevel(str, Enum):
    """Valid verbosity levels for output."""
    concise = "concise"
    detailed = "detailed"
    teacher = "teacher"


class FormatType(str, Enum):
    """Valid output formats."""
    text = "text"
    json = "json"


@app.command()
def differentiate(
    expr: str = typer.Argument(..., help="Expression to differentiate (e.g. 'sin(x**2)')"),
    variable: str = typer.Option("x", "--variable", "-v", help="Variable to differentiate with respect to"),
    order: int = typer.Option(1, "--order", "-n", help="Order of derivative (1 for first, 2 for second, etc.)"),
    format: FormatType = typer.Option(FormatType.text, "--format", help="Renderer format"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.detailed, "--verbosity", help="Output detail level"),
):
    """Differentiate an expression with respect to a variable."""
    if order < 1:
        typer.echo(f"❌ Order must be at least 1, got {order}", err=True)
        raise typer.Exit(code=1)
    if order > 10:
        typer.echo(f"❌ Order must be at most 10, got {order}", err=True)
        raise typer.Exit(code=1)
    
    engine = default_engine(load_entry_points=True)
    try:
        result = engine.run(operation="differentiate", expression=expr, variable=variable, order=order)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}", err=True)
        raise typer.Exit(code=1) from e

    renderer = engine.registry.get_renderer(format=format.value)
    if renderer is None:
        raise typer.BadParameter(f"Unknown format '{format.value}'. Try: text, json")

    typer.echo(renderer.render(result=result, format=format.value, verbosity=verbosity.value))


@app.command()
def expand(
    expr: str = typer.Argument(..., help="Expression to expand (e.g. '(x+1)**2')"),
    format: FormatType = typer.Option(FormatType.text, "--format", help="Renderer format"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.detailed, "--verbosity", help="Output detail level"),
):
    """Expand algebraic expressions using distributive law."""
    engine = default_engine(load_entry_points=True)
    try:
        result = engine.run(operation="expand", expression=expr)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}", err=True)
        raise typer.Exit(code=1) from e

    renderer = engine.registry.get_renderer(format=format.value)
    if renderer is None:
        raise typer.BadParameter(f"Unknown format '{format.value}'. Try: text, json")

    typer.echo(renderer.render(result=result, format=format.value, verbosity=verbosity.value))


@app.command()
def factor(
    expr: str = typer.Argument(..., help="Expression to factor (e.g. 'x**2 + 5*x + 6')"),
    format: FormatType = typer.Option(FormatType.text, "--format", help="Renderer format"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.detailed, "--verbosity", help="Output detail level"),
):
    """Factor algebraic expressions."""
    engine = default_engine(load_entry_points=True)
    try:
        result = engine.run(operation="factor", expression=expr)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}", err=True)
        raise typer.Exit(code=1) from e

    renderer = engine.registry.get_renderer(format=format.value)
    if renderer is None:
        raise typer.BadParameter(f"Unknown format '{format.value}'. Try: text, json")

    typer.echo(renderer.render(result=result, format=format.value, verbosity=verbosity.value))


@app.command()
def simplify(
    expr: str = typer.Argument(..., help="Expression to simplify (e.g. 'sin(x)**2 + cos(x)**2')"),
    format: FormatType = typer.Option(FormatType.text, "--format", help="Renderer format"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.detailed, "--verbosity", help="Output detail level"),
):
    """Simplify expressions using algebraic and trigonometric identities."""
    engine = default_engine(load_entry_points=True)
    try:
        result = engine.run(operation="simplify", expression=expr)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}", err=True)
        raise typer.Exit(code=1) from e

    renderer = engine.registry.get_renderer(format=format.value)
    if renderer is None:
        raise typer.BadParameter(f"Unknown format '{format.value}'. Try: text, json")

    typer.echo(renderer.render(result=result, format=format.value, verbosity=verbosity.value))


@app.command()
def rules(
    operation: str = typer.Option("differentiate", "--operation", help="Operation name"),
):
    engine = default_engine(load_entry_points=True)
    for name in engine.available_rules(operation=operation):
        typer.echo(name)


@app.command(name="matrix-multiply")
def matrix_multiply(
    matrix_a: str = typer.Argument(..., help="First matrix as JSON array (e.g. '[[1,2],[3,4]]')"),
    matrix_b: str = typer.Argument(..., help="Second matrix as JSON array (e.g. '[[5,6],[7,8]]')"),
    format: FormatType = typer.Option(FormatType.text, "--format", help="Renderer format"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.detailed, "--verbosity", help="Output detail level"),
):
    """Multiply two matrices with step-by-step explanation."""
    engine = default_engine(load_entry_points=True)
    try:
        result = engine.run(operation="matrix_multiply", expression=matrix_a, matrix_b=matrix_b)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}", err=True)
        raise typer.Exit(code=1) from e

    renderer = engine.registry.get_renderer(format=format.value)
    if renderer is None:
        raise typer.BadParameter(f"Unknown format '{format.value}'. Try: text, json")

    typer.echo(renderer.render(result=result, format=format.value, verbosity=verbosity.value))


@app.command(name="matrix-determinant")
def matrix_determinant(
    matrix: str = typer.Argument(..., help="Square matrix as JSON array (e.g. '[[1,2],[3,4]]')"),
    format: FormatType = typer.Option(FormatType.text, "--format", help="Renderer format"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.detailed, "--verbosity", help="Output detail level"),
):
    """Calculate the determinant of a square matrix with step-by-step explanation."""
    engine = default_engine(load_entry_points=True)
    try:
        result = engine.run(operation="matrix_determinant", expression=matrix)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}", err=True)
        raise typer.Exit(code=1) from e

    renderer = engine.registry.get_renderer(format=format.value)
    if renderer is None:
        raise typer.BadParameter(f"Unknown format '{format.value}'. Try: text, json")

    typer.echo(renderer.render(result=result, format=format.value, verbosity=verbosity.value))


@app.command(name="matrix-inverse")
def matrix_inverse(
    matrix: str = typer.Argument(..., help="Square matrix as JSON array (e.g. '[[1,2],[3,4]]')"),
    format: FormatType = typer.Option(FormatType.text, "--format", help="Renderer format"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.detailed, "--verbosity", help="Output detail level"),
):
    """Calculate the inverse of a square matrix with step-by-step explanation."""
    engine = default_engine(load_entry_points=True)
    try:
        result = engine.run(operation="matrix_inverse", expression=matrix)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}", err=True)
        raise typer.Exit(code=1) from e

    renderer = engine.registry.get_renderer(format=format.value)
    if renderer is None:
        raise typer.BadParameter(f"Unknown format '{format.value}'. Try: text, json")

    typer.echo(renderer.render(result=result, format=format.value, verbosity=verbosity.value))


@app.command(name="matrix-rref")
def matrix_rref(
    matrix: str = typer.Argument(..., help="Matrix as JSON array (e.g. '[[1,2,3],[4,5,6]]')"),
    format: FormatType = typer.Option(FormatType.text, "--format", help="Renderer format"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.detailed, "--verbosity", help="Output detail level"),
):
    """Transform a matrix to Reduced Row Echelon Form (RREF) with step-by-step row operations."""
    engine = default_engine(load_entry_points=True)
    try:
        result = engine.run(operation="matrix_rref", expression=matrix)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}", err=True)
        raise typer.Exit(code=1) from e

    renderer = engine.registry.get_renderer(format=format.value)
    if renderer is None:
        raise typer.BadParameter(f"Unknown format '{format.value}'. Try: text, json")

    typer.echo(renderer.render(result=result, format=format.value, verbosity=verbosity.value))


@app.command(name="matrix-eigenvalues")
def matrix_eigenvalues(
    matrix: str = typer.Argument(..., help="Square matrix as JSON array (e.g. '[[1,2],[3,4]]')"),
    format: FormatType = typer.Option(FormatType.text, "--format", help="Renderer format"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.detailed, "--verbosity", help="Output detail level"),
):
    """Calculate eigenvalues and eigenvectors of a square matrix with step-by-step explanation."""
    engine = default_engine(load_entry_points=True)
    try:
        result = engine.run(operation="matrix_eigenvalues", expression=matrix)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}", err=True)
        raise typer.Exit(code=1) from e

    renderer = engine.registry.get_renderer(format=format.value)
    if renderer is None:
        raise typer.BadParameter(f"Unknown format '{format.value}'. Try: text, json")

    typer.echo(renderer.render(result=result, format=format.value, verbosity=verbosity.value))


@app.command(name="matrix-lu")
def matrix_lu(
    matrix: str = typer.Argument(..., help="Matrix as JSON array (e.g. '[[1,2],[3,4]]')"),
    format: FormatType = typer.Option(FormatType.text, "--format", help="Renderer format"),
    verbosity: VerbosityLevel = typer.Option(VerbosityLevel.detailed, "--verbosity", help="Output detail level"),
):
    """Perform LU decomposition with partial pivoting: PA = LU."""
    engine = default_engine(load_entry_points=True)
    try:
        result = engine.run(operation="matrix_lu", expression=matrix)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}", err=True)
        raise typer.Exit(code=1) from e

    renderer = engine.registry.get_renderer(format=format.value)
    if renderer is None:
        raise typer.BadParameter(f"Unknown format '{format.value}'. Try: text, json")

    typer.echo(renderer.render(result=result, format=format.value, verbosity=verbosity.value))
