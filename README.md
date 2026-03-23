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

### Maintenance

| Skill | Purpose |
|-------|---------|
| **tech-debt-cleanup** | Structured identification and safe cleanup of technical debt |
| **autoresearch** | Autonomous experiment loop to optimize a single metric |

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
