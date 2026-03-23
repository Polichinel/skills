---
name: review-diff
description: Reviews a git changeset for maintainability and readability before shipping. Checks naming, complexity, error handling, duplication, pattern consistency, and contract alignment. Use when user says "review this diff", "review my changes", "check this diff", "is this diff ready", "review before shipping", "changeset review", "pre-commit review", or "are these changes clean". Do NOT use for whole-codebase review (use expert-code-review), for test assessment (use test-review), for documentation audit (use review-base-docs), or for committing/pushing (use ship-it).
---

# Review Diff

## Important

Follow these rules strictly.

- Do not modify any files. This skill reviews and reports only.
- Determine the diff scope before analyzing. Consult `references/scope.md` for scope detection logic.
- Read surrounding code in affected files to assess pattern consistency. Do not review the diff in isolation.
- Apply all check categories (A-E) to every changed hunk. Category F only if CICs exist for affected classes.
- Ground every finding in a specific file, line range, and changed code. No vague observations.
- Assign a severity to every finding: critical, warning, or suggestion.
- Produce a single verdict: CLEAN, REVIEW, or HOLD.

## Critical Constraint

This skill is read-only. It produces a review report. It does not create, modify, or delete any files. All recommendations are for the user to act on before shipping.

## Purpose

Review a git changeset for semantic quality that linters cannot catch: misleading names, swallowed errors, mixed abstractions, duplicated logic, pattern violations, and contract drift. Lightweight enough to run before every ship-it.

## Procedure

Execute these 3 phases sequentially. For detailed check criteria, consult `references/checks.md`. For scope detection, consult `references/scope.md`.

1. **Scope and Context** -- Determine diff scope, capture content, identify affected files, load CICs if available
2. **Analysis** -- Apply check categories A-F to each changed hunk with surrounding context
3. **Report** -- Compile findings, assign severities, produce verdict

## Required Output Structure

1. Diff Summary (scope, files changed, lines +/-, CICs loaded)
2. Findings (per finding: file, line range, category, severity, description, recommendation)
3. Contract Alerts (only if CICs exist: CIC-governed classes touched, API changes needing CIC update)
4. Verdict (CLEAN / REVIEW / HOLD + finding counts by severity and category)

## Check Categories

- **A -- Naming and Clarity:** Misleading names, ambiguous names, naming inconsistency, unclear booleans, redundant comments
- **B -- Complexity and Structure:** Multi-responsibility functions, deep nesting, long functions, mixed abstraction levels
- **C -- Error Handling:** Swallowed exceptions, overly broad catches, missing error handling, silent fallbacks
- **D -- Duplication and Reuse:** Logic duplicating existing code, copy-paste variations, magic values
- **E -- Pattern Consistency:** Deviates from module patterns, different strategies than surrounding code
- **F -- Contract Alignment (conditional):** New/changed public API not in CIC, CIC guarantee violations, undocumented failure modes. Skipped if no CICs exist.

## Severity Levels

- **Critical:** Silent error swallowing, data loss risk, contract violation, logic duplication of critical code. Should block shipping.
- **Warning:** Misleading names, mixed abstractions, missing error context, pattern deviation. Address before shipping.
- **Suggestion:** Minor naming improvements, comment quality, optional extraction. Nice-to-have.

## Verdict

- **CLEAN:** No findings above suggestion severity. Ship it.
- **REVIEW:** Warnings found. Consider addressing before shipping.
- **HOLD:** Critical findings. Address before shipping.

## Performance Notes

- This skill should be fast. Do not read the entire codebase -- only the diff and surrounding context in affected files.
- For duplication checks (Category D), search the codebase for similar patterns but limit to the same package/module first, then broaden only if the pattern is significant.
- Category F is skipped entirely when no CICs exist. Do not warn about missing CICs -- that is not this skill's concern.
- When the diff is large (20+ files), prioritize: error handling (C) and contract alignment (F) first, then naming (A) and complexity (B), then duplication (D) and consistency (E).
