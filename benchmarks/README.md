# Calcora Benchmarks

This directory contains validation benchmarks for Calcora's computational engines.

## Integration Engine Validation

**`validate_integration.py`** - Compares Calcora integration results against SymPy (ground truth) for 25+ standard Calculus II problems.

### Running Benchmarks

```bash
# From project root
python benchmarks/validate_integration.py
```

### What's Tested

- **Polynomials**: Power rule, polynomial combinations
- **Trigonometric**: sin, cos, tan, sec², cos²
- **Exponential/Logarithmic**: e^x, ln(x), 1/x
- **Rational Functions**: Partial fractions, arctan patterns
- **Square Roots**: √x, 1/√x, products
- **Inverse Trigonometric**: arcsin, arctan patterns
- **Hyperbolic**: sinh, cosh
- **Integration by Parts**: x·e^x, x·sin(x), x·ln(x)
- **U-Substitution**: Chain rule patterns

### Validation Methodology

1. **Ground Truth**: SymPy symbolic integration (peer-reviewed, 15+ year track record)
2. **Comparison**: Symbolic equality check (handles constant of integration)
3. **Metrics**: Correctness (%), average computation time (ms), technique coverage

### Expected Results

- **Accuracy**: ≥95% match with SymPy on standard curriculum
- **Performance**: <100ms average for Calculus II problems
- **Coverage**: 10+ techniques across 8 categories

### Academic Use

This benchmark dataset can be cited when evaluating Calcora for classroom adoption:
- Provides objective validation against established CAS
- Documents algorithm correctness for standard textbook problems
- Enables reproducible testing for research transparency
