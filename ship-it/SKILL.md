---
name: ship-it
description: Validates and ships local changes through a gated pipeline of linting (ruff), import contracts (lint-imports, only where a repo declares them), testing (pytest), staging, committing, and pushing. Use when user says "ship it", "commit and push", "push my changes", "finalize changes", "land this", or "ship my work". Do NOT use for code review, refactoring, running tests in isolation, or deploying to production.
---

# Ship It

## Important

Follow these rules strictly.

- Never skip a gate. If lint or tests fail, stop and report.
- Never silently ignore untracked files.
- Never push without explicit user confirmation.
- Never use `git add .` or `git add -A`.
- Match the repository's existing commit message style (check `git log --oneline -10`).
- If the repository has no commits yet, use plain descriptive messages.

## Procedure

Execute these steps sequentially. Each step gates the next.

### Step 1 — Lint

Run `ruff check .`

If lint errors exist: **STOP**. Report the errors. Do not proceed.

### Step 1.5 — Import contracts (only if the repo declares them)

Check whether `pyproject.toml` contains a `[tool.importlinter]` section.

**If it does not: skip this step silently.** Say nothing. Most repos have no contract, and
a gate that announces itself doing nothing is noise.

**If it does:** run `lint-imports` (`uv run lint-imports` or `poetry run lint-imports`,
matching how the repo runs its other tools).

If any contract is broken: **STOP**. Report the contract name and the exact import chain
the tool names. Do not proceed.

Why this sits between lint and test: a broken contract is an architecture violation, not a
test failure, and it is cheaper to see before the suite runs. CI enforces the same thing —
without this step a repo can ship a violation locally and only learn about it from a red
build after the push.

### Step 2 — Test

Run `pytest`

If any tests fail: **STOP**. Report the failures. Do not proceed.

### Step 3 — Status Check

Run `git status`

If working tree is clean: **STOP**. Report "Nothing to commit."

If untracked files exist that are not in .gitignore:
**STOP**. List the untracked files and ask the user:
- Which files to stage (by name or pattern)
- Whether any should be added to .gitignore instead
- Whether to proceed without them

Do not proceed until the user responds.

### Step 4 — Stage

Run `git add -u` to stage all tracked modified/deleted files.

If the user specified untracked files to include in Step 3, stage those by name.

Show `git diff --cached --stat` so the user can see what will be committed.

### Step 5 — Commit

Check `git log --oneline -10` to determine the repo's commit message style.

Write a commit message that:
- Summarizes what changed and why (not just which files)
- Is honest about the scope (don't inflate small changes)
- Matches the repo's existing style (conventional commits, plain, etc.)

Create the commit.

### Step 6 — Push

Show the user:
- The commit hash and message
- The target remote and branch (`origin/<current-branch>`)

Ask: **"Push to origin?"**

- If yes: run `git push`
- If no: stop. The commit stays local.

## Failure Recovery

If any step fails unexpectedly:
- Report exactly what failed and why
- Do not attempt to fix it automatically
- Do not proceed to the next step
