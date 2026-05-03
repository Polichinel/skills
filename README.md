# Claude Code Skills

A collection of Claude Code skills for software engineering governance, analysis, and workflow automation.

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

### Strategic Writing

| Skill | Purpose |
|-------|---------|
| **writing-harness** | Initialize the artifact substrate for strategic documents (DECISIONS.md, FINDINGS.md, MANIFESTO.md, anchors/, failure mode catalog) |
| **strategic-draft** | Collaborative document drafting through structured Q&A with green/red spectrum tracking, three-question mechanism, and full harness artifact management |

**How to use:** Run `/strategic-draft` to start drafting a document. The skill auto-bootstraps a writing harness if one doesn't exist, asks three setup questions (title, audience, failure conditions), then enters a Q&A loop where every paragraph gets questioned on ground truth, strategy, and reader impact. Sharp formulations are anchored, decisions are recorded, and the green/red oscillation between generative and critical modes is tracked behaviorally. Run `/writing-harness` separately if you want to initialize the artifact structure without drafting.

### Risk Management

| Skill | Purpose |
|-------|---------|
| **register-risk** | Register risks and concerns into the repository's technical risk register |
| **review-rr** | Review, curate, and prioritize the risk register (triage, strategic, or prioritize mode) |

### Maintenance

| Skill | Purpose |
|-------|---------|
| **tech-debt-cleanup** | Structured identification and safe cleanup of technical debt |
| **autoresearch** | Autonomous experiment loop to optimize a single metric |

### Knowledge Graphs

| Skill | Purpose |
|-------|---------|
| **graphify** | Turn any folder of files into a navigable knowledge graph with community detection and audit trail |

### Utility

| Skill | Purpose |
|-------|---------|
| **hello-world** | Demo skill for testing |

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
