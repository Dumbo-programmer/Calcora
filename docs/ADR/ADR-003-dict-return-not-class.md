# ADR-003: Return Dict Instead of Result Classes

**Status:** Accepted (but under review for v1.0)  
**Date:** 2026-01-12  
**Decision-makers:** Calcora Core Team

---

## Context

The `IntegrationEngine.integrate()` method needs to return multiple pieces of information:
- Success status (`True`/`False`)
- Result expression (`"x**3/3 + C"`)
- Step-by-step explanation (list of step objects)
- Metadata (technique used, computation time, graph data if requested)
- Error messages (if failure)

### Requirements

1. **FastAPI compatibility** (must serialize to JSON for API responses)
2. **Easy to extend** (add new fields without breaking existing code)
3. **IDE autocomplete** (developers should see available fields)
4. **Type-safe** (catch errors at development time, not runtime)

---

## Decision

**Use plain Python `dict` as return type.**

**Return Schema:**
```python
{
    "success": bool,
    "output": str,              # LaTeX or plain text result
    "steps": List[dict],        # Step-by-step explanation
    "technique": str,           # e.g., "u_substitution", "by_parts"
    "computation_time_ms": float,
    "graph": Optional[dict],    # If generate_graph=True
    "error": Optional[str]      # If success=False
}
```

**Example:**
```python
result = engine.integrate("x * exp(x)", "x")
# Returns:
{
    "success": True,
    "output": "x*exp(x) - exp(x) + C",
    "steps": [
        {"rule": "Select u and dv", "explanation": "Let u = x, dv = exp(x) dx"},
        {"rule": "Compute du and v", "explanation": "Then du = dx, v = exp(x)"},
        # ...
    ],
    "technique": "integration_by_parts",
    "computation_time_ms": 12.4,
    "graph": None
}
```

---

## Alternatives Considered

### Alternative 1: Dedicated Result Class

**Approach:**
```python
@dataclass
class IntegrationResult:
    success: bool
    output: str
    steps: List[Step]
    technique: str
    computation_time_ms: float
    graph: Optional[GraphData] = None
    error: Optional[str] = None
```

**Pros:**
- **Type-safe:** IDE catches typos (`result.outpt` → error)
- **Self-documenting:** Clear schema in one place
- **Validation:** Can add `__post_init__` checks

**Cons:**
- **JSON serialization complexity:** Need custom encoder/decoder
- **Harder to extend:** Adding field requires changing class definition
- **Import overhead:** Users must `from calcora.models import IntegrationResult`
- **Rejected:** Extra complexity not justified for v0.2

### Alternative 2: Named Tuple

**Approach:**
```python
IntegrationResult = namedtuple('IntegrationResult', [
    'success', 'output', 'steps', 'technique', 'computation_time_ms', 'graph', 'error'
])
```

**Pros:**
- Lightweight (no class overhead)
- Immutable (safer)
- Dot notation (`result.output`)

**Cons:**
- **No optional fields:** Must always provide all 7 fields
- **No default values:** Can't do `IntegrationResult(success=True, output="...")`
- **Poor FastAPI support:** Requires manual serialization
- **Rejected:** Too rigid for evolving API

### Alternative 3: Pydantic Models

**Approach:**
```python
from pydantic import BaseModel

class IntegrationResult(BaseModel):
    success: bool
    output: str
    steps: List[dict]
    technique: str
    computation_time_ms: float
    graph: Optional[dict] = None
    error: Optional[str] = None
```

**Pros:**
- **Perfect FastAPI integration:** Automatic validation + serialization
- **Type-safe:** Pydantic validates at runtime
- **JSON schema generation:** Automatic OpenAPI docs

**Cons:**
- **Dependency overhead:** Adds Pydantic as hard dependency
- **Overkill for simple responses:** Most users don't need validation
- **Learning curve:** Contributors must understand Pydantic
- **Rejected for v0.2:** Revisit for v1.0 when API stabilizes

---

## Decision Rationale

**Why `dict` wins for v0.2:**

