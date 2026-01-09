"""Linear algebra rules for step-by-step matrix operations."""

from __future__ import annotations

import json
from typing import Any

from .models import StepGraph, StepNode
from ..plugins.decorators import rule


def _sp():
    """Lazy import of SymPy."""
    try:
        import sympy as sp  # type: ignore

        return sp
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(
            "SymPy is required for linear algebra operations. Install with: pip install 'calcora[engine-sympy]'"
        ) from e


def _parse_matrix(matrix_str: str):
    """Parse a matrix from JSON string or SymPy format.
    
    Supports:
    - Numeric matrices: [[1,2],[3,4]]
    - Symbolic matrices: [["a","b"],["c","d"]]
    - Mixed: [[1,"a"],[2,"b"]]
    """
    sp = _sp()
    
    # Try parsing as JSON first
    try:
        data = json.loads(matrix_str)
        if isinstance(data, list) and all(isinstance(row, list) for row in data):
            # Convert string entries to SymPy symbols
            sympy_data = []
            for row in data:
                sympy_row = []
                for element in row:
                    if isinstance(element, str):
                        # Parse as SymPy expression (could be symbol or expression like "2*a")
                        sympy_row.append(sp.sympify(element))
                    else:
                        sympy_row.append(element)
                sympy_data.append(sympy_row)
            return sp.Matrix(sympy_data)
    except (json.JSONDecodeError, ValueError) as e:
        # If JSON parsing failed, not a valid matrix
        raise ValueError(f"Could not parse matrix: {matrix_str}") from e
    
    raise ValueError(f"Could not parse matrix: {matrix_str}")


def _format_matrix(matrix) -> str:
    """Format a matrix as JSON string, preserving symbols."""
    sp = _sp()
    if isinstance(matrix, sp.MatrixBase):
        # Convert elements: integers to int, floats to float, symbols to string
        python_list = []
        for row in matrix.tolist():
            formatted_row = []
            for element in row:
                if element.is_Integer:
                    formatted_row.append(int(element))
                elif element.is_Float or element.is_Rational:
                    formatted_row.append(float(element))
                else:
                    # Symbol or expression - convert to string
                    formatted_row.append(str(element))
            python_list.append(formatted_row)
        return json.dumps(python_list)
    return str(matrix)


def _teacher(expl: str, teacher: str) -> dict[str, Any]:
    return {"explanations": {"detailed": expl, "teacher": teacher}}


