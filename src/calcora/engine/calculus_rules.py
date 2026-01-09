"""Decomposed calculus rules for differentiation with pedagogical explanations.

This module provides explicit, auditable calculus rules rather than relying solely
on SymPy's internal differentiation. Each rule explains what it does in human terms.
"""
# type: ignore  # SymPy uses dynamic operator overloading that confuses static analysis

from __future__ import annotations

from typing import Any, Sequence

from ..plugins.decorators import rule
from .models import StepGraph


def _sp():
    try:
        import sympy as sp  # type: ignore[import]

        return sp
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(
            "SymPy is required for the calculus rule engine. Install with: pip install 'calcora[engine-sympy]'"
        ) from e


def _x():
    sp = _sp()
    return sp.Symbol("x")


def _parse(expression: str):
    sp = _sp()
    return sp.sympify(expression)


def _get_derivative_var(expr):
    """Extract the variable from a Derivative expression."""
    sp = _sp()
    if isinstance(expr, sp.Derivative):
        # Get the variable from the derivative
        if expr.variables:
            return expr.variables[0]
    return None


def _is_derivative(expr) -> bool:
    """Check if expr is a Derivative."""
    sp = _sp()
    return isinstance(expr, sp.Derivative)


def _first_derivative(expr):
    """Find the first Derivative node in the expression tree."""
    sp = _sp()
    for node in sp.preorder_traversal(expr):
        if _is_derivative(node):
            return node
    return None


def _rewrite_first_derivative(expr, *, predicate, replacer):
    """Return a rewritten expression, or None if no matching derivative is found."""

    target = None
    for node in _sp().preorder_traversal(expr):
        if _is_derivative(node) and predicate(node):
            target = node
            break

    if target is None:
        return None

    replacement = replacer(target)
    return expr.xreplace({target: replacement})


def _teacher(expl: str, teacher: str) -> dict[str, Any]:
    return {"explanations": {"detailed": expl, "teacher": teacher}}


@rule(
    name="diff_constant",
    operation="differentiate",
    priority=100,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: (
                _get_derivative_var(d) is not None and
                d.expr.free_symbols.isdisjoint({_get_derivative_var(d)})
            ),
            replacer=lambda _d: _sp().Integer(0),
        )
        is not None
    ),
)
def diff_constant(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    
    def predicate(d):
        var = _get_derivative_var(d)
        return var is not None and d.expr.free_symbols.isdisjoint({var})
    
    expl = "Derivative of a constant is 0."
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=predicate,
        replacer=lambda _d: sp.Integer(0),
    )
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "If a term does not depend on the variable, changing it cannot change the term's value, so the rate of change is 0."),
    )


@rule(
    name="expand_higher_order",
    operation="differentiate",
    priority=150,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _first_derivative(_parse(s)) is not None
        and len(_first_derivative(_parse(s)).variables) > 1
    ),
)
def expand_higher_order(expression: str, graph: StepGraph):
    """Expand nth-order derivative by evaluating it (SymPy collapses nested derivatives)."""
    sp = _sp()
    expr = _parse(expression)
    
    target = _first_derivative(expr)
    if target is None or len(target.variables) <= 1:
        return (expression, "Already first-order.", [], {"noop": True})
    
    # Get the order and variable
    var = target.variables[0]
    order = len(target.variables)
    
    # Since SymPy collapses Derivative(Derivative(f,x),x) into Derivative(f,(x,2)),
    # we can't show individual steps. Instead, evaluate the derivative directly.
    result = sp.diff(target.expr, var, order)
    
    # Replace the higher-order derivative with the result
    out_expr = expr.xreplace({target: result})
    
    if order == 2:
        order_name = "second"
        notation = "d²/dx²"
    elif order == 3:
        order_name = "third"
        notation = "d³/dx³"
    elif order == 4:
        order_name = "fourth"
        notation = "d⁴/dx⁴"
    elif order == 5:
        order_name = "fifth"
        notation = "d⁵/dx⁵"
    else:
        order_name = f"{order}th"
        notation = f"d^{order}/dx^{order}"
    
    expl = f"Compute {order_name} derivative: {notation}[{target.expr}]"
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            f"The {order_name} derivative {notation} means differentiating {order} times with respect to {var}. For polynomials, each differentiation reduces the degree by 1 and multiplies by the current power."
        ),
    )


