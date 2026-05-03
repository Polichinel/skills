# Register Risk: Detailed Phase Instructions

## Phase 1 -- Locate or Create Register

Search for the existing register in this order:

1. `reports/technical_risk_register.md`
2. `docs/risk_register.md`
3. Any `.md` file with "risk register" in its first heading

If found:
- Read the full register
- Parse header counts (Total, Open, Resolved)
- Parse all existing entry IDs to determine the next available ID
- Identify the highest C-xx and D-xx numbers
- Note the register's conventions section (if present) for formatting rules

If not found:
- Create `reports/technical_risk_register.md` with the standard template (see below)
- Create the governing ADR in `docs/ADRs/active/` (next available number)
- The ADR should formalize the register as a first-class governance artifact

### Standard register template (for creation):

```markdown
# Technical Risk Register

| Register Info     | Details                              |
|-------------------|--------------------------------------|
| Project           | [project name]                       |
| Owner             | [from user or git config]            |
| Last Updated      | [today's date]                       |
| Total Concerns    | 0                                    |
| Open Concerns     | 0                                    |
| Resolved Concerns | 0                                    |

---

## Tier Definitions

| Tier | Severity | Description |
|------|----------|-------------|
| 1 | Critical | Silent data corruption or model output correctness risk. Requires immediate attention. |
| 2 | High | Structural fragility that will cause failures under realistic change scenarios. |
| 3 | Medium | Maintainability or coupling issues that increase cost of change. |
| 4 | Low | Code quality concerns that do not affect correctness or reliability. |

---

## Open Concerns

(No concerns registered yet.)

---

## Disagreements

(No disagreements registered yet.)

---

## Resolved Concerns

(No resolved concerns yet.)

---

## Register Conventions

- **ID format:** `C-xx` for concerns, `D-xx` for disagreements. IDs are permanent — gaps in numbering indicate merged or resolved entries
- **Sources:** `repo-assimilation`, `expert-review`, `test-review`, `falsification-audit`, `clean-architecture-review`, `pr-review`, `tech-debt-audit`, `incident`
- **Resolution:** Move to "Resolved Concerns" with resolution date and summary when addressed
- **Header counts:** Manually maintained — update whenever a concern is added or resolved
- **Governed by:** [ADR number]
```

---

## Phase 2 -- Extract Findings

Collect risks from the current conversation context. Valid sources:

1. **Audit skill output:** Findings from expert-code-review, test-review, falsify, repo-assimilation, tech-debt-cleanup, or clean-architecture-review that appeared earlier in this conversation
2. **User-stated risks:** The user explicitly describes a risk or concern
3. **Prior analysis:** Code analysis performed earlier in this conversation that identified issues

For each finding, extract:
- **What:** The problem or risk (one sentence)
- **Where:** File path(s) and line numbers
- **Why it matters:** Impact if the risk materializes
- **Source:** Which skill or analysis produced this finding

Do not re-analyze code to find new risks. This skill registers findings, it does not discover them.

---

## Phase 3 -- Deduplicate

For each extracted finding, compare against every existing register entry:

**Exact duplicate:** Same location, same problem → Skip. Note in report.

**Location overlap:** New finding describes the same location but a different aspect → Register as new with cross-reference.

**Subsumption:** New finding is a specific instance of a broader existing concern (e.g., "bare except in file X" when "bare excepts across the codebase" exists) → Merge the specific location into the existing entry's Location field. Do not create a new entry.

**Causal overlap:** New finding is a symptom of the same root cause as an existing entry → Register as new but add cross-reference noting the shared root cause.

**No overlap:** → Register as new.

When merging into an existing entry:
- Add new location(s) to the Location field
- Update the narrative if the new finding adds significant information
- Do not change the tier unless the new finding provides evidence for a different tier
- Note the merge in the report

---

## Phase 4 -- Assign Tiers and Triggers

### Tier assignment

For each new concern, apply the tier criteria:

**Tier 1 test:** Does this risk cause silent data corruption or model output incorrectness with no error signal? If yes → Tier 1. This tier is rare and requires strong evidence.

**Tier 2 test:** Is there a specific, realistic change scenario that would cause a failure? Is the failure structural (not just inconvenient)? If yes → Tier 2.

**Tier 3 test:** Does this increase the cost of change for multiple developers? Does it affect maintainability or coupling? If yes → Tier 3.

**Tier 4 default:** Code quality observations that don't affect correctness or reliability → Tier 4.

**Consistency check:** After assigning a tier, compare against existing entries at the same tier. Does the new entry's severity match its peers? If a new Tier 3 entry is clearly less severe than all existing Tier 3 entries, it should probably be Tier 4.

### Trigger formulation

Write each trigger as: "When [specific developer action], [specific thing to check]."

**Good triggers:**
- "When adding a new decoder head, verify that both `__init__()` and `forward()` are updated"
- "When modifying `_valid_cell_indices()`, verify flip parity with `from_df()`"

**Bad triggers (rewrite these):**
- "Any change to this module" → too broad
- "When things break" → not actionable
- "Performance issues" → not a trigger

### Causal linking

If the register has a causal clusters section (added by review-rr), check whether the new entry belongs to an existing cluster. If so, note the cluster in a cross-reference.

---

## Phase 5 -- Append Entries

Write each new entry in the register's established format. Insert in the correct section:
- Concerns → under `## Open Concerns`, after the last existing concern
- Disagreements → under `## Disagreements`, after the last existing disagreement

For each entry:
1. Use the next available sequential ID (C-xx or D-xx)
2. Include all required fields from the schema
3. Write the narrative paragraph grounded in specific code
4. Add cross-references to related entries if applicable

After all entries are written:
1. Update `Last Updated` in the header to today's date
2. Update `Total Concerns` count
3. Update `Open Concerns` count
4. Verify counts match actual entry counts

If the register file is under a gitignored directory (e.g., `reports/`), use `git add -f` when staging.

---

## Phase 6 -- Report

Present the registration summary to the user:

```
## Registration Summary

| Action | Count |
|--------|-------|
| New entries registered | X |
| Merged into existing | Y |
| Skipped (duplicate) | Z |

### New Entries
| ID | Tier | Title | Source |
|----|------|-------|--------|

### Merged
| Existing ID | Addition | Reason |
|-------------|----------|--------|

### Skipped
| Finding | Existing ID | Reason |
|---------|-------------|--------|

### Header Update
- Total: [old] → [new]
- Open: [old] → [new]
```
