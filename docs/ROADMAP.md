# Calcora Roadmap (Public)

**Philosophy:** Lock scope. Deepen vertically. Stay focused on Calculus I/II until v1.0.

This roadmap is **conservative by design**—timelines include buffer for testing, documentation, and academic validation. Dates are targets, not promises.

**Scope Commitment:** Calcora will NOT expand to linear algebra, graph theory, or differential equations until v1.0 is proven stable. First, do Calculus I/II well.

---

## ✅ v0.1.0 — MVP (Completed: Jan 2026)

**Goal:** Prove the step-by-step architecture works

- ✅ Core project scaffolding (FastAPI backend, Chart.js frontend)
- ✅ Deterministic StepGraph DAG model
- ✅ Differentiation engine (9 rules, 85% Calc I coverage)
- ✅ Basic integration (10 techniques, ~60% Calc II coverage)
- ✅ Text + JSON renderers
- ✅ Live demo deployed (Netlify)

**Status:** Architecture validated, ready for depth improvements.

---

## 🔄 v0.2.0-alpha — Integration Depth (Current: Feb 2026)

**Goal:** Make integration production-quality for Calculus II

### Completed This Sprint
- ✅ Comprehensive test suite (43/43 tests passing, 47% coverage)
- ✅ GitHub Actions CI pipeline (multi-platform, multi-version)
- ✅ Benchmark validation framework (96% accuracy vs SymPy)
- ✅ Academic-honest README (transparent limitations)
- ✅ Coding standards + versioning discipline

### In Progress (Feb 2026)
- 🔄 **Edge case testing** — Discontinuous functions, improper integrals, undefined points
- 🔄 **Performance optimization** — Target <50ms average for standard Calc II problems
- 🔄 **Explanation quality** — Improve step clarity based on user feedback

### Planned Before v0.3 (Feb-Mar 2026)
- 📋 Lighthouse accessibility audit (target: ≥90/100)
- 📋 Tier 1 professor outreach (3-5 friendly instructors)
- 📋 Student feedback collection (10+ real users)
- 📋 Integration coverage 70% → 80% (add rational function edge cases)

**Release Criteria for v0.2.0 (Stable Alpha):**
- ✅ All tests passing (43/43)
- ✅ Coverage ≥70% integration engine
- ✅ Benchmark accuracy ≥95% vs SymPy
- ⏳ 2+ professor testimonials
- ⏳ Accessibility score ≥90

**Target:** March 15, 2026

---

## 📋 v0.3.0-beta — LaTeX Export + Polish (Apr-Jun 2026)

**Goal:** Make Calcora classroom-ready (exportable, shareable, printable)

### Features
- **LaTeX rendering** — Export step-by-step solutions as LaTeX
  - Render engine converts internal representation → LaTeX syntax
  - Copy-paste ready for homework assignments
  - MathJax rendering in frontend
- **Performance improvements** — Memoization for repeated sub-expressions
- **Improved error handling** — Clearer messages when integration fails
- **Definite integral improvements** — Better handling of limits at infinity, discontinuities

### Non-Goals (Explicitly Out of Scope)
- ❌ Series expansion (deferred to v0.4)
- ❌ Limits (deferred to v0.4)
- ❌ Equation solving (deferred to future)
- ❌ New math domains (no linear algebra, graphs, etc.)

**Release Criteria:**
- LaTeX export working for all 10 integration techniques
- Performance: ≥90% of problems complete in <100ms
- Test coverage ≥75%
- 5+ professor testimonials
- Accessibility audit passed (≥90/100)

**Target:** June 1, 2026 (conservative estimate: buffer for LaTeX edge cases)

---

## 📋 v0.4.0-beta — Calculus Completeness (Jul-Sep 2026)

**Goal:** Cover 95%+ of standard Calculus I/II curriculum

### Features
- **Series expansion** — Taylor/Maclaurin series with remainder estimation
- **Limits** — Step-by-step limit evaluation (algebraic, L'Hôpital's, squeeze theorem)
- **Substitution improvements** — Trigonometric substitution (currently missing)
- **More benchmarks** — Expand validation dataset to 100+ problems

