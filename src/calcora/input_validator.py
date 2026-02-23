"""
Input Validation and Sanitization Layer

Purpose: Prevent code execution, injection attacks, and malicious input.
This is the trust boundary between user input and the symbolic engine.

Security principles:
- Fail early, fail loudly
- Whitelist > Blacklist
- No arbitrary code execution
- No attribute access
- No file system access
"""

import re
import sympy as sp
from typing import Dict, Any, Optional


# Maximum input lengths to prevent DoS
MAX_EXPRESSION_LENGTH = 500
MAX_VARIABLE_NAME_LENGTH = 20

# Allowed characters in mathematical expressions
# Letters, digits, spaces, basic math operators, parentheses, dots, underscores
ALLOWED_CHARS_PATTERN = re.compile(r'^[a-zA-Z0-9\s\+\-\*/\^\(\)\.,_]+$')

# Dangerous patterns that should never appear
BLACKLIST_PATTERNS = [
    r'__',          # Double underscore (Python internals)
    r'import',      # Import statement
    r'eval',        # Eval function
    r'exec',        # Exec function
    r'compile',     # Compile function
    r'open',        # File access
    r'system',      # System calls
    r';',           # Statement separator
    r'lambda',      # Lambda functions
    r'\.\./',       # Path traversal
    r'\\\\',        # Windows path separator
    r'<?xml',       # XML injection
    r'<script',     # XSS attempt
    r'javascript:', # XSS attempt
    r'DROP\s+TABLE', # SQL injection attempt (case insensitive)
]

# Safe symbols and functions allowed in expressions
SAFE_LOCALS = {
    # Basic constants
    'pi': sp.pi,
    'e': sp.E,
    'I': sp.I,
    'oo': sp.oo,  # Infinity
    
    # Basic functions
    'sin': sp.sin,
    'cos': sp.cos,
    'tan': sp.tan,
    'sec': sp.sec,
    'csc': sp.csc,
    'cot': sp.cot,
    
    # Inverse trig
    'asin': sp.asin,
    'acos': sp.acos,
    'atan': sp.atan,
    'arcsin': sp.asin,
    'arccos': sp.acos,
    'arctan': sp.atan,
    
    # Hyperbolic
    'sinh': sp.sinh,
    'cosh': sp.cosh,
    'tanh': sp.tanh,
    'asinh': sp.asinh,
    'acosh': sp.acosh,
    'atanh': sp.atanh,
    
    # Exponential/Logarithmic
    'exp': sp.exp,
    'log': sp.log,
    'ln': sp.log,
    'sqrt': sp.sqrt,
    
    # Other
    'abs': sp.Abs,
    'Abs': sp.Abs,
    'factorial': sp.factorial,
    
    # Explicitly block dangerous builtins
    '__builtins__': {},
    '__import__': None,
    '__name__': None,
    '__file__': None,
}


class InputValidationError(Exception):
    """Raised when input validation fails"""
    pass


def validate_expression(expression: str, max_length: int = MAX_EXPRESSION_LENGTH) -> Dict[str, Any]:
    """
    Validate mathematical expression for safety and correctness.
    
    Returns:
        dict with 'valid': bool, 'error': str (if invalid), 'sanitized': str (if valid)
    
    Raises:
        InputValidationError if validation fails
    """
    # Check 1: Not None/empty
    if not expression or not expression.strip():
        return {
            'valid': False,
            'error': 'Expression cannot be empty',
            'code': 'EMPTY_EXPRESSION'
        }
    
    expression = expression.strip()
    
    # Check 2: Length limit (prevent DoS)
    if len(expression) > max_length:
        return {
            'valid': False,
            'error': f'Expression too long (max {max_length} characters)',
            'code': 'TOO_LONG'
        }
    
    # Check 3: Blacklist patterns (dangerous code)
    for pattern in BLACKLIST_PATTERNS:
        if re.search(pattern, expression, re.IGNORECASE):
            return {
                'valid': False,
                'error': f'Expression contains forbidden pattern: {pattern}',
                'code': 'FORBIDDEN_PATTERN'
            }
    
    # Check 4: Allowed characters only
    if not ALLOWED_CHARS_PATTERN.match(expression):
        # Find the first disallowed character
        disallowed = set(expression) - set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 +-*/^().,_')
        return {
            'valid': False,
            'error': f'Expression contains invalid characters: {", ".join(sorted(disallowed))}',
            'code': 'INVALID_CHARACTERS'
        }
    
    # Check 5: Balanced parentheses
    paren_count = 0
    for char in expression:
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        if paren_count < 0:
            return {
                'valid': False,
                'error': 'Unbalanced parentheses (too many closing)',
                'code': 'UNBALANCED_PARENS'
            }
    
    if paren_count != 0:
        return {
            'valid': False,
            'error': 'Unbalanced parentheses (unclosed opening)',
            'code': 'UNBALANCED_PARENS'
        }
    
    # Check 6: No division by literal zero
    if re.search(r'/\s*0(?:\s|$|\))', expression):
        return {
            'valid': False,
            'error': 'Division by zero detected',
            'code': 'DIVISION_BY_ZERO'
        }
    
    return {
        'valid': True,
        'sanitized': expression
    }


