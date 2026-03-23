---
name: init-repo
description: Initializes a governance-ready Python repository with uv, hatchling, ruff, mypy strict, pytest, GitHub Actions CI, and CLAUDE.md for AI-assisted development. Creates empty docs/ and scripts/ directories ready for governance. Use when user says "init a repo", "initialize a new project", "set up a new Python repo", "create project structure", "new repo", "bootstrap a repo", or "init repo". Do NOT use for adding governance docs (use init-base-docs), for existing project analysis (use repo-assimilation), or for non-Python projects.
---

# Init Repo

## Important

Follow these rules strictly.

- Always use uv. Never use pip.
- Always use hatchling as the build backend. Never use setuptools.
- Do not create a Makefile. The repo uses `uv run` for all tool execution.
- Do not create governance documentation (ADRs, CICs, protocols, standards). That is init-base-docs' job. Only create the empty `docs/` directory.
- If the target directory already exists and contains files, STOP and warn the user.
- Always convert the project name to kebab-case for the directory and snake_case for the Python package.
- Always initialize git and create the first commit. Do not leave an uncommitted repo.

## Purpose

Create the seed of a production-quality Python repository. Opinionated about tooling: uv for package management, hatchling for builds, ruff for linting, mypy strict for type safety. Prepares the directory structure for governance documentation but does not create it. Generates CLAUDE.md so AI assistants have accurate context from day one.

## Procedure

### Step 1: Gather Requirements

Ask the user for:
- **Project name** (will be converted to kebab-case for the directory, snake_case for the package)
- **Brief description** (one sentence)
- **Target directory** (default: current working directory)

If the user already provided these in their request, skip asking.

### Step 2: Verify Prerequisites

Check that `uv` is installed: run `uv --version`.

If uv is not available, STOP. Tell the user:
```
uv is required but not installed.
Install it: curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 3: Create Directory Structure

Create the following layout inside the target directory:

```
{project_name}/
├── src/
│   └── {package_name}/
│       ├── __init__.py
│       └── py.typed
├── tests/
│   ├── conftest.py
│   └── test_{package_name}.py
├── docs/
│   └── .gitkeep
├── scripts/
│   └── .gitkeep
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── pyproject.toml
├── CLAUDE.md
└── README.md
```

### Step 4: Populate Files

Use the templates from `references/templates.md`. Substitute:
- `{project_name}` with the kebab-case project name
- `{package_name}` with the snake_case package name
- `{description}` with the user's description

Write each file with the substituted content.

### Step 5: Generate CLAUDE.md

CLAUDE.md is the only file that benefits from creative adaptation beyond template substitution.

Start from the CLAUDE.md template in `references/templates.md`. Substitute the placeholders. If the user provided additional context about the project's domain, architecture, or intended purpose, incorporate it into the Project and Architecture sections.

The goal: an AI assistant reading CLAUDE.md cold should immediately understand what this project is, how to build it, and what principles govern it.

### Step 6: Initialize Git

In the project directory:
1. `git init`
2. `git add -A`
3. `git commit -m "Initial repository scaffold"`

### Step 7: Verify and Report

Run the quality checklist. Then report:
- List all created files
- Show next steps: `cd {project_name} && uv sync && uv run pytest`

## Quality Checklist

Before reporting success, verify every item:

- [ ] All files in the directory structure above exist
- [ ] `uv sync` succeeds in the project directory
- [ ] `uv run pytest` passes (the example test should pass)
- [ ] `uv run ruff check .` reports no violations
- [ ] `uv run mypy src/` reports no errors
- [ ] .gitignore includes `__pycache__/`, `*.pyc`, `.venv/`, `dist/`, `*.egg-info/`, `data/`, `.env`
- [ ] ci.yml uses uv for all operations (not pip)
- [ ] CLAUDE.md contains the project name, description, and accurate development commands
- [ ] `py.typed` marker exists in `src/{package_name}/`
- [ ] git repo is initialized with exactly one commit
- [ ] `docs/` and `scripts/` directories exist with `.gitkeep` files

## Error Handling

- **uv not installed:** STOP. Print install instructions (see Step 2). Do not fall back to pip.
- **Target directory exists with files:** STOP. Ask the user whether to proceed. Do not silently overwrite.
- **git init fails:** Report the error. The scaffold is still usable without git.
- **uv sync fails:** Check pyproject.toml for syntax errors. Report the specific error to the user.
- **Tests or linting fail:** Fix the issue in the generated files before reporting success. These should never fail on a fresh scaffold.

## Performance Notes

- Steps 3-4 are mechanical template substitution. Do not overthink them.
- Step 5 (CLAUDE.md) is the highest-value creative work. Make it genuinely useful.
- Run the full quality checklist. Every item. Do not skip verification.
