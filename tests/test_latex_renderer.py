"""Test LaTeX renderer functionality."""

from calcora.bootstrap import default_engine
from calcora.renderers.latex_renderer import LatexRenderer


def test_latex_basic_differentiation():
    """Test LaTeX rendering of basic differentiation."""
    engine = default_engine(load_entry_points=True)
    result = engine.run(operation="differentiate", expression="x**2", variable="x")
    
    renderer = LatexRenderer()
    latex_output = renderer.render(result=result, format="latex", verbosity="detailed")
    
    # Check that output contains LaTeX markup
    assert "\\[" in latex_output or "\\section" in latex_output
    assert "Calcora" in latex_output
    print("\n✅ Basic differentiation LaTeX output:")
    print(latex_output)


def test_latex_product_rule():
    """Test LaTeX rendering with product rule."""
    engine = default_engine(load_entry_points=True)
    result = engine.run(operation="differentiate", expression="x*sin(x)", variable="x")
    
    renderer = LatexRenderer()
    latex_output = renderer.render(result=result, format="latex", verbosity="detailed")
    
    assert "\\section" in latex_output
    assert "sin" in latex_output or "\\sin" in latex_output
    print("\n✅ Product rule LaTeX output:")
    print(latex_output)


def test_latex_concise_mode():
    """Test LaTeX rendering in concise mode (result only)."""
    engine = default_engine(load_entry_points=True)
    result = engine.run(operation="differentiate", expression="x**3 + 2*x", variable="x")
    
    renderer = LatexRenderer()
    latex_output = renderer.render(result=result, format="latex", verbosity="concise")
    
    # Concise mode should have result but minimal steps
    assert "\\section*{Result}" in latex_output
    print("\n✅ Concise mode LATeX output:")
    print(latex_output)


def test_latex_teacher_mode():
    """Test LaTeX rendering in teacher mode (full details)."""
    engine = default_engine(load_entry_points=True)
    result = engine.run(operation="differentiate", expression="cos(x**2)", variable="x")
    
    renderer = LatexRenderer()
    latex_output = renderer.render(result=result, format="latex", verbosity="teacher")
    
    # Teacher mode should include metadata
    assert "\\section*{Metadata}" in latex_output or "Metadata" in latex_output
    assert "\\cos" in latex_output or "cos" in latex_output
    print("\n✅ Teacher mode LaTeX output:")
    print(latex_output)


if __name__ == "__main__":
    test_latex_basic_differentiation()
    test_latex_product_rule()
    test_latex_concise_mode()
    test_latex_teacher_mode()
    print("\n🎉 All LaTeX renderer tests passed!")