@rule(
    name="diff_identity",
    operation="differentiate",
    priority=100,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr == _get_derivative_var(d),
            replacer=lambda _d: _sp().Integer(1),
        )
        is not None
    ),
)
def diff_identity(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    
    # Get the variable from the derivative
    first_deriv = _first_derivative(expr)
    var = _get_derivative_var(first_deriv) if first_deriv else sp.Symbol('x')
    
    expl = f"Derivative of {var} with respect to {var} is 1."
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr == _get_derivative_var(d),
        replacer=lambda _d: sp.Integer(1),
    )
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "The function f(x)=x increases by 1 for every +1 in x, so its slope is 1."),
    )


@rule(
    name="sum_rule",
    operation="differentiate",
    priority=90,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "Add",
            replacer=lambda d: _sp().Add(*[_sp().Derivative(t, _get_derivative_var(d), evaluate=False) for t in d.expr.args]),
        )
        is not None
    ),
)
def sum_rule(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "Add",
        replacer=lambda d: sp.Add(*[sp.Derivative(t, _get_derivative_var(d), evaluate=False) for t in d.expr.args]),
    )
    expl = "Differentiate term-by-term using linearity: d/dx(f+g)=f'+g'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Linearity means we can differentiate each term separately and then add the results."),
    )


@rule(
    name="constant_multiple",
    operation="differentiate",
    priority=95,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "Mul"
            and any(arg.free_symbols.isdisjoint({_x()}) for arg in d.expr.args),
            replacer=lambda d: (
                _sp().Mul(*[a for a in d.expr.args if a.free_symbols.isdisjoint({_x()})])
                * _sp().Derivative(
                    _sp().Mul(*[a for a in d.expr.args if not a.free_symbols.isdisjoint({_x()})]),
                    _x(),
                    evaluate=False,
                )
            ),
        )
        is not None
    ),
)
def constant_multiple(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    consts: list = []
    vars_: list = []
    def is_const(a):
        return a.free_symbols.isdisjoint({_x()})  # type: ignore[attr-defined]
    d_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "Mul" and any(is_const(arg) for arg in d.expr.args),
        replacer=lambda d: (
            sp.Mul(*[a for a in d.expr.args if is_const(a)])
            * sp.Derivative(sp.Mul(*[a for a in d.expr.args if not is_const(a)]), _get_derivative_var(d), evaluate=False)
        ),
    )
    expl = "Factor out constants: d/dx(c·u)=c·u'."
    return (
        str(d_expr),
        expl,
        [],
        _teacher(expl, "Constants don't change with x, so they factor out of the derivative."),
    )


@rule(
    name="product_rule",
    operation="differentiate",
    priority=80,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "Mul" and len(d.expr.args) >= 2,
            replacer=lambda d: (
                (d.expr.args[0]) * _sp().Derivative(_sp().Mul(*d.expr.args[1:]), _get_derivative_var(d), evaluate=False)
                + (_sp().Mul(*d.expr.args[1:])) * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False)
            ),
        )
        is not None
    ),
)
def product_rule(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "Mul" and len(d.expr.args) >= 2,
        replacer=lambda d: (
            (d.expr.args[0]) * sp.Derivative(sp.Mul(*d.expr.args[1:]), _get_derivative_var(d), evaluate=False)
            + (sp.Mul(*d.expr.args[1:])) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False)
        ),
    )
    expl = "Apply product rule: d/dx(f·g)=f·g' + g·f'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "Think of f·g as one quantity times another. If either changes, the product changes; the product rule accounts for both contributions.",
        ),
    )


@rule(
    name="quotient_rule",
    operation="differentiate",
    priority=80,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "Mul" and any(
                arg.func.__name__ == "Pow" and arg.exp == -1 for arg in d.expr.args
            ),
            replacer=lambda d: None,  # Will be computed in the function
        )
        is not None
        if _parse(s).has(_sp().Derivative)
        else False
    ),
)
def quotient_rule(expression: str, graph: StepGraph):
    """Apply quotient rule for f/g."""
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    
    # Find the derivative node with division
    target = None
    for node in sp.preorder_traversal(expr):
        if _is_dx_derivative(node):
            # Check if it's a division (numerator * denominator^-1)
            if node.expr.func.__name__ == "Mul":
                args = node.expr.args
                # Look for pattern: numerator * (denominator)^-1
                if any(arg.func.__name__ == "Pow" and arg.exp == -1 for arg in args):
                    target = node
                    break
    
    if target is None:
        return (expression, "No quotient found", [], {})
    
    # Extract numerator and denominator
    args = list(target.expr.args)
    denominator_inv = None
    numerator_parts = []
    
    for arg in args:
        if arg.func.__name__ == "Pow" and arg.exp == -1:
            denominator_inv = arg
        else:
            numerator_parts.append(arg)
    
    if denominator_inv is None:
        return (expression, "No denominator found", [], {})
    
    numerator = sp.Mul(*numerator_parts) if numerator_parts else sp.Integer(1)
    denominator = denominator_inv.base
    
    # Apply quotient rule: (f/g)' = (f'g - fg') / g²
    f_prime = sp.Derivative(numerator, _get_derivative_var(d), evaluate=False)
    g_prime = sp.Derivative(denominator, _get_derivative_var(d), evaluate=False)
    
    result = (f_prime * denominator - numerator * g_prime) / (denominator ** 2)
    out_expr = expr.xreplace({target: result})
    
    expl = "Apply quotient rule: d/dx(f/g) = (f'·g - f·g') / g²."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "When dividing functions, use the quotient rule: derivative of numerator times denominator minus numerator times derivative of denominator, all over denominator squared.",
        ),
    )


