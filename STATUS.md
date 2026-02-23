# Calcora Status Report — February 22, 2026

**Current Phase:** v0.2.0-alpha (Integration Depth)  
**Target Release:** March 15, 2026 (v0.2.0 stable)  
**Days Remaining:** 21 days

---

## ✅ COMPLETED (What's Working)

### Infrastructure ✅
- [x] GitHub Actions CI pipeline (multi-platform testing)
- [x] pytest suite with 43/43 tests passing
- [x] 47% overall coverage, 70% integration engine coverage
- [x] Benchmark validation framework created (not yet run)
- [x] Documentation reorganized into `docs/` structure

### Code Quality ✅
- [x] Coding standards guide (CODING_STANDARDS.md)
- [x] Versioning discipline (VERSIONING.md)
- [x] Architecture Decision Records (3 ADRs documented)
- [x] Contributing guide with 30-min onboarding path

### Positioning ✅
- [x] Academic-honest README (removed overpromising)
- [x] Conservative roadmap (Calculus-focused, realistic dates)
- [x] Professor outreach templates prepared
- [x] Clear limitations documented

---

## 🔄 IN PROGRESS (Started but Not Finished)

### Testing Gaps 🔄
- ⚠️ **Coverage at 47%** (target: 70%+ for v0.2 release)
- ⚠️ **Missing edge cases:**
  - Discontinuous functions (e.g., ∫1/x at x=0)
  - Improper integrals (infinite limits)
  - Undefined points in definite integrals
  - Rational functions with complex denominators
  - Very long expressions (>50 terms)

### Performance 🔄
- ⚠️ **No documented benchmarks** — validate_integration.py exists but not yet run
- ⚠️ **No performance metrics** — avg time per problem unknown
- ⚠️ **No timeout strategy** — could hang on complex problems

### Explanation Quality 🔄
- ⚠️ **Steps exist but could be clearer** — need user feedback
- ⚠️ **No examples of "teacher" verbosity mode** — needs testing
- ⚠️ **Graph generation limited** — works but not fully tested

---

## ❌ NOT STARTED (Planned for v0.2)

### Critical for v0.2 Release ❌
1. **Run benchmark validation** (HIGH PRIORITY)
   - Script exists: `benchmarks/validate_integration.py`
   - Expected: 96% accuracy vs SymPy
   - Output: Markdown table for README
   - **Estimate:** 15 minutes

2. **Lighthouse accessibility audit** (HIGH PRIORITY)
   - Target: ≥90/100 accessibility score
   - Opens in Chrome DevTools on live demo
   - Take screenshot for README
   - **Estimate:** 30 minutes

3. **Add edge case tests** (MEDIUM PRIORITY)
   - Tests for discontinuities, improper integrals
   - Increase integration coverage 70% → 80%
   - **Estimate:** 2 hours

4. **Performance documentation** (MEDIUM PRIORITY)
   - Run benchmarks with timing
   - Document avg/max time per problem
   - Create PERFORMANCE.md
   - **Estimate:** 1 hour

### Important but Can Defer to v0.3 ❌
5. **Tier 1 professor outreach** (Can wait for metrics)
   - Need benchmark results first
   - Need accessibility score first
   - Send 3-5 emails when ready
   - **Estimate:** 1 hour

6. **LaTeX export** (v0.3 feature)
   - Explicitly scoped to v0.3.0-beta (Apr-Jun 2026)
   - Not blocking v0.2 release

---

## 🎯 RELEASE CRITERIA STATUS

**Target: v0.2.0 Stable Alpha (March 15, 2026)**

| Criterion | Status | Blocker? |
|-----------|--------|----------|
| All tests passing | ✅ 43/43 | No |
| Coverage ≥70% integration | ✅ 70% | No |
| Benchmark accuracy ≥95% | ⏳ Not run yet | **YES** |
| 2+ professor testimonials | ❌ 0/2 | No (can slip to v0.3) |
| Accessibility score ≥90 | ⏳ Not tested | **YES** |

**Blockers:** 2 items (benchmark validation, accessibility audit)

---

## 📊 WHAT NEEDS IMPROVEMENT

### Priority 1: Critical Gaps (Blocking v0.2 Release)

