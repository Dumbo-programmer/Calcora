# ADR-001: Separate Integration Engine from Step Engine

**Status:** Accepted  
**Date:** 2026-01-15  
**Decision-makers:** Calcora Core Team

---

## Context

During v0.1, all symbolic computation logic was tightly coupled within `step_engine.py`. This worked for differentiation (single operation type), but integration requires:

1. **Multiple technique detection** (u-substitution, by parts, partial fractions, etc.)
2. **Complex decision trees** ("If polynomial, use power rule; else if product, check LIATE priority...")
3. **Fallback strategies** (numerical methods when symbolic fails)
4. **Graph generation** (plot integrand + antiderivative + shaded area)

Cramming all this into `step_engine.py` would create a 2000+ line monolithic file that's hard to test and maintain.

### Requirements

- Integration must return step-by-step explanations (like differentiation)
- Need to experiment with technique selection without breaking differentiation
- Should be independently testable (29 integration tests vs 9 differentiation tests)
- Future-proof: limits/series expansion may need similar separation

---

## Decision

**Create `src/calcora/integration_engine.py` as a standalone module**, separate from `step_engine.py`.

**API Design:**
```python
class IntegrationEngine:
    def integrate(
        self,
        expression: str,
        variable: str,
        lower_limit: Optional[float] = None,
        upper_limit: Optional[float] = None,
        verbosity: str = "concise",
        generate_graph: bool = False
    ) -> dict:
        """Returns dict with success, output, steps, technique, graph."""
```

**Rationale:**
- Integration complexity warrants dedicated file (700 lines currently, room to grow)
- Isolated testing (can mock SymPy separately from step engine)
- API flexibility (can add `timeout`, `max_iterations` without affecting differentiation)
- Clear responsibility: `step_engine.py` = general DAG, `integration_engine.py` = integration-specific logic

---

## Alternatives Considered

### Alternative 1: Keep Everything in `step_engine.py`

**Pros:**
- One central file for all symbolic operations
- Reuses existing plugin infrastructure

**Cons:**
- File becomes 2000+ lines (hard to navigate)
- Tight coupling between differentiation and integration logic
- Changes to integration risk breaking differentiation tests
- **Rejected:** Violates single responsibility principle

### Alternative 2: Plugin-Based Integration Rules

**Pros:**
- Follows existing plugin model
- Highly extensible (community can add techniques)

**Cons:**
- Over-engineered for v0.2 (only 1 integration "plugin" needed)
- Plugin overhead (registry, discovery, priority) not justified yet
- Harder to debug (logic scattered across files)
- **Rejected:** Wait until v0.4+ when we have >3 integration engines (symbolic, numerical, CAS comparison)

### Alternative 3: Micro-Services Architecture

**Pros:**
- Ultimate separation of concerns
- Could scale horizontally

**Cons:**
- Massive overkill for educational tool
- Network overhead for local computation
- Deployment complexity
- **Rejected:** Not appropriate for offline-first tool

---

## Consequences

### Positive

✅ **Clear Separation of Concerns**
- `step_engine.py`: Generic DAG construction (~400 lines)
- `integration_engine.py`: Integration-specific logic (~700 lines)
- `differentiation_rules.py`: Differentiation rules (~500 lines)

✅ **Independent Testing**
- 29 integration tests don't clutter differentiation test suite
- Can refactor integration without touching differentiation

✅ **Faster Iteration**
- New integration techniques added without risk to differentiation
- Performance optimizations isolated

✅ **Easier Onboarding**
- New contributors can understand integration_engine.py in isolation
- Don't need to understand full step_engine.py architecture

### Negative

❌ **Code Duplication**
- Some step formatting logic duplicated between engines
- Solution: Extract to shared `utils/step_formatting.py` in v0.3

❌ **API Inconsistency**
- `step_engine` uses `StepGraph` object
- `integration_engine` uses `dict` return type
- Solution: Converge on shared result format in v1.0 (see ADR-003)

❌ **Missed Plugin Reuse**
- Integration techniques not pluggable like differentiation rules
- Solution: If we need >10 integration techniques (v0.4+), refactor to plugin model

### Neutral

⚪ **File Count Increases**
- Now have 3 engines instead of 1
- Trade-off: More files but each file is understandable

⚪ **Import Paths**
- Users must `from calcora.integration_engine import IntegrationEngine`
- Not a problem: documented in README

---

## Future Work

1. **v0.3:** Extract shared step formatting to `utils/step_formatting.py`
2. **v0.4:** If we add symbolic series expansion, create `series_engine.py` following same pattern
3. **v1.0:** Unify return types (`StepGraph` vs `dict`) — see ADR-003

## References

- Original discussion: GitHub Issue #38
- Similar pattern: SymPy separates `integrate()` from `diff()` in distinct modules
- Textbook reference: Stewart's Calculus dedicates Ch. 5-6 to differentiation, Ch. 7-8 to integration (conceptually separate)

---

## Review Notes

**Decision Rationale:**  
At 700 lines and growing, keeping integration in `step_engine.py` would create maintenance burden. Separate file is net positive for understandability and testing.

**Consensus:** Accepted by core team on 2026-01-15.

**Next Review:** v0.5 (If integration_engine.py exceeds 1500 lines, consider splitting into technique-specific modules)