@rule(
    name="power_rule",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "Pow" and d.expr.exp.free_symbols.isdisjoint({_x()}),
            replacer=lambda d: (
                d.expr.exp
                * (d.expr.base ** (d.expr.exp - 1))
                * _sp().Derivative(d.expr.base, _get_derivative_var(d), evaluate=False)
            ),
        )
        is not None
    ),
)
def power_rule(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "Pow" and d.expr.exp.free_symbols.isdisjoint({_x()}),
        replacer=lambda d: d.expr.exp
        * (d.expr.base ** (d.expr.exp - 1))
        * sp.Derivative(d.expr.base, _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply power rule with chain: d/dx(u^n)=n·u^(n-1)·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "If u depends on x, we differentiate u^n like the usual power rule, then multiply by u' to account for how u changes with x.",
        ),
    )


@rule(
    name="chain_rule_sin",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "sin",
            replacer=lambda d: _sp().cos(d.expr.args[0]) * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
        )
        is not None
    ),
)
def chain_rule_sin(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "sin",
        replacer=lambda d: sp.cos(d.expr.args[0]) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply chain rule: d/dx(sin(u))=cos(u)·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "Outer function: sin(·). Inner function: u. Differentiate the outer (cos) and multiply by the derivative of the inner (u').",
        ),
    )


@rule(
    name="chain_rule_cos",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "cos",
            replacer=lambda d: -_sp().sin(d.expr.args[0]) * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
        )
        is not None
    ),
)
def chain_rule_cos(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "cos",
        replacer=lambda d: -sp.sin(d.expr.args[0]) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply chain rule: d/dx(cos(u))=-sin(u)·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Differentiate the outer (cos→-sin) and multiply by the inner derivative."),
    )


@rule(
    name="chain_rule_tan",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "tan",
            replacer=lambda d: (_sp().sec(d.expr.args[0]) ** 2)
            * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
        )
        is not None
    ),
)
def chain_rule_tan(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "tan",
        replacer=lambda d: (sp.sec(d.expr.args[0]) ** 2) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply chain rule: d/dx(tan(u))=sec(u)^2·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Derivative of tan is sec^2; multiply by the inner derivative."),
    )


@rule(
    name="chain_rule_sec",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "sec",
            replacer=lambda d: _sp().sec(d.expr.args[0])
            * _sp().tan(d.expr.args[0])
            * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
        )
        is not None
    ),
)
def chain_rule_sec(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "sec",
        replacer=lambda d: sp.sec(d.expr.args[0]) * sp.tan(d.expr.args[0]) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply chain rule: d/dx(sec(u))=sec(u)·tan(u)·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Derivative of sec is sec·tan; multiply by the inner derivative."),
    )


@rule(
    name="chain_rule_csc",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "csc",
            replacer=lambda d: -_sp().csc(d.expr.args[0])
            * _sp().cot(d.expr.args[0])
            * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
        )
        is not None
    ),
)
def chain_rule_csc(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "csc",
        replacer=lambda d: -sp.csc(d.expr.args[0]) * sp.cot(d.expr.args[0]) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply chain rule: d/dx(csc(u))=-csc(u)·cot(u)·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Derivative of csc is -csc·cot; multiply by the inner derivative."),
    )


@rule(
    name="chain_rule_cot",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "cot",
            replacer=lambda d: -(_sp().csc(d.expr.args[0]) ** 2)
            * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
        )
        is not None
    ),
)
def chain_rule_cot(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "cot",
        replacer=lambda d: -(sp.csc(d.expr.args[0]) ** 2) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply chain rule: d/dx(cot(u))=-csc(u)^2·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Derivative of cot is -csc^2; multiply by the inner derivative."),
    )


@rule(
    name="chain_rule_exp",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "exp",
            replacer=lambda d: _sp().exp(d.expr.args[0]) * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
        )
        is not None
    ),
)
def chain_rule_exp(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "exp",
        replacer=lambda d: sp.exp(d.expr.args[0]) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply chain rule: d/dx(e^u)=e^u·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "The derivative of e^u is itself times the inner derivative."),
    )


