# Architecture Decision Records (ADRs)

This directory documents **why** architectural decisions were made, not just what was implemented.

## What is an ADR?

An **Architecture Decision Record** captures:
- The context that led to a decision
- The decision itself
- The consequences (trade-offs)

**Purpose:** In 2 years, when you've forgotten why `integration_engine.py` is separate from `step_engine.py`, you can read ADR-002 and understand the reasoning.

## When to Write an ADR

Create an ADR for decisions that:
- Affect public API design
- Change core architecture (new modules, separation of concerns)
- Introduce new dependencies
- Establish patterns (error handling, testing approaches)
- Reject alternative approaches

**Don't create ADRs** for:
- Bug fixes (use commit messages)
- Minor refactoring (keep explanations in code comments)
- Obvious choices (e.g., "We chose Python because...")

## ADR Format

```markdown
# ADR-XXX: Title

**Status:** Accepted | Superseded by ADR-YYY | Rejected  
**Date:** YYYY-MM-DD  
**Decision-makers:** Name(s)

## Context

What is the problem we're trying to solve?
What constraints exist?

## Decision

What did we decide to do?

## Alternatives Considered

What other approaches did we evaluate? Why were they rejected?

## Consequences

### Positive
- What benefits does this bring?

### Negative
- What trade-offs are we accepting?

### Neutral
- What changes but neither helps nor hurts?
```

## Current ADRs

| Number | Title | Status |
|--------|-------|--------|
| [001](ADR-001-separate-integration-engine.md) | Separate Integration Engine from Step Engine | Accepted |
| [002](ADR-002-sympy-as-backend.md) | Use SymPy as Symbolic Backend | Accepted |
| [003](ADR-003-dict-return-not-class.md) | Return Dict Instead of Result Classes | Accepted |

## Creating New ADRs

1. Copy `ADR-000-template.md`
2. Increment number: Next available is ADR-004
3. Fill in all sections
4. Get review from maintainer
5. Merge to `main` branch
6. Update this README index
