from calcora.bootstrap import default_engine


def test_differentiate_sin_x_squared_expands_into_steps():
    engine = default_engine(load_entry_points=False)
    result = engine.run(operation="differentiate", expression="sin(x**2)")

    # Expect multi-step decomposition (at least chain + power).
    rules = [n.rule for n in result.graph.nodes]
    assert "chain_rule_sin" in rules
    assert "power_rule" in rules

    # Final output should be equivalent to 2*x*cos(x**2) (string form may vary in ordering).
    assert "cos(x**2)" in result.output
    assert "2" in result.output
    assert "x" in result.output