@rule(
    name="chain_rule_log",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "log",
            replacer=lambda d: _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / d.expr.args[0],
        )
        is not None
    ),
)
def chain_rule_log(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "log",
        replacer=lambda d: sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / d.expr.args[0],
    )
    expl = "Apply chain rule: d/dx(ln(u))=u'/u."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Differentiate log by dividing the inner derivative by the inner function."),
    )


@rule(
    name="chain_rule_asin",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "asin",
            replacer=lambda d: _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False)
            / _sp().sqrt(1 - d.expr.args[0] ** 2),
        )
        is not None
    ),
)
def chain_rule_asin(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "asin",
        replacer=lambda d: sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / sp.sqrt(1 - d.expr.args[0] ** 2),
    )
    expl = "Apply chain rule: d/dx(arcsin(u))=u'/sqrt(1-u^2)."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Derivative of arcsin uses 1/sqrt(1-u^2); include inner derivative."),
    )


@rule(
    name="chain_rule_acos",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "acos",
            replacer=lambda d: -_sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False)
            / _sp().sqrt(1 - d.expr.args[0] ** 2),
        )
        is not None
    ),
)
def chain_rule_acos(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "acos",
        replacer=lambda d: -sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / sp.sqrt(1 - d.expr.args[0] ** 2),
    )
    expl = "Apply chain rule: d/dx(arccos(u))=-u'/sqrt(1-u^2)."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Derivative of arccos is -1/sqrt(1-u^2); include inner derivative."),
    )


@rule(    name="chain_rule_sinh",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "sinh",
            replacer=lambda d: _sp().cosh(d.expr.args[0]) * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
        )
        is not None
    ),
)
def chain_rule_sinh(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "sinh",
        replacer=lambda d: sp.cosh(d.expr.args[0]) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply chain rule: d/dx(sinh(u))=cosh(u)·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Hyperbolic sine differentiates to hyperbolic cosine times the inner derivative."),
    )


@rule(
    name="chain_rule_cosh",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "cosh",
            replacer=lambda d: _sp().sinh(d.expr.args[0]) * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
        )
        is not None
    ),
)
def chain_rule_cosh(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "cosh",
        replacer=lambda d: sp.sinh(d.expr.args[0]) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply chain rule: d/dx(cosh(u))=sinh(u)·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Hyperbolic cosine differentiates to hyperbolic sine times the inner derivative."),
    )


@rule(
    name="chain_rule_tanh",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "tanh",
            replacer=lambda d: (1 / _sp().cosh(d.expr.args[0]) ** 2) * _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
        )
        is not None
    ),
)
def chain_rule_tanh(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "tanh",
        replacer=lambda d: (1 / sp.cosh(d.expr.args[0]) ** 2) * sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False),
    )
    expl = "Apply chain rule: d/dx(tanh(u))=sech²(u)·u'."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Hyperbolic tangent differentiates to hyperbolic secant squared times the inner derivative."),
    )


@rule(
    name="chain_rule_asinh",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "asinh",
            replacer=lambda d: _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / _sp().sqrt(d.expr.args[0] ** 2 + 1),
        )
        is not None
    ),
)
def chain_rule_asinh(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "asinh",
        replacer=lambda d: sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / sp.sqrt(d.expr.args[0] ** 2 + 1),
    )
    expl = "Apply chain rule: d/dx(asinh(u))=u'/sqrt(u²+1)."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Inverse hyperbolic sine differentiates to u' over sqrt(u²+1)."),
    )


@rule(
    name="chain_rule_acosh",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "acosh",
            replacer=lambda d: _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / _sp().sqrt(d.expr.args[0] ** 2 - 1),
        )
        is not None
    ),
)
def chain_rule_acosh(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "acosh",
        replacer=lambda d: sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / sp.sqrt(d.expr.args[0] ** 2 - 1),
    )
    expl = "Apply chain rule: d/dx(acosh(u))=u'/sqrt(u²-1)."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Inverse hyperbolic cosine differentiates to u' over sqrt(u²-1)."),
    )


@rule(
    name="chain_rule_atanh",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "atanh",
            replacer=lambda d: _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / (1 - d.expr.args[0] ** 2),
        )
        is not None
    ),
)
def chain_rule_atanh(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "atanh",
        replacer=lambda d: sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / (1 - d.expr.args[0] ** 2),
    )
    expl = "Apply chain rule: d/dx(atanh(u))=u'/(1-u²)."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Inverse hyperbolic tangent differentiates to u' over (1-u²)."),
    )


