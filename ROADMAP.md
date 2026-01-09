# Calcora Roadmap (Public)

This roadmap is written for users, educators, and contributors. Versions represent capability milestones and API stability—not a promise of exact dates.

## v0.1 — MVP (Architecture-First)

- Core project scaffolding (engine, plugin SDK, CLI/API stubs)
- Deterministic step DAG data model
- Minimal symbolic pipeline (via optional SymPy adapter)
- Baseline renderers: text + JSON

## v0.2 — Explainability Engine

- Formal rule selection + auditing metadata
- Multiple verbosity levels (concise / detailed / teacher)
- Stronger validation/safety checks for plugins
- Exportable reasoning output (JSON DAG)

## v0.3 — Linear Algebra & Graphs

**Linear algebra**
- Gaussian elimination with steps (row operations as explicit StepNodes)
- Matrix multiplication, determinants

**Graph theory**
- BFS / DFS / Dijkstra with step traces
- Graph ↔ matrix views (adjacency, Laplacian)

## v0.4 — Platform & Plugins

- Stable plugin API guarantees
- Plugin discovery via Python entry points
- Curated community plugin gallery
- Renderer plugins (LaTeX, HTML, graph views)

## v0.5 — Visualization & Education

- Expression tree visualization
- Step graph visualization (DAG viewer)
- Classroom mode (shareable links, printable exports)
- Export to LaTeX / PDF

## How this maps to GitHub Issues

- Each bullet above maps to an epic label: `v0.2`, `v0.3`, etc.
- Issues should be written as user-facing outcomes ("render JSON reasoning DAG") plus acceptance criteria.