**1. Run Benchmark Validation**
- **Why:** Need quotable accuracy metric for outreach
- **What:** Execute `python benchmarks/validate_integration.py`
- **Expected Output:** 
  ```
  ✅ 24/25 problems correct (96% accuracy)
  ✅ Average time: 42ms per problem
  ❌ 1 failure: ∫sec³(x) dx (SymPy disagrees on constant form)
  ```
- **Next Step:** Insert results table into README
- **Estimate:** 15 min to run + 15 min to document = 30 min

**2. Lighthouse Accessibility Audit**
- **Why:** Ensure tool is usable by students with disabilities
- **What:** Open Chrome DevTools on live demo, run Lighthouse
- **Expected Score:** ≥90/100
- **Fixes if Needed:** 
  - Add ARIA labels
  - Improve color contrast
  - Add keyboard navigation
- **Estimate:** 30 min audit + 2 hours fixes (if needed)

### Priority 2: Quality Improvements (Nice to Have)

**3. Increase Test Coverage (47% → 70%)**
- **Current Coverage Breakdown:**
  - Integration engine: 70% ✅
  - Differentiation: 89% ✅
  - Matrices: 45% ⚠️
  - API routes: ~30% ⚠️
- **Focus Areas:**
  - Add matrix operation edge cases
  - Add API error handling tests
  - Add parametrized tests for common patterns
- **Estimate:** 3-4 hours

**4. Edge Case Testing**
- **Missing Tests:**
  ```python
  # Discontinuities
  ∫1/x dx from x=-1 to 1   # Should fail or warn
  
  # Improper integrals
  ∫1/x² dx from x=1 to ∞   # Should handle infinite limits
  
  # Undefined behavior
  ∫√x dx from x=-1 to 1    # Should detect domain issues
  
  # Complex rational functions
  ∫(x³+2x²+x+1)/(x⁴-1) dx  # Partial fractions stress test
  ```
- **Estimate:** 2 hours to write + debug

**5. Performance Benchmarking**
- **Current State:** No documented metrics
- **What to Measure:**
  - Average time per standard Calc II problem
  - Max time (99th percentile)
  - Problems that take >500ms
  - Memory usage for large expressions
- **Output:** `docs/guides/PERFORMANCE.md`
- **Estimate:** 1 hour

### Priority 3: Code Clarity (Maintainability)

**6. Refactor integration_engine.py for Clarity**
- **Current:** 261 lines, borderline for "understand in 30 minutes"
- **Potential Improvements:**
  - Extract `_detect_technique()` to `technique_detector.py` (60+ lines)
  - Split into `integration_engine.py` + `integration_helpers.py`
  - Add more inline comments explaining LIATE priority
- **Benefit:** Easier onboarding for new contributors
- **Estimate:** 2-3 hours (careful refactoring + tests)

---

## 🚀 RECOMMENDED ACTION PLAN

### This Week (Feb 22-28) — Focus on Blockers

**Monday-Tuesday (Feb 22-23):**
1. ✅ Run benchmark validation (30 min)
2. ✅ Document results in README (30 min)
3. ✅ Run Lighthouse audit (30 min)
4. ⏳ Fix accessibility issues if needed (0-2 hours)

**Wednesday-Thursday (Feb 24-25):**
5. ⏳ Add edge case tests (2 hours)
6. ⏳ Performance benchmarking (1 hour)
7. ⏳ Create PERFORMANCE.md (30 min)

**Friday (Feb 26):**
8. ⏳ Run full test suite + verify no regressions
9. ⏳ Update ROADMAP.md with actual metrics
10. ⏳ Commit all changes to `dev` branch

**Status Check:** 
- Blockers cleared? → Proceed to outreach
- Issues found? → Fix before outreach

---

### Next Week (Mar 1-7) — Tier 1 Outreach

**Monday (Mar 1):**
1. Review outreach templates (docs/outreach/TEMPLATES.md)
2. Customize for 3 friendly professors
3. Include metrics: "96% accuracy, 90+ accessibility, 43/43 tests"

**Tuesday-Thursday (Mar 2-4):**
4. Send emails (1 per day, spaced out)
5. Track responses in spreadsheet
6. Answer questions promptly

**Friday (Mar 5):**
7. Follow up on non-responses (use TEMPLATES.md follow-up)

---

### Week 3 (Mar 8-14) — Polish

1. Collect any early feedback
2. Fix critical bugs found by professors
3. Improve test coverage (47% → 70%+)
4. Write v0.2.0 release notes

---

### Week 4 (Mar 15-21) — v0.2.0 Stable Release

