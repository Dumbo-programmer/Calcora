# type: ignore  # SymPy expressions use operator overloading
from __future__ import annotations

import sympy as sp

from calcora.bootstrap import default_engine


engine = default_engine(load_entry_points=False)


def run(expr: str) -> sp.Expr:
    res = engine.run(operation="differentiate", expression=expr)
    return sp.sympify(res.output)


def sym(expr: str) -> sp.Expr:
    x = sp.Symbol("x")
    return sp.diff(sp.sympify(expr), x)


def test_exp_chain():
    assert sp.simplify(run("exp(x**2)") - sym("exp(x**2)")) == 0


def test_log_chain():
    # ln(x**2) derivative is 2/x on principal branch
    assert sp.simplify(run("log(x**2)") - sym("log(x**2)")) == 0


def test_cos():
    assert sp.simplify(run("cos(x)") - sym("cos(x)")) == 0


def test_tan_chain():
    assert sp.simplify(run("tan(x**2)") - sym("tan(x**2)")) == 0


def test_sec_csc_cot():
    assert sp.simplify(run("sec(x)") - sym("sec(x)")) == 0
    assert sp.simplify(run("csc(x)") - sym("csc(x)")) == 0
    assert sp.simplify(run("cot(x)") - sym("cot(x)")) == 0


def test_inverse_trig():
    assert sp.simplify(run("asin(x)") - sym("asin(x)")) == 0
    assert sp.simplify(run("acos(x)") - sym("acos(x)")) == 0
    assert sp.simplify(run("atan(x)") - sym("atan(x)")) == 0


def test_constant_multiple():
    assert sp.simplify(run("3*x**2") - sym("3*x**2")) == 0