@rule(    name="chain_rule_atan",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "atan",
            replacer=lambda d: _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False)
            / (1 + d.expr.args[0] ** 2),
        )
        is not None
    ),
)
def chain_rule_atan(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "atan",
        replacer=lambda d: sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / (1 + d.expr.args[0] ** 2),
    )
    expl = "Apply chain rule: d/dx(arctan(u))=u'/(1+u^2)."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Derivative of arctan uses 1/(1+u^2); include inner derivative."),
    )


@rule(
    name="chain_rule_asec",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "asec",
            replacer=lambda d: _sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False)
            / (_sp().Abs(d.expr.args[0]) * _sp().sqrt(d.expr.args[0] ** 2 - 1)),
        )
        is not None
    ),
)
def chain_rule_asec(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "asec",
        replacer=lambda d: sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False)
        / (sp.Abs(d.expr.args[0]) * sp.sqrt(d.expr.args[0] ** 2 - 1)),
    )
    expl = "Apply chain rule: d/dx(arcsec(u))=u'/(|u|·√(u²-1))."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Inverse secant differentiates to u' over (absolute value of u times sqrt(u²-1))."),
    )


@rule(
    name="chain_rule_acsc",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "acsc",
            replacer=lambda d: -_sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False)
            / (_sp().Abs(d.expr.args[0]) * _sp().sqrt(d.expr.args[0] ** 2 - 1)),
        )
        is not None
    ),
)
def chain_rule_acsc(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "acsc",
        replacer=lambda d: -sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False)
        / (sp.Abs(d.expr.args[0]) * sp.sqrt(d.expr.args[0] ** 2 - 1)),
    )
    expl = "Apply chain rule: d/dx(arccsc(u))=-u'/(|u|·√(u²-1))."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Inverse cosecant differentiates to negative u' over (absolute value of u times sqrt(u²-1))."),
    )


@rule(
    name="chain_rule_acot",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: d.expr.func.__name__ == "acot",
            replacer=lambda d: -_sp().Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / (1 + d.expr.args[0] ** 2),
        )
        is not None
    ),
)
def chain_rule_acot(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: d.expr.func.__name__ == "acot",
        replacer=lambda d: -sp.Derivative(d.expr.args[0], _get_derivative_var(d), evaluate=False) / (1 + d.expr.args[0] ** 2),
    )
    expl = "Apply chain rule: d/dx(arccot(u))=-u'/(1+u²)."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(expl, "Inverse cotangent differentiates to negative u' over (1+u²)."),
    )


@rule(
    name="logarithmic_differentiation",
    operation="differentiate",
    priority=80,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: (
        _rewrite_first_derivative(
            _parse(s),
            predicate=lambda d: (
                d.expr.func.__name__ == "Pow"
                and not d.expr.base.free_symbols.isdisjoint({_x()})
                and not d.expr.exp.free_symbols.isdisjoint({_x()})
            ),
            replacer=lambda d: d.expr * (
                _sp().log(d.expr.base) * _sp().Derivative(d.expr.exp, _get_derivative_var(d), evaluate=False)
                + (d.expr.exp / d.expr.base) * _sp().Derivative(d.expr.base, _get_derivative_var(d), evaluate=False)
            ),
        )
        is not None
    ),
)
def logarithmic_differentiation(expression: str, graph: StepGraph):
    """Differentiate u(x)^v(x) using logarithmic differentiation.
    
    For y = u^v where both u and v depend on x:
    ln(y) = v*ln(u)
    (1/y)*dy/dx = ln(u)*dv/dx + (v/u)*du/dx
    dy/dx = y * [ln(u)*dv/dx + (v/u)*du/dx]
    """
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda d: (
            d.expr.func.__name__ == "Pow"
            and not d.expr.base.free_symbols.isdisjoint({x})
            and not d.expr.exp.free_symbols.isdisjoint({x})
        ),
        replacer=lambda d: d.expr * (
            sp.log(d.expr.base) * sp.Derivative(d.expr.exp, _get_derivative_var(d), evaluate=False)
            + (d.expr.exp / d.expr.base) * sp.Derivative(d.expr.base, _get_derivative_var(d), evaluate=False)
        ),
    )
    expl = "Apply logarithmic differentiation: d/dx(u^v) = u^v·[ln(u)·v' + (v/u)·u']."
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "When both base and exponent depend on x, use logarithmic differentiation: take ln of both sides, differentiate, then solve for dy/dx.",
        ),
    )


