# Register Risk: Entry Schema and Formatting

## Concern Entry Format

```markdown
### C-XX: [Short descriptive title]

| Field | Value |
|-------|-------|
| ID | C-XX |
| Tier | [1-4] |
| Source | [source] ([date]) |
| Trigger | [specific future action that makes this acute] |
| Location | [file:line or file:line-range, comma-separated for multiple] |

[Narrative paragraph: 2-5 sentences grounded in specific code. Describe what the risk is, why it matters, and what the current mitigation (if any) is. If referencing external sources (books, standards), include specific citations.]

[Optional: "See also C-XX (related concern)." or "Part of causal cluster: [cluster name]."]
```

## Disagreement Entry Format

```markdown
### D-XX: [Short descriptive title]

| Field | Value |
|-------|-------|
| ID | D-XX |
| Source | [source] ([date]) |
| Perspectives | [Name1 (position — brief argument), Name2 (position — brief argument)] |
| Resolution | [Current resolution or "Unresolved"] |
```

## Resolved Entry Format

```markdown
### C-XX: [Original title] — RESOLVED

| Field | Value |
|-------|-------|
| ID | C-XX |
| Resolved | [date] |
| Resolution | [1-2 sentence summary of what was done] |
```

---

## Field Definitions

### ID

Format: `C-xx` for concerns, `D-xx` for disagreements. Sequential within each prefix. IDs are permanent — never reuse an ID, even after resolution or merge. Gaps in numbering are expected and indicate merged or resolved entries.

### Tier (concerns only)

| Tier | Label | Criteria | Examples |
|------|-------|----------|----------|
| 1 | Critical | Silent data corruption or model output incorrectness with no error signal | Wrong spatial coordinates in output; silent numeric overflow; inverted geographic data |
| 2 | High | Structural fragility causing failures under realistic change scenarios | Implicit coupling between two operations that must be symmetric; untested arithmetic that silently corrupts training data |
| 3 | Medium | Maintainability or coupling issues increasing cost of change | God functions; duplicated setup code; framework coupling blocking tests; SRP violations affecting multiple developers |
| 4 | Low | Code quality observations with no correctness or reliability impact | Naming opacity; in-place mutation in non-production paths; missing but non-critical tests; style violations |

**Tier assignment rules:**
- Never assign Tier 1 without identifying the specific path by which data corruption occurs silently
- Tier 2 requires a concrete trigger scenario, not just "this could break"
- Tier 3 vs Tier 4 hinge on scope: Tier 3 affects multiple developers or modules; Tier 4 is localized
- When in doubt between two tiers, assign the lower tier and note the uncertainty

### Source

The audit skill or activity that produced the finding. Valid values:

| Source value | Producing skill |
|-------------|----------------|
| `repo-assimilation` | repo-assimilation |
| `expert-review` | expert-code-review |
| `test-review` | test-review |
| `falsification-audit` | falsify |
| `tech-debt-audit` | tech-debt-cleanup |
| `pr-review` | review-diff or external PR review |
| `incident` | Production incident or operational failure |
| `manual` | User-reported or ad-hoc identification |

Always include the date in parentheses: `expert-review (2026-04-08)`

### Trigger (concerns only)

A specific future action that makes this concern acute. Must be:
- **Actionable:** Names what a developer would do (not what would happen as a consequence)
- **Specific:** References concrete files, functions, or operations
- **Falsifiable:** You could determine whether the trigger has occurred

**Pattern:** "When [someone] [does specific action], [what to check or what breaks]"

**Anti-patterns to reject:**
- "Any change to X" — too broad. Which specific change?
- "When things go wrong" — tautological
- "Performance degrades" — that's a consequence, not a trigger
- Always-true conditions — if it's true today, it's a standing concern, not a triggered risk

### Location (concerns only)

File paths with line numbers or ranges. Use backtick formatting.

- Single location: `` `volume_handler.py:615-635` ``
- Multiple locations: `` `train_model.py:105,199,242`, `hydranet_inference.py:122,137` ``
- Module-level: `` `views_hydranet/utils/` (20 of 25 source files) ``

### Narrative

The body text below the field table. Requirements:
- 2-5 sentences for Tier 4; 3-8 sentences for Tier 1-3
- Must reference specific code (function names, patterns, values)
- Must state the risk, not just describe the code
- If citing external sources (Clean Architecture, etc.), include chapter and page numbers
- End with current mitigation if one exists ("Currently mitigated by...", "Guarded indirectly by...")

### Cross-references

Optional line after the narrative: "See also C-XX (brief reason for link)."

Use cross-references when:
- Two concerns share a root cause
- One concern is a specific instance of a broader pattern
- A concern relates to a disagreement (C-xx → D-xx)
- Two concerns affect the same file/class from different angles

---

## Formatting Rules

1. Use `---` (horizontal rule) between entries
2. Use `###` (h3) for entry headings
3. Use pipe tables for field metadata
4. Wrap file paths and code references in backticks
5. One blank line between the field table and the narrative
6. One blank line between the narrative and the horizontal rule
7. Concerns and disagreements in separate sections (never interleave)
8. Resolved entries in their own section with the ` — RESOLVED` suffix in the heading
