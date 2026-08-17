# Claude Code Skills

A collection of Claude Code skills for software engineering governance, strategic writing, analysis, and workflow automation.

## Skills

### Repository Lifecycle

| Skill | Purpose |
|-------|---------|
| **init-repo** | Initialize a governance-ready Python repository (uv, hatchling, ruff, mypy, CLAUDE.md) |
| **init-base-docs** | Bootstrap constitutional ADRs, CIC infrastructure, contributor protocols, and standards |
| **adopt-base-docs** | Retrofit governance documentation onto an existing project |
| **ship-it** | Gated pipeline: lint, test, stage, commit, push |

### Analysis

| Skill | Purpose |
|-------|---------|
| **repo-assimilation** | Build a structured mental model of a repository through 8 sequential phases |
| **expert-code-review** | Multi-perspective review from 8 canonical engineering viewpoints |
| **test-review** | Audit test coverage and quality from 5 expert perspectives |
| **review-base-docs** | Detect drift between governance docs and current code |
| **review-diff** | Pre-ship changeset review for maintainability |
| **falsify** | Popperian falsification audit against claims about software behavior |
| **expert-method-review** | Library-grounded multi-persona critique of ML/research design and methodology |

### Strategic Writing

| Skill | Purpose |
|-------|---------|
| **writing-harness** | Initialize the artifact substrate for strategic documents (DECISIONS.md, FINDINGS.md, MANIFESTO.md, anchors/, failure mode catalog) |
| **strategic-draft** | Collaborative document drafting through structured Q&A with green/red spectrum tracking, three-question mechanism, and full harness artifact management |
| **review-harness** | Sync harness artifacts against the current document (update stale statuses) or prioritize what to work on next |
| **persona-critique** | Multi-persona critique of a draft: domain panels, craft personas, and a bespoke Scout |
| **verify-sources** | Verify every citation against local source PDFs; maintains a citation ledger |

**How to use:** The writing skills share an artifact harness (`_dev_materials/<document>/`) that tracks decisions, findings, manifesto entries, and precision anchors across sessions.

- `/strategic-draft` — Start or resume drafting. Auto-bootstraps a harness if none exists. Every paragraph gets three questions (ground truth, strategy, reader impact). Sharp formulations are anchored, decisions recorded, and the green/red oscillation between generative and critical modes is tracked.
- `/review-harness sync` — After a drafting session, compare harness artifact statuses against the actual document text and update what's stale (decisions resolved but still marked Open, findings addressed but still Pending, manifesto entries landed but not verified).
- `/review-harness prioritize` — Get a ranked action plan: what to resolve, draft, or fix next, ordered by what blocks what.
- `/writing-harness` — Initialize the artifact structure deliberately (seed manifesto tiers, create anchors from reference materials) before drafting begins.
- `/persona-critique` — Deploy domain expert and writing craft personas to critique a draft. Produces structured findings in `critiques/` that feed the harness pipeline.
- `/verify-sources` — Verify every citation against local source PDFs. Maintains a citation ledger in `citations/`.
- `/falsify` — Audit claims in the harness: decisions become falsifiable assertions, landed findings become verification targets, implicit manifesto entries become negative probes.

### Risk Management

| Skill | Purpose |
|-------|---------|
| **register-risk** | Register risks and concerns into the repository's technical risk register |
| **review-rr** | Review, curate, and prioritize the risk register (triage, strategic, or prioritize mode) |

### Research

| Skill | Purpose |
|-------|---------|
| **library** | Claim-centric research library: manage papers, extract claims, verify citations, semantic search |
| **rnd-dossier** | Scaffold and maintain R&D experimentation dossiers (pre-register, log, promote to ADR) |

### Maintenance

| Skill | Purpose |
|-------|---------|
| **tech-debt-cleanup** | Structured identification and safe cleanup of technical debt |
| **autoresearch** | Autonomous experiment loop to optimize a single metric |

### Coordination

| Skill | Purpose |
|-------|---------|
| **thingit** | Run a þing — the cross-repo deliberation protocol for decisions spanning repositories |

### Knowledge Graphs

| Skill | Purpose |
|-------|---------|
| **graphify** | Turn any folder of files into a navigable knowledge graph with community detection and audit trail |


## Skill Seams — Responsibility Boundaries

Skills compose through filesystem artifacts, not programmatic APIs. Where responsibilities overlap, one skill owns the concern and others delegate or consume its output.

| Boundary | Skill A owns | Skill B owns | Seam |
|----------|-------------|-------------|------|
| **verify-sources** vs **library verify** | Document-level citation audit (batch, harness-integrated) | Single-claim targeted verification (calibrated confidence, drift analysis) | verify-sources resolves PDFs via library sidecars; delegates to `/library verify` for claims where the library has extracted evidence |
| **expert-method-review** vs **persona-critique** | Design/methodology: *what to build and why* (pre-implementation) | Writing/argument: *how it's argued* (post-draft) | Shared named-persona convention; method-review seats from `references/personas.md`, persona-critique from its own domain panels. Same figure carries the same documented stance in both |
| **expert-method-review** vs **falsify** | Generative: proposes what's missing, surfaces disagreements | Destructive: tries to break specific claims | Method-review precedes pre-registration; falsify attacks claims after |
| **rnd-dossier** vs **expert-method-review** | Experiment lifecycle governance (scaffold, pre-register, log, promote) | Design critique that shapes what's worth testing | Dossier orchestrates; method-review critiques `02_design` before pre-registration |
| **rnd-dossier** vs **register-risk** | Records experiment outcomes and methodology gaps | Owns the risk register (dedup, tiering, linking) | Dossier outputs register-compatible risks; `register-risk` handles intake |
| **library** vs all research/writing skills | Data layer: papers, claims, metadata, search index, verification engine | Each skill's domain concern | Skills consume library via `/library search`, `/library find`, `/library verify`, sidecar reads. No skill duplicates library storage or search |

## Installation

Place this directory at `~/.claude/skills/` or upload individual skill folders via Claude.ai Settings > Capabilities > Skills.

## Skill Structure

Each skill follows the [progressive disclosure](https://claude.com/blog/skills) pattern:

```
skill-name/
├── SKILL.md              # Instructions with YAML frontmatter
└── references/           # Detailed docs loaded on demand
```

## Philosophy

These skills are grounded in explicit architectural governance:

- **Fail loud** over silent failure
- **Declare** semantics, don't infer them
- **Testing** is mandatory critical infrastructure
- **Intent contracts** for non-trivial classes
- **AI agents** are untrusted contributors under human accountability