@rule(
    name="matrix_multiply",
    operation="matrix_multiply",
    priority=100,
    domains=("linear_algebra",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: True,  # Always matches for matrix multiplication
)
def matrix_multiply(expression: str, graph: StepGraph):
    """Multiply two matrices step-by-step.
    
    Args:
        expression: Two matrices separated by '|||' as JSON strings
    """
    sp = _sp()
    
    # Parse the input - expecting "matrix_a|||matrix_b" format
    if "|||" not in expression:
        raise ValueError("Expected two matrices separated by '|||'. Example: [[1,2],[3,4]]|||[[5,6],[7,8]]")
    
    parts = expression.split("|||", 1)
    matrix_a_str = parts[0].strip()
    matrix_b_str = parts[1].strip()
    
    A = _parse_matrix(matrix_a_str)
    B = _parse_matrix(matrix_b_str)
    
    # Validate dimensions
    if A.cols != B.rows:
        raise ValueError(
            f"Cannot multiply matrices: A is {A.rows}×{A.cols}, B is {B.rows}×{B.cols}. "
            f"Number of columns in A ({A.cols}) must equal number of rows in B ({B.rows})."
        )
    
    m, n, p = A.rows, A.cols, B.cols
    
    # Create result matrix with symbolic entries
    result = sp.zeros(m, p)
    
    # Generate steps for each element
    for i in range(m):
        for j in range(p):
            # Calculate C[i,j] = sum of A[i,k] * B[k,j] for k=0..n-1
            terms = []
            for k in range(n):
                a_val = A[i, k]
                b_val = B[k, j]
                product = a_val * b_val
                terms.append((a_val, b_val, product))
            
            # Sum the products
            element_sum = sum(a * b for a, b, _ in terms)
            result[i, j] = element_sum
            
            # Create step showing calculation for this element
            if len(graph.nodes) < 8:  # Limit detailed steps to avoid clutter
                terms_str = " + ".join(f"({a})·({b})" for a, b, _ in terms)
                computed_str = " + ".join(f"{p}" for _, _, p in terms)
                
                step_id = f"element_{i}_{j}"
                step_input = f"C[{i},{j}] = {terms_str}"
                step_output = f"{element_sum}"
                
                graph.nodes.append(
                    StepNode(
                        id=step_id,
                        operation="matrix_multiply",
                        rule=f"multiply_element",
                        input=step_input,
                        output=step_output,
                        explanation=f"Calculate element ({i},{j}) by taking row {i} of A times column {j} of B: {computed_str} = {element_sum}",
                    )
                )
    
    # Final result
    result_str = _format_matrix(result)
    
    expl = f"Multiply {m}×{n} matrix A by {n}×{p} matrix B to get {m}×{p} matrix C. Each element C[i,j] is the dot product of row i from A and column j from B."
    
    return (
        result_str,
        expl,
        [],
        _teacher(
            expl,
            f"Matrix multiplication works by taking each row of the first matrix and each column of the second matrix, "
            f"multiplying corresponding elements, and summing them up. The result has dimensions {m}×{p}."
        ),
    )


@rule(
    name="matrix_determinant",
    operation="matrix_determinant",
    priority=100,
    domains=("linear_algebra",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: True,
)
def matrix_determinant(expression: str, graph: StepGraph):
    """Calculate the determinant of a square matrix step-by-step.
    
    Args:
        expression: Matrix as JSON string (must be square)
    """
    sp = _sp()
    
    A = _parse_matrix(expression)
    
    # Validate it's a square matrix
    if A.rows != A.cols:
        raise ValueError(
            f"Determinant requires a square matrix. Got {A.rows}×{A.cols} matrix. "
            f"The matrix must have the same number of rows and columns."
        )
    
    n = A.rows
    
    # For small matrices, show explicit calculation
    if n == 1:
        det = A[0, 0]
        expl = f"For a 1×1 matrix, the determinant is simply the element itself: {det}"
        
        return (
            str(det),
            expl,
            [],
            _teacher(expl, "A 1×1 matrix contains just one number, so that number is its determinant."),
        )
    
    elif n == 2:
        # det = ad - bc
        a, b, c, d = A[0,0], A[0,1], A[1,0], A[1,1]
        det = a*d - b*c
        
        graph.nodes.append(
            StepNode(
                id="det_2x2",
                operation="matrix_determinant",
                rule="determinant_2x2",
                input=f"det([[{a}, {b}], [{c}, {d}]])",
                output=f"{det}",
                explanation=f"For a 2×2 matrix, det = ad - bc = ({a})({d}) - ({b})({c}) = {a*d} - {b*c} = {det}",
            )
        )
        
        expl = f"Calculate determinant using 2×2 formula: ad - bc"
        
        return (
            str(det),
            expl,
            [],
            _teacher(
                expl,
                f"For a 2×2 matrix [[a,b],[c,d]], the determinant is ad-bc. This represents the signed area of the parallelogram formed by the row vectors."
            ),
        )
    
    else:
        # For larger matrices, use cofactor expansion along first row
        det = A.det()
        
        # Show cofactor expansion for 3×3
        if n == 3:
            minor_steps = []
            for j in range(3):
                # Calculate minor (2×2 matrix by removing row 0 and column j)
                minor_matrix = A.minor_submatrix(0, j)
                cofactor = A.cofactor(0, j)
                sign = "+" if j % 2 == 0 else "-"
                
                minor_det = minor_matrix.det()
                minor_steps.append(f"{sign}{A[0,j]}·det(M{j}) = {sign}{A[0,j]}·({minor_det})")
                
                graph.nodes.append(
                    StepNode(
                        id=f"minor_0_{j}",
                        operation="matrix_determinant",
                        rule="cofactor_expansion",
                        input=f"Minor M[0,{j}] = det({_format_matrix(minor_matrix)})",
                        output=f"{minor_det}",
                        explanation=f"Calculate 2×2 minor by removing row 0 and column {j}",
                    )
                )
            
            expansion_str = " + ".join(minor_steps)
            graph.nodes.append(
                StepNode(
                    id="cofactor_sum",
                    operation="matrix_determinant",
                    rule="cofactor_expansion",
                    input=f"det(A) = {expansion_str}",
                    output=f"{det}",
                    explanation="Sum the cofactor terms to get the determinant",
                )
            )
        
        expl = f"Calculate {n}×{n} determinant using cofactor expansion along the first row"
        
        return (
            str(det),
            expl,
            [],
            _teacher(
                expl,
                f"Cofactor expansion breaks down an n×n determinant into n smaller (n-1)×(n-1) determinants. "
                f"For each element in the first row, multiply it by its cofactor (with alternating signs) and sum them."
            ),
        )


@rule(
    name="matrix_inverse",
    operation="matrix_inverse",
    priority=100,
    domains=("linear_algebra",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: True,
)
def matrix_inverse(expression: str, graph: StepGraph):
    """Calculate the inverse of a square matrix step-by-step.
    
    Args:
        expression: Square matrix as JSON string
    """
    sp = _sp()
    
    A = _parse_matrix(expression)
    
    # Validate it's a square matrix
    if A.rows != A.cols:
        raise ValueError(
            f"Matrix inverse requires a square matrix. Got {A.rows}×{A.cols} matrix. "
            f"The matrix must have the same number of rows and columns."
        )
    
    n = A.rows
    
    # Check if matrix is invertible
    det = A.det()
    if det == 0:
        raise ValueError(
            f"Matrix is singular (determinant = 0) and cannot be inverted. "
            f"A matrix must have a non-zero determinant to be invertible."
        )
    
    # Calculate inverse
    A_inv = A.inv()
    
    # Show steps based on size
    if n == 2:
        # For 2×2: A^-1 = (1/det) * [[d, -b], [-c, a]]
        a, b, c, d = A[0,0], A[0,1], A[1,0], A[1,1]
        
        graph.nodes.append(
            StepNode(
                id="det_calc",
                operation="matrix_inverse",
                rule="inverse_2x2",
                input=f"det(A) = ad - bc = ({a})({d}) - ({b})({c})",
                output=f"{det}",
                explanation=f"Calculate determinant: {a*d} - {b*c} = {det}",
            )
        )
        
        graph.nodes.append(
            StepNode(
                id="inverse_formula",
                operation="matrix_inverse",
                rule="inverse_2x2",
                input=f"A^-1 = (1/{det}) * [[{d}, {-b}], [{-c}, {a}]]",
                output=_format_matrix(A_inv),
                explanation=f"Apply 2×2 inverse formula: swap diagonal, negate off-diagonal, divide by determinant",
            )
        )
        
        expl = f"Calculate inverse using 2×2 formula: A^-1 = (1/det(A)) * adj(A)"
        
        return (
            _format_matrix(A_inv),
            expl,
            [],
            _teacher(
                expl,
                f"For a 2×2 matrix [[a,b],[c,d]], the inverse is (1/(ad-bc)) * [[d,-b],[-c,a]]. "
                f"This swaps the diagonal elements, negates the off-diagonal elements, and divides everything by the determinant."
            ),
        )
    
    else:
        # For larger matrices, use adjugate method
        graph.nodes.append(
            StepNode(
                id="det_calc",
                operation="matrix_inverse",
                rule="inverse_adjugate",
                input=f"det(A)",
                output=f"{det}",
                explanation=f"Calculate determinant of {n}×{n} matrix: {det}",
            )
        )
        
        graph.nodes.append(
            StepNode(
                id="adjugate_calc",
                operation="matrix_inverse",
                rule="inverse_adjugate",
                input=f"Compute adjugate matrix (transpose of cofactor matrix)",
                output="Adjugate calculated",
                explanation=f"Form the matrix of cofactors, then transpose it to get the adjugate",
            )
        )
        
        graph.nodes.append(
            StepNode(
                id="inverse_result",
                operation="matrix_inverse",
                rule="inverse_adjugate",
                input=f"A^-1 = (1/{det}) * adj(A)",
                output=_format_matrix(A_inv),
                explanation=f"Multiply adjugate matrix by 1/{det} to get the inverse",
            )
        )
        
        expl = f"Calculate {n}×{n} inverse using adjugate method: A^-1 = (1/det(A)) * adj(A)"
        
        return (
            _format_matrix(A_inv),
            expl,
            [],
            _teacher(
                expl,
                f"The inverse is computed using the adjugate (adjoint) matrix. "
                f"The adjugate is the transpose of the cofactor matrix. "
                f"Dividing the adjugate by the determinant gives the inverse. "
                f"The result satisfies A * A^-1 = I (identity matrix)."
            ),
        )


@rule(
    name="matrix_rref",
    operation="matrix_rref",
    priority=100,
    domains=("linear_algebra",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: True,  # Always matches for RREF operation
)
def matrix_rref(expression: str, graph: StepGraph):
    """Transform a matrix to its Reduced Row Echelon Form (RREF) with step-by-step row operations.
    
    The RREF of a matrix is a canonical form where:
    1. All zero rows are at the bottom
    2. The leading entry (pivot) of each nonzero row is 1
    3. Each pivot is the only nonzero entry in its column
    4. Each pivot is to the right of the pivot in the row above
    
    Args:
        expression: The matrix as JSON array string
        graph: The step graph to record operations
    
    Returns:
        Tuple of (output_matrix_json, explanation, [], teacher_explanation)
    """
    A = _parse_matrix(expression)
    m, n = A.shape  # m rows, n columns
    
    # Create a copy to work with
    R = A.as_mutable()
    
    # Track row operations for explanation
    operations = []
    
    graph.nodes.append(
        StepNode(
            id="rref_start",
            operation="matrix_rref",
            rule="rref_initialize",
            input=_format_matrix(A),
            output=f"Starting {m}×{n} matrix",
            explanation=f"Begin row reduction to transform matrix to RREF",
        )
    )
    
    current_row = 0
    
    # Process each column for pivots
    for col in range(n):
        if current_row >= m:
            break
        
        # Find pivot (first nonzero entry in column at or below current_row)
        pivot_row = None
        for row in range(current_row, m):
            if R[row, col] != 0:
                pivot_row = row
                break
        
        if pivot_row is None:
            # No pivot in this column, move to next column
            continue
        
        # Swap rows if needed
        if pivot_row != current_row:
            R.row_swap(current_row, pivot_row)
            operations.append(f"R{current_row+1} ↔ R{pivot_row+1}")
            graph.nodes.append(
                StepNode(
                    id=f"rref_swap_{current_row}_{pivot_row}",
                    operation="matrix_rref",
                    rule="rref_swap",
                    input=f"Swap row {current_row+1} with row {pivot_row+1}",
                    output=_format_matrix(R),
                    explanation=f"Move nonzero pivot to row {current_row+1}",
                )
            )
        
        # Scale row to make pivot = 1
        pivot_value = R[current_row, col]
        if pivot_value != 1:
            R.row_op(current_row, lambda v, _: v / pivot_value)
            operations.append(f"R{current_row+1} → (1/{pivot_value}) * R{current_row+1}")
            graph.nodes.append(
                StepNode(
                    id=f"rref_scale_{current_row}",
                    operation="matrix_rref",
                    rule="rref_scale",
                    input=f"Divide row {current_row+1} by {pivot_value}",
                    output=_format_matrix(R),
                    explanation=f"Scale row to make pivot = 1",
                )
            )
        
        # Eliminate all other entries in this column
        for row in range(m):
            if row != current_row and R[row, col] != 0:
                factor = R[row, col]
                R.row_op(row, lambda v, j: v - factor * R[current_row, j])
                operations.append(f"R{row+1} → R{row+1} - ({factor}) * R{current_row+1}")
                graph.nodes.append(
                    StepNode(
                        id=f"rref_eliminate_{row}_{current_row}",
                        operation="matrix_rref",
                        rule="rref_eliminate",
                        input=f"Eliminate entry at row {row+1}, column {col+1}",
                        output=_format_matrix(R),
                        explanation=f"Subtract {factor} times row {current_row+1} from row {row+1}",
                    )
                )
        
        current_row += 1
    
    # Convert back to immutable matrix
    R = R.as_immutable()
    
    graph.nodes.append(
        StepNode(
            id="rref_complete",
            operation="matrix_rref",
            rule="rref_final",
            input="All row operations complete",
            output=_format_matrix(R),
            explanation=f"Matrix is now in reduced row echelon form",
        )
    )
    
    expl = f"Transform {m}×{n} matrix to RREF using {len(operations)} row operations"
    
    return (
        _format_matrix(R),
        expl,
        [],
        _teacher(
            expl,
            f"RREF is computed through systematic row operations: "
            f"(1) Find pivot (leading nonzero) in each column, "
            f"(2) Swap rows to position pivot correctly, "
            f"(3) Scale row to make pivot = 1, "
            f"(4) Eliminate all other entries in pivot column. "
            f"The result is unique for any matrix and useful for solving linear systems, "
            f"finding rank, and determining linear independence. "
            f"Operations performed: {'; '.join(operations) if operations else 'None needed (already in RREF)'}"
        ),
    )


@rule(
    name="matrix_eigenvalues",
    operation="matrix_eigenvalues",
    priority=100,
    domains=("linear_algebra",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: True,  # Always matches for eigenvalues operation
)
def matrix_eigenvalues(expression: str, graph: StepGraph):
    """Calculate eigenvalues and eigenvectors of a square matrix with step-by-step explanation.
    
    Eigenvalues λ satisfy: det(A - λI) = 0
    Eigenvectors v satisfy: Av = λv
    
    Args:
        expression: The matrix as JSON array string
        graph: The step graph to record operations
    
    Returns:
        Tuple of (output_json, explanation, [], teacher_explanation)
    """
    sp = _sp()
    A = _parse_matrix(expression)
    m, n = A.shape
    
    # Must be square matrix
    if m != n:
        raise ValueError(
            f"Eigenvalues require a square matrix. Got {m}×{n} matrix. "
            f"The matrix must have the same number of rows and columns."
        )
    
    graph.nodes.append(
        StepNode(
            id="eigenvalues_start",
            operation="matrix_eigenvalues",
            rule="eigenvalues_initialize",
            input=_format_matrix(A),
            output=f"Starting {n}×{n} matrix",
            explanation=f"Find eigenvalues λ by solving det(A - λI) = 0",
        )
    )
    
    # Calculate eigenvalues
    eigenvals = A.eigenvals()
    eigenvects = A.eigenvects()
    
    # Format eigenvalues with multiplicities
    eigenvalue_list = []
    for eigenval, multiplicity in eigenvals.items():
        eigenvalue_list.append({"value": float(eigenval) if eigenval.is_real else complex(eigenval), "multiplicity": multiplicity})
    
    graph.nodes.append(
        StepNode(
            id="eigenvalues_characteristic",
            operation="matrix_eigenvalues",
            rule="eigenvalues_characteristic_poly",
            input=f"Compute characteristic polynomial det(A - λI)",
            output=f"Found {len(eigenvals)} distinct eigenvalue(s)",
            explanation=f"The characteristic polynomial gives the eigenvalues when solved",
        )
    )
    
    # Add step for each eigenvalue
    for i, (eigenval, multiplicity, eigenvects_list) in enumerate(eigenvects):
        eigenval_float = float(eigenval) if eigenval.is_real else complex(eigenval)
        
        graph.nodes.append(
            StepNode(
                id=f"eigenvalue_{i}",
                operation="matrix_eigenvalues",
                rule="eigenvalue_found",
                input=f"λ{i+1} = {eigenval}",
                output=f"Multiplicity: {multiplicity}",
                explanation=f"Eigenvalue λ{i+1} = {eigenval_float} with algebraic multiplicity {multiplicity}",
            )
        )
        
        # Add eigenvectors for this eigenvalue
        for j, eigenvect in enumerate(eigenvects_list):
            graph.nodes.append(
                StepNode(
                    id=f"eigenvector_{i}_{j}",
                    operation="matrix_eigenvalues",
                    rule="eigenvector_found",
                    input=f"Solve (A - {eigenval}I)v = 0",
                    output=_format_matrix(eigenvect),
                    explanation=f"Eigenvector v{j+1} for λ{i+1}: satisfies Av = {eigenval_float}v",
                )
            )
    
    # Prepare output
    output = {
        "eigenvalues": eigenvalue_list,
        "eigenvectors": {}
    }
    
    for i, (eigenval, multiplicity, eigenvects_list) in enumerate(eigenvects):
        eigenval_str = str(float(eigenval) if eigenval.is_real else complex(eigenval))
        output["eigenvectors"][eigenval_str] = [
            json.loads(_format_matrix(v)) for v in eigenvects_list
        ]
    
    expl = f"Found {len(eigenvals)} distinct eigenvalue(s) for {n}×{n} matrix"
    
    return (
        json.dumps(output),
        expl,
        [],
        _teacher(
            expl,
            f"Eigenvalues are found by solving the characteristic equation det(A - λI) = 0. "
            f"Each eigenvalue λ has corresponding eigenvectors v that satisfy Av = λv. "
            f"Eigenvalues represent how much a matrix scales vectors in certain directions. "
            f"The algebraic multiplicity is how many times an eigenvalue appears as a root. "
            f"Eigenvectors form the basis for understanding matrix transformations and diagonalization."
        ),
    )


@rule(
    name="matrix_lu",
    operation="matrix_lu",
    priority=100,
    domains=("linear_algebra",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: True,  # Always matches for LU decomposition
)
def matrix_lu(expression: str, graph: StepGraph):
    """Perform LU decomposition with partial pivoting: PA = LU.
    
    Decomposes matrix A into:
    - P: Permutation matrix (for row swaps)
    - L: Lower triangular matrix (with 1s on diagonal)
    - U: Upper triangular matrix
    
    Args:
        expression: The matrix as JSON array string
        graph: The step graph to record operations
    
    Returns:
        Tuple of (output_json, explanation, [], teacher_explanation)
    """
    sp = _sp()
    A = _parse_matrix(expression)
    m, n = A.shape
    
    graph.nodes.append(
        StepNode(
            id="lu_start",
            operation="matrix_lu",
            rule="lu_initialize",
            input=_format_matrix(A),
            output=f"Starting {m}×{n} matrix",
            explanation=f"Decompose A into PA = LU using Gaussian elimination with partial pivoting",
        )
    )
    
    # Perform LU decomposition with partial pivoting
    L, U, perm = A.LUdecomposition()
    
    # Create permutation matrix from permutation list
    P = sp.eye(m)
    for i, j in enumerate(perm):
        if i != j:
            # Swap rows i and j in identity matrix
            P.row_swap(i, j)
    
    graph.nodes.append(
        StepNode(
            id="lu_pivot",
            operation="matrix_lu",
            rule="lu_permutation",
            input="Apply partial pivoting",
            output=_format_matrix(P),
            explanation=f"Permutation matrix P records row swaps for numerical stability",
        )
    )
    
    graph.nodes.append(
        StepNode(
            id="lu_lower",
            operation="matrix_lu",
            rule="lu_lower_triangular",
            input="Compute lower triangular matrix L",
            output=_format_matrix(L),
            explanation=f"L is lower triangular with 1s on diagonal, stores elimination multipliers",
        )
    )
    
    graph.nodes.append(
        StepNode(
            id="lu_upper",
            operation="matrix_lu",
            rule="lu_upper_triangular",
            input="Compute upper triangular matrix U",
            output=_format_matrix(U),
            explanation=f"U is upper triangular, result of Gaussian elimination",
        )
    )
    
    # Verify: PA = LU
    graph.nodes.append(
        StepNode(
            id="lu_verify",
            operation="matrix_lu",
            rule="lu_verification",
            input="Verify PA = LU",
            output="Decomposition verified",
            explanation=f"Multiplying L and U gives PA, confirming correct decomposition",
        )
    )
    
    # Prepare output
    output = {
        "P": json.loads(_format_matrix(P)),
        "L": json.loads(_format_matrix(L)),
        "U": json.loads(_format_matrix(U))
    }
    
    expl = f"LU decomposition of {m}×{n} matrix: PA = LU"
    
    return (
        json.dumps(output),
        expl,
        [],
        _teacher(
            expl,
            f"LU decomposition factors a matrix into lower and upper triangular matrices. "
            f"This is useful for solving systems of linear equations efficiently, "
            f"computing determinants (det(A) = det(L)·det(U)), and matrix inversion. "
            f"Partial pivoting (permutation matrix P) ensures numerical stability by "
            f"choosing the largest pivot element at each step. "
            f"Once computed, LU decomposition can be reused to solve Ax = b for multiple right-hand sides."
        ),
    )


# Export all rules
BUILTIN_LINALG_RULES = [
    matrix_multiply,
    matrix_determinant,
    matrix_inverse,
    matrix_rref,
    matrix_eigenvalues,
    matrix_lu,
]