### Success Metrics
- Calculus II coverage: 80% → 95%
- Benchmark accuracy: 96% → 98%
- Test count: 43 → 100+
- Coverage: 75% → 85%

**Release Criteria:**
- Series expansion working for polynomial, trig, exponential functions
- Limits handle indeterminate forms (0/0, ∞/∞, 0·∞)
- 10+ professor testimonials (including 1+ teaching-focused university adoption)
- Documentation complete (getting started guide, video tutorials)

**Target:** September 15, 2026

---

## 🎯 v1.0.0 — Production-Ready Calculus I/II Tool (Dec 2026)

**Goal:** Stable, reliable, trustworthy tool for academic use

### Maturity Requirements
- **API stability** — Public API frozen (SemVer guarantees kick in)
- **LTS commitment** — Security updates for 2+ years
- **Comprehensive testing** — Coverage ≥90%, 200+ tests
- **Academic adoption** — 20+ professors using in classrooms
- **Student metrics** — 100+ active users, ≥70% satisfaction

### Features (Focus on Depth, Not Breadth)
- **Better explanations** — AI-assisted natural language generation (optional)
- **Multi-language support** — Spanish, Chinese translations
- **Offline mode** — PWA for exam situations (no internet)
- **Export formats** — LaTeX, PDF, plain text, JSON

### Non-Goals (Post-v1.0)
- ❌ Differential equations (v2.0+)
- ❌ Multivariable calculus (v2.0+)
- ❌ Linear algebra (separate project or v3.0+)
- ❌ Graph theory (out of scope forever—wrong domain)

**Release Criteria:**
- Zero known critical bugs
- Performance: 95% of problems <50ms
- Accessibility: 100/100 Lighthouse score
- Documentation: Complete API reference, tutorial videos, teacher guide
- Security audit: Dependency scan clean, OWASP checks passed

**Target:** December 2026 (1 year from MVP to production-ready)

---

## Post-v1.0 (2027+): Deepen, Don't Expand

**Guiding Principle:** Master Calculus I/II before moving to new domains.

### Possible Future Work (Not Committed)
- **v1.x** — Edge case improvements, performance optimization, UI polish
- **v2.0** — Differential equations (if academic demand exists)
- **v2.x** — Multivariable calculus (partial derivatives, multiple integrals)
- **v3.0+** — Other domains (TBD based on user research)

**Decision Gate:** Will NOT start v2.0 work until:
1. v1.0 has 50+ active professors using it
2. Student feedback shows ≥80% satisfaction
3. No critical bugs reported in 3+ months
4. Maintainability audit shows codebase is sustainable

---

## Version Naming Convention

See [VERSIONING.md](VERSIONING.md) for SemVer details.

- **Alpha (v0.1-v0.2):** Features incomplete, API unstable, use at your own risk
- **Beta (v0.3-v0.9):** Features complete, API mostly stable, safe for testing
- **Stable (v1.0+):** Production-ready, API frozen, LTS support

**Current Status (Feb 2026):** v0.2.0-alpha — Integration depth improvements in progress

---

## How This Maps to GitHub Issues

Each version milestone has a GitHub project board:
- **v0.2.0:** https://github.com/user/calcora/projects/2
- **v0.3.0:** (Not yet created—wait until v0.2 ships)

Issues use epic labels: `v0.2-integration-depth`, `v0.3-latex-export`, etc.

**Rule:** Maximum 3 issues "In Progress" at once. Finish before starting new work.

---

## Feedback & Adjustments

This roadmap is **living but conservative**—dates may slip, but scope will NOT expand.

**If we're behind schedule:** Cut features, not quality. Ship v0.3 without LaTeX rather than rush buggy LaTeX.

**If professors request new features:** Add to backlog, prioritize by impact, but don't compromise core Calculus reliability.

**Contact:** For roadmap questions, open a GitHub discussion or email team@calcora.dev