1. **Zero friction:** Every Python developer understands dicts
2. **FastAPI native:** `return {"success": True, ...}` just works
3. **Easy to extend:** Add `"warning": "Integration may be incomplete"` without changing codebase
4. **No dependency:** Works with stdlib only
5. **JSON-ready:** `json.dumps(result)` works immediately

**Trade-offs we accept:**
- ❌ No IDE autocomplete for result keys
- ❌ Typos not caught until runtime (`result["outpt"]` doesn't error until accessed)
- ⚠️ Schema documentation must live in README/docstrings, not code

---

## Consequences

### Positive

✅ **Rapid Prototyping**
- Add new fields without touching class definitions
- Example: Added `"computation_time_ms"` in one line

✅ **FastAPI Simplicity**
```python
@app.post("/integrate")
def integrate_endpoint(expr: str, var: str):
    result = engine.integrate(expr, var)
    return result  # FastAPI serializes dict automatically
```

✅ **JavaScript-Friendly**
- Frontend receives plain JSON object
- No need for client-side deserialization classes

✅ **Backward Compatibility**
- Adding optional fields (e.g., `"warnings": List[str]`) doesn't break existing code
- Old clients ignore new fields

### Negative

❌ **No Type Safety**
```python
# This typo won't be caught until runtime:
if result["succes"]:  # Typo: should be "success"
    print(result["output"])
```

**Mitigation:** Comprehensive tests + linting with `mypy` type hints in function signatures

❌ **Schema Drift**
- No central source of truth for return schema
- Different parts of codebase might return slightly different dicts

**Mitigation:** Document schema in:
1. Function docstring
2. README "API Reference"
3. OpenAPI schema (FastAPI generates this automatically)

❌ **No Validation**
- If code accidentally returns `{"success": "yes"}` (string instead of bool), no error until client fails

**Mitigation:** Add integration tests that validate return types

### Neutral

⚪ **IDE Support Varies**
- PyCharm can infer dict keys from `TypedDict` annotations (see Future Work)
- VS Code with Pylance requires explicit type hints

---

## Future Work

### v0.3: Use TypedDict for Type Hints

Add type hints without changing runtime behavior:

```python
from typing import TypedDict, List, Optional

class IntegrationResultDict(TypedDict):
    success: bool
    output: str
    steps: List[dict]
    technique: str
    computation_time_ms: float
    graph: Optional[dict]
    error: Optional[str]

def integrate(self, expression: str, variable: str) -> IntegrationResultDict:
    # Return plain dict, but IDE knows the schema
    return {"success": True, ...}
```

**Benefit:** IDE autocomplete + type checking, no runtime overhead

### v1.0: Migrate to Pydantic Models

Once API is stable and we have 100+ users:

1. **Create Pydantic models** for all return types
2. **Validate inputs and outputs** (catch bugs earlier)
3. **Generate OpenAPI schema** automatically
4. **Deprecate dict returns** (keep for 2 minor versions per VERSIONING.md)

**Migration path:**
```python
# v0.9: Both dict and Pydantic work
result = engine.integrate("x**2", "x")
assert isinstance(result, IntegrationResult)  # Pydantic model
assert result.success == True  # Dot notation
assert result.dict()["success"] == True  # Still works as dict

# v1.0: Pydantic only (dict access deprecated)
# v1.2: Dict access removed
```

---

## References

- **FastAPI Best Practices:** https://fastapi.tiangolo.com/tutorial/response-model/
- **TypedDict PEP:** PEP 589 (Python 3.8+)
- **Similar Pattern:** Flask returns plain dicts, Django REST Framework uses serializers (too heavy for us)

---

## Review Notes

**Decision Rationale:**  
Plain dicts are the simplest thing that could work for v0.2. We're not at scale where type safety becomes critical (no team of 10+ developers). Pydantic would be premature optimization.

**When to revisit:**
1. **v0.5+:** If we have 3+ return types (integration, differentiation, series), consider shared result base class
2. **v1.0:** When API stabilizes, migrate to Pydantic for production-grade validation
3. **Bug reports about schema inconsistency:** If users complain about undocumented fields, switch to TypedDict

**Consensus:** Accepted on 2026-01-12 with plan to revisit at v1.0.

**Status:** ✅ Accepted (use dicts for now, TypedDict in v0.3, Pydantic in v1.0)
