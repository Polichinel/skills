# Review Diff: Scope Detection

## Determining What to Review

Resolve the diff scope using this priority order. Stop at the first match.

### 1. User-specified scope

If the user provides an explicit scope, use it:
- "review diff against main" → `git diff main...HEAD`
- "review staged changes" → `git diff --cached`
- "review last commit" → `git diff HEAD~1`
- "review last 3 commits" → `git diff HEAD~3`
- "review changes in src/parser.py" → `git diff -- src/parser.py`

### 2. Staged changes

Run `git diff --cached --stat`. If non-empty, the scope is staged changes.

This is the most common pre-commit case. The user has staged their work and wants it reviewed before committing.

Capture the full diff: `git diff --cached`

### 3. Unstaged changes

Run `git diff --stat`. If non-empty, the scope is unstaged changes.

The user is still working but wants a check on their progress.

Capture the full diff: `git diff`

### 4. Last commit

Run `git diff HEAD~1 --stat`. If non-empty, the scope is the most recent commit.

The user just committed and wants a post-commit review.

Capture the full diff: `git diff HEAD~1`

### 5. Nothing to review

If all of the above are empty, **STOP** and tell the user:

> "No changes found to review. Stage your changes, or specify a scope (e.g., 'review diff against main')."

## Reporting the Scope

Always state the resolved scope at the top of the report so the user knows exactly what was reviewed:

- "Reviewing: staged changes (N files)"
- "Reviewing: unstaged changes (N files)"
- "Reviewing: diff against main (N files, M commits)"
- "Reviewing: last commit `abc1234` (N files)"

## Large Diffs

If the diff touches more than 30 files, warn the user:

> "Large diff (N files). Prioritizing error handling and contract checks. For a full review, consider running expert-code-review on the whole codebase."

Still review all files, but apply the priority order from SKILL.md Performance Notes.
