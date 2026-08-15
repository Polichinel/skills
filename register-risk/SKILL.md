---
name: register-risk
description: Registers risks, concerns, and disagreements into the repository's technical risk register. Creates the register and its governing ADR if they don't exist. Deduplicates against existing entries, assigns provisional tiers, validates trigger quality, and links to causal clusters. Use when user says "register this risk", "add to risk register", "register these findings", "register all items", "track this concern", or "log this risk". Do NOT use for reviewing or auditing the register (use review-rr), for finding risks (use expert-code-review, test-review, falsify, repo-assimilation, or tech-debt-cleanup), or for fixing risks (fix the code directly).
---

# Register Risk

## Important

Follow these rules strictly.

- Do not invent risks. Only register risks that are present in the conversation context (from audit skill output, user statements, or code analysis already performed).
- Do not register duplicates. Before appending, check every existing entry for overlap. If a new finding overlaps an existing concern, update the existing entry instead of creating a new one.
- Do not assign Tier 1 or Tier 2 without explicit justification grounded in silent-corruption or structural-fragility evidence.
- Do not modify source code. This skill writes only to the register file and (if creating) the ADR.
- Do not skip the deduplication check. It is the primary quality gate.
- Always update header counts after modifying the register.
- Use `git add -f` for the register file if it lives under a gitignored directory (e.g., `reports/`).

## Purpose

Single intake funnel for risk registration. All audit skills (expert-code-review, test-review, falsify, repo-assimilation, tech-debt-cleanup, review-diff) produce findings that may warrant tracking. This skill is the controlled gate between "finding identified" and "finding tracked," enforcing deduplication, tier consistency, trigger quality, and causal linking.

## Procedure

Execute these 6 phases sequentially. For detailed instructions, consult `references/phases.md`. For the entry schema and tier definitions, consult `references/schema.md`.

1. **Locate or Create Register** -- Find the existing register, or create it with header, tier definitions, empty sections, and governing ADR
2. **Extract Findings** -- Collect risks from conversation context (audit output, user statements, prior analysis)
3. **Deduplicate** -- Compare each finding against every existing entry. Merge overlapping findings into existing entries.
4. **Assign Tiers and Triggers** -- Apply tier criteria with explicit rationale. Write actionable triggers. Link to causal clusters if applicable.
5. **Append Entries** -- Write new entries and update existing entries. Update header counts.
6. **Report** -- Summarize what was registered, merged, and skipped.

## Required Output Structure

1. Registration Summary (counts: new entries, merged into existing, skipped as duplicate)
2. New Entries (table: ID, tier, title, source)
3. Merged Entries (table: existing ID, what was added, why merged)
4. Skipped Entries (table: finding, reason skipped)
5. Updated Header (before/after counts)

## Entry Schema

Every concern entry must have these fields. Consult `references/schema.md` for field definitions, valid values, and formatting rules.

| Field | Required | Description |
|-------|----------|-------------|
| ID | Yes | `C-xx` for concerns, `D-xx` for disagreements |
| Tier | Yes (concerns only) | 1-4 with explicit rationale |
| Source | Yes | Skill or audit that produced the finding |
| Trigger | Yes (concerns only) | Specific future action that makes this concern acute |
| Location | Yes (concerns only) | File path(s) with line numbers where applicable |
| Narrative | Yes | Grounded description of the risk |
| Cross-refs | If applicable | Links to related concerns or disagreements |

## Tier Definitions

| Tier | Severity | Criteria |
|------|----------|----------|
| 1 | Critical | Silent data corruption or model output incorrectness. No error signal. Requires immediate attention. |
| 2 | High | Structural fragility that will cause failures under realistic change scenarios. Clear trigger exists. |
| 3 | Medium | Maintainability or coupling issues that increase cost of change. Multiple developers affected. |
| 4 | Low | Code quality observations. Single-developer scope. No correctness or reliability impact. |

## Deduplication Rules

A new finding overlaps an existing entry when:
- It describes the same code location AND the same problem type
- It is a more specific instance of a broader existing concern (merge as a location update)
- It describes a symptom of an existing root-cause entry

When overlap is detected:
- If the new finding adds information (new locations, stronger evidence): update the existing entry
- If the new finding is strictly contained by the existing entry: skip and note in report
- If the new finding partially overlaps: register as new but add cross-reference to the related entry

## Trigger Quality Gate

Reject triggers that are:
- **Perpetual:** Always true today (e.g., "any change to this module"). Rewrite as a specific future action.
- **Vague:** Don't specify what action or what to check. Rewrite with concrete scenario.
- **Symptoms:** Describe the consequence, not the cause. Rewrite as the action that causes the consequence.

A good trigger answers: "What specific thing might a developer do next that would make this concern a problem?"

## Performance Notes

- Speed matters. This skill should be fast — it's the intake step, not the analysis step.
- Do not re-analyze code. Trust the source skill's analysis. Your job is formatting, deduplication, and tier assignment.
- When registering many findings at once (e.g., after expert-code-review), batch the deduplication check — compare all new findings against all existing entries before writing any.
- If the register has causal clusters (added by review-rr), assign new entries to clusters where applicable.
