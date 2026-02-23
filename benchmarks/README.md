# Calcora Benchmarks

This directory contains validation benchmarks for Calcora's computational engines.

## Integration Engine Validation

**Purpose**: Verify Calcora's integration results against SymPy (symbolic mathematics ground truth)

**Status**: 26/26 tests passing (100% accuracy)  
**Last Validated**: February 24, 2026

---

## Reproducibility

### Environment
- **Python**: 3.13.7
- **SymPy**: 1.14.0
- **NumPy**: 1.26+ (see requirements.txt)
- **OS**: Windows 11 (also tested on Linux)

### Running Benchmarks

```bash
# From project root
python benchmarks/validate_integration.py

# Save results with timestamp
python benchmarks/validate_integration.py > benchmarks/results_$(date +%Y-%m-%d).txt
```

### Committed Results
- `results_2026-02-24_post_timeout.txt` - After timeout protection (26/26, ~15ms avg)
- `results_2026-02-22.txt` - Initial validation (26/26, ~13ms avg)

Results are version-controlled for reproducibility verification.

---

## What's Tested

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

1. **Ground Truth**: SymPy symbolic integration (peer-reviewed CAS, 15+ year track record)
2. **Comparison**: Symbolic equality check after normalizing constant of integration
3. **Metrics**: Correctness (%), average computation time (ms), technique coverage
4. **Independence**: Calcora and SymPy use separate code paths (no shared algorithms)

### Comparison Logic
```python
# Strip "+ C" from Calcora output
calcora_clean = calcora_str.replace(' + C', '')

# Parse both and compute symbolic difference
diff = sp.simplify(calcora_sympy - sympy_result)
## Academic Use

This benchmark dataset provides objective validation for classroom adoption evaluation:

- **Reproducible Testing**: Version-controlled environment and results
- **Independent Verification**: Ground truth from established CAS (SymPy)
- **Scope Documentation**: Honest coverage limitations
- **Standard Curriculum**: Problems from Stewart, Thomas, Anton textbooks

**Suitable For**: Calculus I/II coursework (educational use)  
**Not Suitable For**: Research computing, peer-reviewed publications

### Citation

When evaluating Calcora for academic use, reference:
- Benchmark accuracy: 26/26 (100%)
- Environment: Python 3.13.7, SymPy 1.14.0
- Results files: `benchmarks/results_*.txt`
- Validation date: February 24, 2026

---

## Maintenance

### Before Each Release
1. Run full benchmark suite
2. Commit results with timestamp
3. Update this README with results
4. Document any environment changes

### Versioning
Results are timestamped (`YYYY-MM-DD`) and version-controlled for regression detection.

**Last Updated**: February 24, 2026

### Current Results (v0.2.0)

**By Category**:
- Polynomials: 3/3 passed (100%), ~57ms avg
- Trigonometric: 5/5 passed (100%), ~5ms avg
- Exponential: 3/3 passed (100%), ~8ms avg
- Rational: 3/3 passed (100%), ~15ms avg
- Radicals: 3/3 passed (100%), ~3ms avg
- Inverse Trig: 2/2 passed (100%), ~22ms avg
- Hyperbolic: 2/2 passed (100%), ~11ms avg
- By Parts: 3/3 passed (100%), ~22ms avg
- Substitution: 2/2 passed (100%), ~14ms avg

**Overall**: 26/26 passed (100%), ~15ms average

### Known Limitations

**Not Covered by Benchmarks**:
- Trigonometric substitution (not implemented)
- Reduction formulas (not implemented)
- Improper integrals (infinite limits)
- Non-elementary integrals (elliptic functions, etc.)

Benchmarks validate **implemented techniques only** (~80% of standard Calculus II textbook problems).

---

## Academic Use

This benchmark dataset can be cited when evaluating Calcora for classroom adoption:
- Provides objective validation against established CAS
- Documents algorithm correctness for standard textbook problems
- Enables reproducible testing for research transparency