# Special functions
@rule(
    name="chain_rule_erf",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: _parse(s).find(lambda n: isinstance(n, _sp().erf)) and _parse(s).has(_sp().Derivative),
)
def chain_rule_erf(expression: str, graph: StepGraph):
    """Derivative of erf(u): d/dx[erf(u)] = (2/√π) * exp(-u²) * u'"""
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    
    def predicate(d):
        return any(isinstance(n, sp.erf) for n in sp.preorder_traversal(d.expr))
    
    def replacer(d):
        target_erf = None
        for node in sp.preorder_traversal(d.expr):
            if isinstance(node, sp.erf):
                target_erf = node
                break
        if target_erf is None:
            return d
        u = target_erf.args[0]
        u_prime = sp.diff(u, x)
        # d/dx[erf(u)] = (2/√π) * exp(-u²) * u'
        result = (2 / sp.sqrt(sp.pi)) * sp.exp(-u**2) * u_prime
        return d.expr.xreplace({target_erf: result})
    
    out_expr = _rewrite_first_derivative(expr, predicate=predicate, replacer=replacer)
    expl = "Apply chain rule to error function: d/dx[erf(u)] = (2/√π)·exp(-u²)·u'"
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "The error function erf(u) is the Gaussian distribution integral. Its derivative follows from the fundamental theorem of calculus: d/dx[erf(u)] = (2/√π)·exp(-u²)·du/dx."
        ),
    )


@rule(
    name="chain_rule_gamma",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: _parse(s).find(lambda n: isinstance(n, _sp().gamma)) and _parse(s).has(_sp().Derivative),
)
def chain_rule_gamma(expression: str, graph: StepGraph):
    """Derivative of gamma(u): d/dx[gamma(u)] = gamma(u) * polygamma(0, u) * u'"""
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    
    def predicate(d):
        return any(isinstance(n, sp.gamma) for n in sp.preorder_traversal(d.expr))
    
    def replacer(d):
        target_gamma = None
        for node in sp.preorder_traversal(d.expr):
            if isinstance(node, sp.gamma):
                target_gamma = node
                break
        if target_gamma is None:
            return d
        u = target_gamma.args[0]
        u_prime = sp.diff(u, x)
        # d/dx[gamma(u)] = gamma(u) * digamma(u) * u'
        result = target_gamma * sp.polygamma(0, u) * u_prime
        return d.expr.xreplace({target_gamma: result})
    
    out_expr = _rewrite_first_derivative(expr, predicate=predicate, replacer=replacer)
    expl = "Apply chain rule to gamma function: d/dx[Γ(u)] = Γ(u)·ψ(u)·u' where ψ is the digamma function"
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "The gamma function Γ(u) generalizes factorials. Its derivative is Γ(u)·ψ(u)·du/dx where ψ (psi) is the digamma function, the logarithmic derivative of gamma."
        ),
    )


@rule(
    name="chain_rule_heaviside",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: _parse(s).find(lambda n: isinstance(n, _sp().Heaviside)) and _parse(s).has(_sp().Derivative),
)
def chain_rule_heaviside(expression: str, graph: StepGraph):
    """Derivative of Heaviside(u): d/dx[H(u)] = δ(u)·u' where δ is the Dirac delta"""
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    
    def predicate(d):
        return any(isinstance(n, sp.Heaviside) for n in sp.preorder_traversal(d.expr))
    
    def replacer(d):
        target_h = None
        for node in sp.preorder_traversal(d.expr):
            if isinstance(node, sp.Heaviside):
                target_h = node
                break
        if target_h is None:
            return d
        u = target_h.args[0]
        u_prime = sp.diff(u, x)
        # d/dx[H(u)] = δ(u) * u'
        result = sp.DiracDelta(u) * u_prime
        return d.expr.xreplace({target_h: result})
    
    out_expr = _rewrite_first_derivative(expr, predicate=predicate, replacer=replacer)
    expl = "Apply chain rule to Heaviside step function: d/dx[H(u)] = δ(u)·u' where δ is the Dirac delta"
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "The Heaviside function H(u) is 0 for u<0 and 1 for u>0. Its derivative is the Dirac delta δ(u), a generalized function representing an infinitely sharp spike at u=0."
        ),
    )


