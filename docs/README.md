# Calcora Documentation

**Welcome to the Calcora documentation!** This directory contains all project documentation organized by purpose.

---

## 📚 For Contributors

Start here if you want to contribute code, tests, or documentation:

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** — How to set up dev environment, coding standards, workflow
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — System design, data flow, key components (30-min overview)
- **[CODING_STANDARDS.md](CODING_STANDARDS.md)** — Style guide, complexity limits, documentation requirements
- **[ADR/](ADR/)** — Architecture Decision Records (why we made specific design choices)

### Quick Start for New Contributors
1. Read [CONTRIBUTING.md](../CONTRIBUTING.md) "Quick Start" section (5 min)
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) "Understanding the Architecture" (20 min)
3. Pick a `good-first-issue` from GitHub Issues
4. Follow [CODING_STANDARDS.md](CODING_STANDARDS.md) checklist

---

## 🗺️ For Maintainers

Managing the project long-term:

- **[ROADMAP.md](ROADMAP.md)** — Product roadmap with conservative timelines (v0.2 → v1.0)
- **[VERSIONING.md](VERSIONING.md)** — SemVer policy, API stability guarantees, deprecation process
- **[SECURITY.md](SECURITY.md)** — Security policy, vulnerability reporting, supported versions
- **[releases/](releases/)** — Release notes and post-mortems for each version

---

## 📖 For Users

Using Calcora or integrating it into your workflow:

- **[guides/GETTING_STARTED.md](guides/GETTING_STARTED.md)** — Installation and first use
- **[guides/INTEGRATION_FEATURES.md](guides/INTEGRATION_FEATURES.md)** — Complete guide to integration capabilities
- **[guides/QUICK_REFERENCE.md](guides/QUICK_REFERENCE.md)** — Cheat sheet for common tasks
- **[guides/VERIFICATION.md](guides/VERIFICATION.md)** — How to verify computation correctness

---

## 🎓 For Academic Outreach

Materials for reaching out to professors and universities:

- **[outreach/STRATEGY.md](outreach/STRATEGY.md)** — Overall academic outreach strategy
- **[outreach/TEMPLATES.md](outreach/TEMPLATES.md)** — Email templates for professors
- **[outreach/CHECKLIST.md](outreach/CHECKLIST.md)** — Pre-outreach checklist
- **[outreach/ONE_PAGER.md](outreach/ONE_PAGER.md)** — One-page project summary for busy academics

---

## 🚀 For Deployment

Deploying Calcora to production:

- **[deployment/GUIDE.md](deployment/GUIDE.md)** — Full deployment guide (Netlify, Render, etc.)
- **[deployment/SEO.md](deployment/SEO.md)** — SEO optimization for discoverability

---

## 📦 Releases

Version-specific documentation:

- **[releases/v0.2/](releases/v0.2/)** — v0.2 release notes, fixes, enhancements, verification
- Future releases will have their own folders (v0.3, v0.4, v1.0)

---

## 🔗 Quick Links

| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](../README.md) | Project overview | Everyone |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Contribution guide | Contributors |
| [CHANGELOG.md](../CHANGELOG.md) | Change history | Users + Maintainers |
| [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) | Community standards | Everyone |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design | Contributors + Maintainers |
| [CODING_STANDARDS.md](CODING_STANDARDS.md) | Code quality standards | Contributors |
| [VERSIONING.md](VERSIONING.md) | Version policy | Maintainers + API users |
| [ROADMAP.md](ROADMAP.md) | Product roadmap | Everyone |
| [ADR/](ADR/) | Design decisions | Contributors + Maintainers |

---

## 📂 Directory Structure

```
docs/
├── README.md (this file) ..................... Master index
├── ARCHITECTURE.md ........................... System design & data flow
├── CODING_STANDARDS.md ....................... Code quality standards
├── VERSIONING.md ............................. SemVer policy & API stability
├── ROADMAP.md ................................ Product roadmap (v0.2 → v1.0)
├── SECURITY.md ............................... Security policy & reporting
│
├── ADR/ ...................................... Architecture Decision Records
│   ├── README.md
│   ├── ADR-001-separate-integration-engine.md
│   ├── ADR-002-sympy-as-backend.md
│   └── ADR-003-dict-return-not-class.md
│
├── guides/ ................................... User guides
│   ├── GETTING_STARTED.md .................... Installation & first use
│   ├── INTEGRATION_FEATURES.md ............... Integration capabilities
│   ├── QUICK_REFERENCE.md .................... Command cheat sheet
│   └── VERIFICATION.md ....................... Verify correctness
│
├── outreach/ ................................. Academic outreach materials
│   ├── STRATEGY.md ........................... Outreach strategy
│   ├── TEMPLATES.md .......................... Email templates
│   ├── CHECKLIST.md .......................... Pre-outreach checklist
│   └── ONE_PAGER.md .......................... Project summary
│
├── deployment/ ............................... Deployment documentation
│   ├── GUIDE.md .............................. Deployment guide
│   └── SEO.md ................................ SEO optimization
│
└── releases/ ................................. Release-specific docs
    └── v0.2/
        ├── RELEASE_NOTES.md .................. v0.2 release notes
        ├── FIXES.md .......................... Bug fixes
        ├── ENHANCEMENTS.md ................... New features
        ├── VERIFICATION.md ................... Test results
        ├── BEFORE_AFTER.md ................... Comparison
        └── MISSION_COMPLETE.md ............... Completion summary
```

---

## 🆘 Need Help?

- **New contributor?** Start with [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Understanding design?** Read [ARCHITECTURE.md](ARCHITECTURE.md)
- **Using Calcora?** Check [guides/](guides/)
- **Deploying?** See [deployment/](deployment/)
- **Questions?** Open GitHub Discussion

---

## 📝 Documentation Standards

All documentation in this directory follows these standards:

1. **Markdown format** — Standard GitHub-flavored markdown
2. **Clear headings** — Hierarchical structure (H1 → H2 → H3)
3. **Code examples** — Syntax highlighting with language tags
4. **Cross-references** — Use relative links (e.g., `[ARCHITECTURE.md](ARCHITECTURE.md)`)
5. **Tables of contents** — For docs >100 lines
6. **Last updated** — Include date at bottom of long-lived docs

**To update a document:**
1. Make changes following the standards above
2. Update "Last Updated" date (if present)
3. Update cross-references if structure changes
4. Test all links
5. Commit with `docs: <description>` prefix

---

**Last Updated:** February 21, 2026