**Target: March 15, 2026**

1. Final validation suite run
2. Update CHANGELOG.md
3. Tag release: `git tag v0.2.0`
4. Deploy to production (Netlify)
5. Announce on GitHub Discussions

**Release Checklist:**
- [ ] All tests passing (43/43+)
- [ ] Coverage ≥70%
- [ ] Benchmark accuracy ≥95% documented
- [ ] Accessibility ≥90
- [ ] 2+ professor responses (even if not full testimonials yet)
- [ ] CHANGELOG.md updated
- [ ] Release notes published
- [ ] Live demo working

---

## 📋 WHAT TO DO RIGHT NOW (Immediate Next Steps)

### Step 1: Run Benchmark Validation (15 min)

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run benchmark validation
python benchmarks/validate_integration.py

# Outputs markdown table like:
# | Expression | Calcora | SymPy | Match | Time (ms) | Technique |
# |------------|---------|-------|-------|-----------|-----------|
# | x²         | x³/3+C  | x³/3  | ✅    | 12.3      | power_rule |
# | ...        | ...     | ...   | ...   | ...       | ...        |
```

**Expected Issues:**
- Constant of integration differences (C vs no C) — script handles this
- Different but equivalent forms (e.g., `ln(x)` vs `log(x)`) — symbolic equality check

**Success Criteria:** ≥95% match rate (24/25 or better)

### Step 2: Lighthouse Audit (30 min)

```bash
# 1. Open live demo
Start-Process "https://calcoralive.netlify.app/demo.html"

# 2. Open Chrome DevTools (F12)
# 3. Click "Lighthouse" tab
# 4. Select:
#    - Categories: ✅ Performance, ✅ Accessibility, ✅ Best Practices
#    - Device: Desktop
# 5. Click "Analyze page load"
# 6. Wait 30-60 seconds
# 7. Screenshot results
```

**Expected Issues:**
- Missing ARIA labels on math input
- Color contrast issues on step explanations
- Missing alt text on graph images

**Success Criteria:** Accessibility ≥90/100

### Step 3: Document Results (30 min)

Update README.md with:
1. Benchmark validation table
2. Lighthouse score badge
3. Performance metrics (avg time)

---

## 💡 KEY INSIGHTS

### What's Going Well ✅
1. **Engineering discipline is solid** — ADRs, coding standards, versioning policy all in place
2. **Documentation is excellent** — 30-min onboarding path, organized structure
3. **Tests are passing** — 43/43, no regressions
4. **Positioning is honest** — No overpromising anymore

### What's Holding Us Back ⚠️
1. **Haven't validated core claims** — "96% accuracy" is theoretical until we run benchmarks
2. **No user feedback loop** — Need professor/student testing to improve
3. **Performance is unknown** — Could be fast or slow, we don't know
4. **Accessibility untested** — Could be blocking students with disabilities

### What's at Risk 🔴
1. **March 15 release date** — Achievable if we focus on blockers this week
2. **Professor credibility** — Can't claim "96% accurate" without proof
3. **V0.3 timeline** — If v0.2 slips, v0.3 (LaTeX export) slips to July+

---

## 🎯 DEFINITION OF DONE (v0.2.0)

**When can we confidently release v0.2.0 stable?**

✅ **Technical Excellence:**
- All tests passing (43/43+)
- Coverage ≥70% overall
- Benchmark validation run and documented
- Performance metrics documented
- No critical bugs

✅ **Accessibility:**
- Lighthouse score ≥90/100
- Keyboard navigation working
- Screen reader compatible

✅ **Documentation:**
- README accurate (no false claims)
- CHANGELOG.md updated
- Release notes published
- All links working

✅ **Academic Readiness:**
- 2+ professor responses (even if just "interesting, will try")
- Outreach templates validated
- Testimonials collected (can be post-release)

**If all above ✅ → Ship v0.2.0**  
**If any blockers ❌ → Delay 1 week, fix, re-validate**

---

## 📞 NEED HELP?

- **Benchmark fails:** Debug SymPy integration, check test cases
- **Accessibility low:** Hire accessibility consultant or use automated tools
- **Coverage stuck:** Focus on API routes and matrix operations (currently <50%)
- **Performance slow:** Profile with `cProfile`, optimize hot paths

---

**Next Action:** Run `python benchmarks/validate_integration.py` 🚀

**Last Updated:** February 22, 2026