@rule(
    name="chain_rule_abs",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: _parse(s).find(lambda n: isinstance(n, _sp().Abs)) and _parse(s).has(_sp().Derivative),
)
def chain_rule_abs(expression: str, graph: StepGraph):
    """Derivative of |u|: d/dx[|u|] = sign(u)·u'"""
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    
    def predicate(d):
        return any(isinstance(n, sp.Abs) for n in sp.preorder_traversal(d.expr))
    
    def replacer(d):
        target_abs = None
        for node in sp.preorder_traversal(d.expr):
            if isinstance(node, sp.Abs):
                target_abs = node
                break
        if target_abs is None:
            return d
        u = target_abs.args[0]
        u_prime = sp.diff(u, x)
        # d/dx[|u|] = sign(u) * u'
        result = sp.sign(u) * u_prime
        return d.expr.xreplace({target_abs: result})
    
    out_expr = _rewrite_first_derivative(expr, predicate=predicate, replacer=replacer)
    expl = "Apply chain rule to absolute value: d/dx[|u|] = sign(u)·u'"
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "The absolute value function |u| has derivative sign(u)·du/dx, where sign(u) = u/|u| for u≠0. Note that |u| is not differentiable at u=0."
        ),
    )


@rule(
    name="chain_rule_floor",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: _parse(s).find(lambda n: isinstance(n, _sp().floor)) and _parse(s).has(_sp().Derivative),
)
def chain_rule_floor(expression: str, graph: StepGraph):
    """Derivative of floor(u): floor is not differentiable except at non-integer points where it's 0"""
    sp = _sp()
    expr = _parse(expression)
    
    def predicate(d):
        return any(isinstance(n, sp.floor) for n in sp.preorder_traversal(d.expr))
    
    def replacer(d):
        target_floor = None
        for node in sp.preorder_traversal(d.expr):
            if isinstance(node, sp.floor):
                target_floor = node
                break
        if target_floor is None:
            return d
        # floor function has derivative 0 almost everywhere (except at integer points where it's undefined)
        return d.expr.xreplace({target_floor: sp.Integer(0)})
    
    out_expr = _rewrite_first_derivative(expr, predicate=predicate, replacer=replacer)
    expl = "Derivative of floor function: d/dx[⌊u⌋] = 0 (except at integers where undefined)"
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "The floor function ⌊u⌋ is a step function that's constant between integers. At non-integer points, its derivative is 0. At integer values of u, the derivative is undefined (the function has a jump discontinuity)."
        ),
    )


