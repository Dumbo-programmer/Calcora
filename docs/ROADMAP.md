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

## ✅ v0.2.0 — Integration Depth (Completed: Feb 2026)

**Goal:** Make integration production-quality for Calculus II

### Completed Features
- ✅ Comprehensive test suite (43/43 tests passing, 47% coverage)
- ✅ GitHub Actions CI pipeline (multi-platform, multi-version)
- ✅ Benchmark validation framework (96% accuracy vs SymPy)
- ✅ Academic-honest README (transparent limitations)
- ✅ Coding standards + versioning discipline
- ✅ Edge case testing — Discontinuous functions, improper integrals
- ✅ Performance optimization — <50ms average for standard problems
- ✅ Lighthouse accessibility audit (≥90/100 achieved)

**Status:** Shipped February 2026

---

## ✅ v0.3.0 — Desktop App & Production Polish (Completed: Feb 26, 2026)

**Goal:** Professional desktop application with production-ready UX

### Major Features Delivered
- ✅ **Windows Desktop App** — Single-file .exe (37.26 MB, PyInstaller)
- ✅ **Custom Application Icon** — Mathematical ∫ symbol with professional branding
- ✅ **Graceful Shutdown System** — UI button + API endpoint (localhost-only)
- ✅ **Professional Console Output** — Colored, structured messaging (colorama)
- ✅ **Enhanced Reliability** — Health check + multi-browser fallback
- ✅ **OS-Managed Ports** — Security architecture upgrade
- ✅ **Windows EXE Metadata** — Company, version, copyright info
- ✅ **Desktop Mode Badge** — Runtime transparency indicator
- ✅ **Top-Level Exception Boundary** — No raw tracebacks to users

### Documentation & Infrastructure
- ✅ Comprehensive release notes (946 lines)
- ✅ Pre-ship audit (A grade, 95% confidence)
- ✅ Code signing guide for future releases
- ✅ Netlify site updated with download button
- ✅ SHA256 checksums for integrity verification

### Performance Improvements
- ✅ Binary size reduction: 47.79 MB → 37.26 MB (22% smaller)
- ✅ Cold start time: ~2.8 seconds (professional standard)

**Status:** Shipped February 26, 2026 — **Production Ready**

**Known Limitation:** Windows SmartScreen warning (unsigned executable — fixed in v0.3.1)

---

## � v0.3.1 — Code Signing & Trust (Current: Feb-Mar 2026)

**Goal:** Eliminate Windows SmartScreen warning and build trust

### Planned Features
- 📋 **Code-signed executable** — Individual code signing certificate ($199/year)
- 📋 **SmartScreen reputation** — Microsoft publisher verification
- 📋 **Multi-platform testing** — Verify on Windows 10 and Windows 11
- 📋 **Optional console-less mode** — `console=False` build variant
- 📋 **GitHub Actions automation** — Automated signing in build pipeline

### Infrastructure Improvements
- 📋 Automated build signing workflow
- 📋 Certificate management documentation
- 📋 Windows Defender submission tracking

**Release Criteria:**
- Code-signed .exe (no SmartScreen warning)
- Verified on 3+ Windows machines
- Build automation updated

**Target:** March 15, 2026 (after certificate verification, 1-3 days)

---

## 📋 v0.4.0 — LaTeX Export + PyWebView (Apr-Jun 2026)

**Goal:** Make Calcora classroom-ready with exportable solutions and native GUI wrapper

### Features
- **LaTeX rendering** — Export step-by-step solutions as LaTeX
  - Render engine converts internal representation → LaTeX syntax
  - Copy-paste ready for homework assignments
  - MathJax rendering in frontend
- **PyWebView GUI** — Native window wrapper (replaces browser-launcher)
  - No console window (professional native app feel)
  - Better OS integration (file associations, drag-drop)
  - Cross-platform (Windows, macOS, Linux)
- **Performance improvements** — Memoization for repeated sub-expressions
- **Improved error handling** — Clearer messages when integration fails
- **Definite integral improvements** — Better handling of limits at infinity, discontinuities
- **macOS and Linux builds** — Multi-platform desktop apps

### Non-Goals (Explicitly Out of Scope)
- ❌ Series expansion (deferred to v0.5)
- ❌ Limits (deferred to v0.5)
- ❌ Equation solving (deferred to future)
- ❌ New math domains (no additional linear algebra, graphs, etc.)

**Release Criteria:**
- LaTeX export working for all 10 integration techniques
- PyWebView GUI on Windows, macOS, Linux
- Code-signed for all platforms (Windows EV cert, macOS notarization)
- Performance: ≥90% of problems complete in <100ms
- Test coverage ≥80%
- 5+ professor testimonials
- Accessibility audit passed (≥90/100)

**Target:** June 2026 (conservative estimate: buffer for multi-platform builds)

---

## 📋 v0.5.0 — Calculus Completeness (Jul-Sep 2026)

**Goal:** Cover 95%+ of standard Calculus I/II curriculum

### Features
- **Series expansion** — Taylor/Maclaurin series with remainder estimation
- **Limits** — Step-by-step limit evaluation (algebraic, L'Hôpital's, squeeze theorem)
- **Substitution improvements** — Trigonometric substitution (currently missing)
- **More benchmarks** — Expand validation dataset to 100+ problems
- **PDF export** — Generate printable solution sheets

### Success Metrics
- Calculus II coverage: 80% → 95%
- Benchmark accuracy: 96% → 98%
- Test count: 43 → 100+
- Coverage: 80% → 85%

**Release Criteria:**
- Series expansion working for polynomial, trig, exponential functions
- Limits handle indeterminate forms (0/0, ∞/∞, 0·∞)
- 10+ professor testimonials (including 1+ teaching-focused university adoption)
- Documentation complete (getting started guide, video tutorials)

**Target:** September 2026

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

**Current Status (Feb 26, 2026):** v0.3.0 shipped — Desktop app production-ready, working on v0.3.1 code signing

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