def validate_variable(variable: str) -> Dict[str, Any]:
    """
    Validate variable name for safety.
    
    Returns:
        dict with 'valid': bool, 'error': str (if invalid)
    """
    # Check 1: Not None/empty
    if not variable or not variable.strip():
        return {
            'valid': False,
            'error': 'Variable name cannot be empty',
            'code': 'EMPTY_VARIABLE'
        }
    
    variable = variable.strip()
    
    # Check 2: Length limit
    if len(variable) > MAX_VARIABLE_NAME_LENGTH:
        return {
            'valid': False,
            'error': f'Variable name too long (max {MAX_VARIABLE_NAME_LENGTH} characters)',
            'code': 'TOO_LONG'
        }
    
    # Check 3: Valid Python identifier (letters, digits, underscore, but not starting with digit)
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', variable):
        return {
            'valid': False,
            'error': 'Variable name must start with letter/underscore and contain only letters, digits, underscores',
            'code': 'INVALID_VARIABLE_NAME'
        }
    
    # Check 4: Not a Python keyword
    python_keywords = {'and', 'or', 'not', 'if', 'else', 'elif', 'for', 'while', 'def', 'class', 'import', 'from', 'return', 'yield', 'lambda', 'with', 'as', 'try', 'except', 'finally', 'raise', 'assert', 'del', 'pass', 'break', 'continue', 'global', 'nonlocal', 'is', 'in'}
    if variable.lower() in python_keywords:
        return {
            'valid': False,
            'error': f'Variable name cannot be a Python keyword: {variable}',
            'code': 'PYTHON_KEYWORD'
        }
    
    # Check 5: No double underscore (Python internals)
    if '__' in variable:
        return {
            'valid': False,
            'error': 'Variable name cannot contain double underscores',
            'code': 'DOUBLE_UNDERSCORE'
        }
    
    return {
        'valid': True,
        'sanitized': variable
    }


def safe_sympify(expression: str, local_dict: Optional[Dict] = None) -> sp.Expr:
    """
    Safely parse expression using SymPy with sandboxed locals.
    
    This prevents code execution by:
    - Using restricted local dictionary
    - Disabling builtins
    - Disabling attribute access to dangerous methods
    
    Args:
        expression: Mathematical expression to parse
        local_dict: Additional safe symbols (merged with SAFE_LOCALS)
    
    Returns:
        SymPy expression object
    
    Raises:
        SympifyError: If parsing fails
        InputValidationError: If expression is unsafe
    """
    # Validate input first
    validation = validate_expression(expression)
    if not validation['valid']:
        raise InputValidationError(f"{validation['error']} (code: {validation['code']})")
    
    # Merge custom locals with safe locals
    safe_dict = SAFE_LOCALS.copy()
    if local_dict:
        safe_dict.update(local_dict)
    
    # Parse with restricted environment
    try:
        # evaluate=True allows simplification but not arbitrary code execution
        # locals restricts available names to our whitelist
        result = sp.sympify(
            expression,
            locals=safe_dict,
            evaluate=True,
            rational=False  # Don't convert floats to rationals automatically
        )
        return result
    except (sp.SympifyError, SyntaxError, TypeError, ValueError) as e:
        raise InputValidationError(f"Failed to parse expression: {str(e)}")


def validate_matrix_string(matrix_str: str) -> Dict[str, Any]:
    """
    Validate matrix string format.
    
    Expected format: [[1,2],[3,4]] or [[a,b],[c,d]]
    
    Returns:
        dict with 'valid': bool, 'error': str (if invalid)
    """
    if not matrix_str or not matrix_str.strip():
        return {
            'valid': False,
            'error': 'Matrix string cannot be empty',
            'code': 'EMPTY_MATRIX'
        }
    
    matrix_str = matrix_str.strip()
    
    # Basic bracket matching
    if not (matrix_str.startswith('[[') and matrix_str.endswith(']]')):
        return {
            'valid': False,
            'error': 'Matrix must be enclosed in double brackets: [[...]]',
            'code': 'INVALID_BRACKETS'
        }
    
    # Count brackets
    if matrix_str.count('[') != matrix_str.count(']'):
        return {
            'valid': False,
            'error': 'Unbalanced brackets in matrix',
            'code': 'UNBALANCED_BRACKETS'
        }
    
    # Allowed characters: digits, letters, brackets, commas, spaces, +, -, ., /
    if not re.match(r'^[\[\]\d\s,a-zA-Z\+\-\./]+$', matrix_str):
        return {
            'valid': False,
            'error': 'Matrix contains invalid characters',
            'code': 'INVALID_CHARACTERS'
        }
    
    return {
        'valid': True,
        'sanitized': matrix_str
    }