@rule(
    name="chain_rule_ceiling",
    operation="differentiate",
    priority=85,
    domains=("calculus",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: _parse(s).find(lambda n: isinstance(n, _sp().ceiling)) and _parse(s).has(_sp().Derivative),
)
def chain_rule_ceiling(expression: str, graph: StepGraph):
    """Derivative of ceiling(u): ceiling is not differentiable except at non-integer points where it's 0"""
    sp = _sp()
    expr = _parse(expression)
    
    def predicate(d):
        return any(isinstance(n, sp.ceiling) for n in sp.preorder_traversal(d.expr))
    
    def replacer(d):
        target_ceil = None
        for node in sp.preorder_traversal(d.expr):
            if isinstance(node, sp.ceiling):
                target_ceil = node
                break
        if target_ceil is None:
            return d
        # ceiling function has derivative 0 almost everywhere (except at integer points where it's undefined)
        return d.expr.xreplace({target_ceil: sp.Integer(0)})
    
    out_expr = _rewrite_first_derivative(expr, predicate=predicate, replacer=replacer)
    expl = "Derivative of ceiling function: d/dx[⌈u⌉] = 0 (except at integers where undefined)"
    return (
        str(out_expr),
        expl,
        [],
        _teacher(
            expl,
            "The ceiling function ⌈u⌉ rounds up to the nearest integer. Like floor, it's piecewise constant, so its derivative is 0 at non-integer points and undefined at integer jumps."
        ),
    )


@rule(
    name="evaluate_derivative_fallback",
    operation="differentiate",
    priority=-50,
    domains=("calculus",),
    plugin_name="calcora-engine-sympy",
    plugin_version="0.1.0",
    matches=lambda s: _parse(s).has(_sp().Derivative),
)
def evaluate_derivative_fallback(expression: str, graph: StepGraph):
    sp = _sp()
    expr = _parse(expression)
    x = _x()
    out_expr = _rewrite_first_derivative(
        expr,
        predicate=lambda _d: True,
        replacer=lambda d: sp.diff(d.expr, x),
    )
    expl = "Fallback: evaluate derivative (backend)."
    return (
        str(out_expr),
        expl,
        [],
        {"backend": "sympy", "explanations": {"detailed": expl, "teacher": expl}},
    )


@rule(
    name="simplify",
    operation="differentiate",
    priority=-200,
    domains=("calculus",),
    plugin_name="calcora-engine-sympy",
    plugin_version="0.1.0",
    matches=lambda s: not _parse(s).has(_sp().Derivative),
)
def simplify(expression: str, graph: StepGraph):
    sp = _sp()
    parsed = _parse(expression)
    
    # Try trigonometric simplification first
    trig_simplified = sp.trigsimp(parsed)
    if trig_simplified != parsed:
        expl = "Apply trigonometric identities to simplify."
        return (
            str(trig_simplified),
            expl,
            [],
            {"backend": "sympy", "explanations": {"detailed": expl, "teacher": "Use identities like sin²+cos²=1, double angle formulas, etc."}},
        )
    
    # Try general simplification
    simplified = sp.simplify(parsed)
    if simplified == parsed:
        # Return same expression; the engine will stop if no other rule matches.
        return (expression, "No further simplification.", [], {"noop": True})
    expl = "Simplify algebraically."
    return (
        str(simplified),
        expl,
        [],
        {"backend": "sympy", "explanations": {"detailed": expl, "teacher": "We simplify the expression to a standard, cleaner form."}},
    )


BUILTIN_DIFFERENTIATION_RULES: Sequence[Any] = (
    expand_higher_order,
    diff_constant,
    diff_identity,
    sum_rule,
    constant_multiple,
    quotient_rule,
    power_rule,
    product_rule,
    logarithmic_differentiation,
    # Trig and exponential/log chain rules
    chain_rule_sin,
    chain_rule_cos,
    chain_rule_tan,
    chain_rule_sec,
    chain_rule_csc,
    chain_rule_cot,
    chain_rule_exp,
    chain_rule_log,
    chain_rule_asin,
    chain_rule_acos,
    chain_rule_atan,
    chain_rule_asec,
    chain_rule_acsc,
    chain_rule_acot,
    # Hyperbolic functions
    chain_rule_sinh,
    chain_rule_cosh,
    chain_rule_tanh,
    chain_rule_asinh,
    chain_rule_acosh,
    chain_rule_atanh,
    # Special functions
    chain_rule_erf,
    chain_rule_gamma,
    chain_rule_heaviside,
    chain_rule_abs,
    chain_rule_floor,
    chain_rule_ceiling,
    # Fallbacks
    evaluate_derivative_fallback,
    simplify,
)


# Algebraic manipulation operations
@rule(
    name="expand_expression",
    operation="expand",
    priority=100,
    domains=("algebra",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: True,
)
def expand_expression(expression: str, graph: StepGraph):
    """Expand algebraic expressions."""
    sp = _sp()
    parsed = _parse(expression)
    expanded = sp.expand(parsed)
    
    if expanded == parsed:
        return (expression, "Expression is already expanded.", [], {"noop": True})
    
    expl = "Expand using distributive law: multiply out products and powers."
    return (
        str(expanded),
        expl,
        [],
        _teacher(expl, "Expanding means writing (a+b)² as a²+2ab+b², distributing multiplication over addition."),
    )


@rule(
    name="factor_expression",
    operation="factor",
    priority=100,
    domains=("algebra",),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: True,
)
def factor_expression(expression: str, graph: StepGraph):
    """Factor algebraic expressions."""
    sp = _sp()
    parsed = _parse(expression)
    factored = sp.factor(parsed)
    
    if factored == parsed:
        return (expression, "Expression cannot be factored further.", [], {"noop": True})
    
    expl = "Factor by extracting common terms and recognizing patterns."
    return (
        str(factored),
        expl,
        [],
        _teacher(expl, "Factoring means writing x²+5x+6 as (x+2)(x+3), finding common factors and grouping."),
    )


@rule(
    name="simplify_trig",
    operation="simplify",
    priority=100,
    domains=("algebra", "trigonometry"),
    plugin_name="calcora-engine-core",
    plugin_version="0.1.0",
    matches=lambda s: True,
)
def simplify_trig(expression: str, graph: StepGraph):
    """Simplify expressions using trigonometric identities."""
    sp = _sp()
    parsed = _parse(expression)
    
    # Try trigonometric simplification
    trig_simplified = sp.trigsimp(parsed)
    if trig_simplified != parsed:
        expl = "Apply trigonometric identities (sin²+cos²=1, double angles, etc.)."
        return (
            str(trig_simplified),
            expl,
            [],
            _teacher(expl, "Use fundamental trig identities to combine or reduce trigonometric expressions."),
        )
    
    # Try general simplification
    simplified = sp.simplify(parsed)
    if simplified != parsed:
        expl = "Simplify algebraically."
        return (
            str(simplified),
            expl,
            [],
            _teacher(expl, "Combine like terms, cancel common factors, and reduce to simpler form."),
        )
    
    return (expression, "Expression is already simplified.", [], {"noop": True})


BUILTIN_ALGEBRA_RULES: Sequence[Any] = (
    expand_expression,
    factor_expression,
    simplify_trig,
)


