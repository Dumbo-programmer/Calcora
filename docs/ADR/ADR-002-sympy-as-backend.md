# ADR-002: Use SymPy as Symbolic Backend

**Status:** Accepted  
**Date:** 2026-01-10  
**Decision-makers:** Calcora Core Team

---

## Context

Calcora needs a **symbolic computation backend** to:
- Parse mathematical expressions (`"x**2 + sin(x)"` → AST)
- Perform symbolic integration, differentiation
- Simplify expressions (`2*x + 3*x` → `5*x`)
- Validate mathematical correctness

### Requirements

1. **Peer-reviewed accuracy** (for academic credibility)
2. **Open-source** (for transparency)
3. **Python-native** (no C++ bindings that complicate deployment)
4. **Well-documented** (for contributors to learn)
5. **Actively maintained** (security updates, bug fixes)

---

## Decision

**Use [SymPy](https://github.com/sympy/sympy) as the symbolic computation backend.**

**Integration Points:**
```python
import sympy as sp

# Expression parsing
expr = sp.sympify("x**2 + sin(x)")

# Symbolic integration
antiderivative = sp.integrate(expr, x)

# Simplification
simplified = sp.simplify(expr)

# Numerical evaluation
value = expr.evalf(subs={x: 2.0})
```

**Rationale:**
- SymPy is peer-reviewed (Meurer et al., 2017, PeerJ Computer Science)
- 100% Python (no compilation required)
- 15+ years of development (stable, mature)
- Used by academic institutions worldwide
- MIT license (compatible with Calcora)

---

## Alternatives Considered

### Alternative 1: Mathematica/Wolfram Engine

**Pros:**
- Industry standard for symbolic computation
- Extremely powerful (handles obscure edge cases)
- Used in research publications

**Cons:**
- **Proprietary license** ($140/year for students, $295+ for professionals)
- Not open-source (violates transparency requirement)
- Requires external installation (deployment complexity)
- **Rejected:** Cost and closed-source nature incompatible with academic adoption goals

### Alternative 2: SageMath

**Pros:**
- Very powerful (built on SymPy, Maxima, GAP, PARI/GP)
- Free and open-source
- Designed for mathematics education/research

**Cons:**
- **Heavyweight** (1.5GB+ download, includes entire SageMath distribution)
- Difficult to embed (separate Python environment)
- Deployment complexity (Docker recommended)
- Overkill for Calculus I/II scope
- **Rejected:** Too heavy for a focused Calculus tool

### Alternative 3: Custom CAS Implementation

**Pros:**
- Complete control over algorithms
- Optimized for Calculus I/II specifically
- Educational value in implementing algorithms

**Cons:**
- **Months of work** to match SymPy's basic functionality
- Not peer-reviewed (zero academic credibility)
- Reinventing the wheel (SymPy already does this well)
- High bug risk (integration is mathematically complex)
- **Rejected:** Not feasible for v0.2 timeline, questionable value

### Alternative 4: Maxima (via PyMaxima)

**Pros:**
- Mature CAS (40+ years old)
- Strong integration capabilities
- Free and open-source

**Cons:**
- Lisp-based (Python wrapper is thin abstraction)
- Less Pythonic API (harder for contributors)
- Smaller Python community than SymPy
- **Rejected:** SymPy has better Python integration and documentation

---

## Consequences

### Positive

✅ **Academic Credibility**
- SymPy cited in 1000+ academic papers
- Peer-reviewed publication (Meurer et al., 2017)
- Validates Calcora results against established CAS

✅ **Rapid Development**
- Don't need to implement basic symbolic algorithms
- Focus effort on step-by-step **explanation** (Calcora's differentiator)
- Integration, differentiation, simplification "just work"

✅ **Cross-Verification**
- Benchmark validation compares Calcora vs SymPy
- If SymPy gets it right, Calcora (using SymPy) should too

✅ **Python-Native**
- No compilation step
- Works on Windows, macOS, Linux
- Easy `pip install`

✅ **Community Support**
- Active development (commits daily)
- Extensive documentation
- Large user base (easy to find Stack Overflow answers)

### Negative

❌ **Dependency on External Library**
- If SymPy introduces breaking changes, Calcora breaks
- **Mitigation:** Pin SymPy version in `pyproject.toml`, test before upgrading

❌ **SymPy Performance Limitations**
- Pure Python (slower than Mathematica's C++ core)
- Large expressions (>100 terms) can be slow
- **Mitigation:** Document performance limits, use numeric fallback

❌ **SymPy Quirks Leak Through**
- SymPy's expression format appears in Calcora output
- Example: `exp(x)` instead of `e^x` in some cases
- **Mitigation:** Add rendering layer to normalize output (v0.3)

❌ **Not Always Optimal**
- SymPy may choose different integration path than textbook
- Example: Textbook uses u-sub, SymPy uses pattern matching
- **Mitigation:** Calcora detects technique **before** calling SymPy, controls narrative

### Neutral

⚪ **License Compatibility**
- SymPy: BSD-3-Clause
- Calcora: MIT
- Both permissive, no conflict

⚪ **Installation Size**
- SymPy adds ~50MB to installation
- Acceptable for desktop/server, manageable for web deployment

---

## Design Decisions Based on This ADR

1. **SymPy is a black box** — Calcora doesn't modify SymPy's algorithms
2. **Calcora adds value through explanation** — SymPy computes, Calcora explains *why*
3. **Technique detection happens in Calcora** — We decide which technique to apply, SymPy validates
4. **Fallback to SymPy** — If Calcora's technique fails, use `sp.integrate()` as safety net

## Implementation Details

### Expression Parsing
```python
try:
    expr = sp.sympify(expression)
except sp.SympifyError as e:
    return {"success": False, "error": f"Invalid syntax: {e}"}
```

### Integration Workflow
```python
# 1. Parse expression
expr = sp.sympify("x * exp(x)")

# 2. Detect technique (Calcora logic)
technique = self._detect_technique(expr)  # Returns "integration_by_parts"

# 3. Apply technique with explanation
if technique == "integration_by_parts":
    u, dv = self._select_u_dv(expr)
    steps = [
        {"rule": "Select u and dv", "explanation": f"Let u = {u}, dv = {dv}"},
        {"rule": "Compute du and v", "explanation": "..."},
        # ... more steps
    ]
    result = sp.integrate(expr, variable)  # SymPy computes, Calcora explains
```

### Numeric Fallback
```python
# For definite integrals, numeric integration as safety net
try:
    symbolic_result = sp.integrate(expr, (x, a, b))
except:
    # Fallback to Simpson's rule
    numeric_result = sp.integrate(expr, (x, a, b), method='quad')
```

---

## Future Considerations

**v0.3+:** If SymPy becomes a bottleneck:
- Explore SymEngine (C++ backend with Python bindings)
- Profile hot paths, optimize expressions before passing to SymPy
- Consider hybrid approach (SymPy for correctness, custom code for performance)

**v1.0+:** For research-grade accuracy:
- Add alternative CAS comparison (Mathematica, SageMath) as validation
- Document differences between CAS results
- Provide "confidence score" based on cross-verification

---

## References

- **SymPy Paper:** Meurer, A., et al. (2017). "SymPy: symbolic computing in Python." *PeerJ Computer Science*, 3, e103. https://doi.org/10.7717/peerj-cs.103
- **SymPy Documentation:** https://docs.sympy.org/
- **GitHub:** https://github.com/sympy/sympy (17k+ stars, 4k+ forks)

---

## Review Notes

**Decision Rationale:**  
SymPy is the only option that meets all 5 requirements (peer-reviewed, open-source, Python-native, documented, maintained). Custom implementation is academically irresponsible for v0.2 timeline.

**Consensus:** Accepted unanimously on 2026-01-10.

**Next Review:** v0.5 (If performance becomes critical issue, revisit SymEngine)
