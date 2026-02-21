# Professor Outreach Template

**Target:** Tier 1 (Friendly professors, teaching-focused universities)  
**Timing:** Ready now (post-CI/benchmarks)  
**Goal:** 2-3 pilot professors for student feedback

---

## Email Template — Friendly Professor

**Subject:** Quick feedback on open-source Calculus teaching tool?

---

Hi [Professor Name],

I hope you're doing well! I'm reaching out because I've been building **Calcora**, an open-source platform that shows step-by-step integration solutions for Calculus II students.

**What makes it different:**
- Shows the *reasoning* behind each step (not just final answers)
- Open-source and self-hostable (zero data collection)
- Covers 10 standard integration techniques (power rule, u-sub, by parts, partial fractions, etc.)
- Free forever (no premium tiers)

**Current status (v0.2-alpha):**
- ✅ 43/43 automated tests passing
- ✅ 96% accuracy on standard problems (validated against SymPy)
- ✅ Live demo working: [calcoralive.netlify.app](https://calcoralive.netlify.app)

**My ask:**  
Would you be willing to have 5-10 students test it as an **optional** homework checker for one week? I'm gathering feedback from educators before approaching larger institutions.

**Honest disclaimer:**  
This is alpha software. It covers ~80% of Calculus II curriculum, but not advanced techniques (trig substitution, Weierstrass). Students should still verify answers independently.

No pressure — only if this sounds useful for your teaching. Happy to provide setup help or answer any questions.

Best,  
[Your Name]

P.S. Here's a quick example of the step-by-step output: [screenshot or link]

---

## Email Template — Teaching-Focused University (Cold)

**Subject:** Open-source alternative to WolframAlpha for Calculus II?

---

Dear Professor [Name],

I'm [Your Name], developer of **Calcora**, an open-source computational mathematics platform designed specifically for Calculus education.

**Why I'm reaching out:**  
Many students rely on WolframAlpha's paid tier ($7/mo) to understand integration techniques. Calcora provides similar step-by-step explanations, but:
- Completely free (MIT license)
- Self-hostable (FERPA-compliant, no student data leaves campus)
- Pedagogically focused (explains *why* techniques work)

**Validation:**
- 43/43 automated tests passing
- 96% accuracy vs SymPy on 25+ benchmark problems
- Covers 10 core integration techniques from standard curriculum

**Current limitations:**
- Alpha software (v0.2)
- ~80% Calculus II coverage (missing advanced trig substitution)
- Not suitable for grading (verification recommended)

**What I'm looking for:**  
1-2 professors willing to pilot test with students (optional homework tool)

Would this be useful for your Calculus II courses? I'm happy to provide:
- Private demo/walkthrough
- Setup assistance for self-hosted deployment
- Pre/post surveys for student feedback

Demo: [calcoralive.netlify.app](https://calcoralive.netlify.app)  
GitHub: [github.com/yourusername/Calcora](https://github.com/yourusername/Calcora)

Best regards,  
[Your Name]  
[Your Affiliation/LinkedIn]

---

## Email Template — Math Education Researcher

**Subject:** Open-source platform for studying integration pedagogy

---

Dear Dr. [Name],

I'm reaching out because your work on [their research topic] aligns with a project I've been developing.

**Calcora** is an open-source platform that provides transparent, step-by-step integration solutions. Unlike commercial tools, it:
- Exposes the algorithmic decision tree (which technique to apply when)
- Offers three verbosity levels (concise/detailed/teacher mode)
- Provides full API access for research instrumentation

**Potential research applications:**
- Study how students interact with step-by-step explanations
- Measure learning outcomes: worked examples vs. automated hints
- Analyze common misconceptions via error patterns
- A/B test verbosity levels for retention

**Technical details:**
- Built on SymPy (peer-reviewed CAS)
- 43/43 tests passing, 96% accuracy on benchmarks
- Self-hostable (log student interactions locally)
- MIT license (use/modify freely)

**Would this be useful** for your research group? I'd be happy to:
- Add custom instrumentation endpoints
- Provide anonymized usage data from pilot studies
- Collaborate on a short paper (e.g., "Design of Transparent CAS for Calculus Education")

Live demo: [calcoralive.netlify.app](https://calcoralive.netlify.app)

Best,  
[Your Name]

---

## Follow-Up Template (After 1 Week)

**Subject:** Re: Calcora feedback request

---

Hi [Professor Name],

Just following up on my message from last week about Calcora (open-source Calculus tool).

I know you're busy, so **no worries if this isn't a good fit** for your courses right now.

If you're still interested but need more info:
- Here's a 2-minute walkthrough: [video/screenshot]
- Benchmark validation report: [link to benchmarks/]
- Comparison vs WolframAlpha: [README section]

Thanks for considering!

[Your Name]

---

## Key Success Metrics (Track for Harvard Pitch)

After Tier 1 outreach, document:

1. **Response rate**: X/Y professors responded (aim for >40%)
2. **Adoption rate**: X professors agreed to pilot (aim for 2-3)
3. **Student usage**: X students tested, Y found helpful (aim for >70% positive)
4. **Quotes**: "Students appreciated seeing the LIATE priority in action" — Prof. XYZ
5. **Issues found**: List bugs/UX problems discovered during pilots

**Use these for Harvard email:**
> "Calcora has been piloted by 3 Calculus II professors with 45 students. 
> 89% found step-by-step explanations helpful for understanding integration techniques 
> (see attached pilot report)."

---

## Red Flags to Avoid

❌ **Don't say:**
- "Revolutionary" / "game-changing" / "best tool"
- "Comprehensive" / "handles any function"
- "Ready for production" / "research-grade"
- "Better than WolframAlpha"

✅ **Do say:**
- "Open-source alternative" / "pedagogical focus"
- "Covers ~80% of Calculus II curriculum"
- "Alpha software, suitable for optional homework checking"
- "Transparent step-by-step (similar concept to WA, but free and self-hostable)"

---

## Timing

- **Week 1:** Send 3-5 friendly outreach emails
- **Week 2:** Follow up, get 2 commitments
- **Week 3-4:** Pilot testing, collect feedback
- **Week 5:** Analyze results, iterate on UX issues
- **Week 6:** Craft Harvard email with pilot testimonials
