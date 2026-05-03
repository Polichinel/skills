# Review Risk Register: Detailed Phase Instructions

## Phase 1 -- Structural Integrity

Read the full register. Check each of the following:

### Header accuracy

- Parse `Total Concerns`, `Open Concerns`, `Resolved Concerns` from the header table
- Count actual `### C-xx` entries in each section
- Verify: Total = Open + Resolved
- Verify: Open count matches entries under `## Open Concerns`
- Verify: Resolved count matches entries under `## Resolved Concerns`
- Check `Last Updated` date — flag if more than 90 days old

### Section ordering

Verify sections appear in this order:
1. `## Tier Definitions`
2. `## Open Concerns`
3. `## Disagreements`
4. `## Resolved Concerns`
5. `## Register Conventions`

Optional section (if present):
- `## Causal Clusters` — between Tier Definitions and Open Concerns

Flag any concerns appearing under the wrong section heading (e.g., C-entries under Disagreements).

### ID sequencing

- All C-xx IDs should be sequential with acknowledged gaps
- All D-xx IDs should be sequential with acknowledged gaps
- No duplicate IDs
- Resolved entries should retain their original ID
- IDs in the Resolved section should not also appear in Open Concerns

### Formatting compliance

- Every entry has the required field table (ID, Tier, Source, Trigger, Location for concerns; ID, Source, Perspectives, Resolution for disagreements)
- Every entry has a narrative paragraph below the field table
- `---` separators between entries
- Backtick-wrapped file paths and code references
- Source field includes date in parentheses

### Cross-reference integrity

- Every "See also C-XX" reference points to an entry that exists
- Every "See also D-XX" reference points to a disagreement that exists
- Resolved entries referenced by other entries are noted (not dangling)

---

## Phase 2 -- Deduplication Scan

Compare all open entries pairwise. For N entries, this is O(N²) but the register is small enough for exhaustive comparison.

### Overlap types to detect

**Location overlap:** Two entries reference the same file and overlapping line ranges.
- Example: C-13 (`volume_handler.py:615-635`) and C-14 (`volume_handler.py:637-653`) — related but distinct methods. Not duplicates.
- Example: C-21 (`train_model.py:214`) and a hypothetical C-34 (`train_model.py:214`) — exact location match. Duplicate.

**Problem type overlap:** Two entries describe the same type of problem in different locations.
- Example: C-13 (in-place mutation of `_permute`) and C-14 (in-place mutation of `flip`) — same problem type, different methods. Related, not duplicate. Should cross-reference.

**Subsumption:** One entry is a strict subset of another.
- Example: "bare except in file X" is subsumed by "bare except in 3 files including file X." The specific entry should be merged into the broader one.

### Output per finding

For each detected overlap:
- Entry pair (IDs)
- Overlap type (location / problem type / subsumption)
- Recommended action (merge / cross-reference / keep separate)
- Rationale (one sentence)

---

## Phase 3 -- Report (Triage)

If in triage mode, compile findings from Phases 1-2 and present:

```
## Triage Report

### Structural Checks
| Check | Status | Detail |
|-------|--------|--------|
| Header counts | PASS/FAIL | [expected vs actual] |
| Section ordering | PASS/FAIL | [what's wrong] |
| ID sequencing | PASS/FAIL | [duplicates or issues] |
| Formatting | PASS/FAIL | [entries with issues] |
| Cross-references | PASS/FAIL | [broken refs] |

### Duplicates
[table of findings or "None detected"]

### Verdict: CLEAN / NEEDS FIX
```

If NEEDS FIX, ask: "Want me to apply these fixes?"

---

## Phase 4 -- Tier Calibration (Strategic only)

For each tier level (1 through 4), read all entries at that tier and check:

### Internal consistency

Do all entries at the same tier have comparable severity? Specifically:
- Are all Tier 2 entries structural fragilities with realistic triggers?
- Are all Tier 3 entries maintainability concerns affecting multiple developers?
- Is the Tier 3/4 boundary clean? (Tier 3 = multi-developer scope, Tier 4 = localized)

### Cross-tier comparison

For each entry, ask: "Is there an entry at a different tier that has clearly comparable severity?" If so, one of them is mis-tiered.

Common patterns:
- **Silent data risk at Tier 4:** If an entry describes behavior where incorrect output is produced without error signals, it should be Tier 1 or 2, not 4.
- **Code style at Tier 3:** If an entry describes a naming or formatting concern with no maintainability impact beyond the immediate author, it should be Tier 4, not 3.

### Rationale check

For Tier 1 and 2 entries, verify that the narrative provides explicit evidence for the tier assignment:
- Tier 1: Identifies the specific path by which data corruption occurs silently
- Tier 2: Identifies the specific change scenario that would cause failure

If the evidence is missing, flag for tier downgrade or narrative enhancement.

### Output

Table of proposed changes:
| ID | Current Tier | Proposed Tier | Rationale |
|----|-------------|---------------|-----------|

---

## Phase 5 -- Causal Clustering (Strategic only)

This is the highest-value phase. It transforms the register from a flat list into a strategic tool.

### Identify root causes

Read all open entries and group by shared root cause. A root cause is shared when:
- Fixing one underlying issue would resolve or significantly reduce multiple entries
- Multiple entries describe symptoms of the same structural decision or omission
- Multiple entries affect the same component for different reasons (suggesting the component itself is the problem)

### Name each cluster

Give each cluster a descriptive name that identifies the root cause, not the symptoms.

**Good cluster names:**
- "VolumeHandler responsibility accumulation"
- "Config validation gap between Pydantic and consumption"
- "Exception handling doctrine undefined"

**Bad cluster names:**
- "VolumeHandler concerns" — too vague
- "Testing gaps" — too broad
- "Various issues" — useless

### Assess cluster gravity

For each cluster:
- Count of entries (raw size)
- Highest tier in the cluster (severity ceiling)
- Would fixing the root cause resolve all entries, or only reduce them?
- Is there a single refactor that addresses the root cause?

### Output

```
### Causal Cluster: [Name]

**Root cause:** [One sentence describing the underlying structural issue]
**Entries:** C-XX, C-XX, C-XX, D-XX
**Highest tier:** [N]
**Fix strategy:** [One sentence: what refactor or decision would address this]
**Resolution scope:** [Full — fixes all entries / Partial — reduces but doesn't eliminate]
```

### Recommendation

If the register has more than 3 clusters with 4+ entries each, recommend adding a `## Causal Clusters` section to the register itself (between Tier Definitions and Open Concerns) as a permanent navigation aid.

---

## Phase 6 -- Trigger Quality (Strategic only)

Audit every trigger field against the quality criteria:

### Classification

For each trigger, classify as:
- **Actionable:** Specific future action + what to check. Good.
- **Perpetual:** Always true today. Needs rewrite.
- **Vague:** Doesn't specify the action or the check. Needs rewrite.
- **Compound:** Multiple triggers bundled. Should be split or prioritized.
- **Symptomatic:** Describes consequence, not cause. Needs inversion.

### Proposed rewrites

For each non-actionable trigger, propose a rewrite following the pattern:
"When [specific developer action], [specific thing to verify or risk to check]."

### Output

Table:
| ID | Current Trigger | Classification | Proposed Rewrite |
|----|----------------|----------------|------------------|

---

## Phase 7 -- Signal-to-Noise (Strategic only)

Assess whether every entry warrants formal register tracking.

### Criteria for register-worthy entries

A concern belongs in the register if:
- It could cause silent correctness failures (Tier 1-2)
- It requires coordination between multiple people to fix (Tier 3)
- Its trigger is non-obvious — someone could hit it without realizing
- It's a recurring theme across audits (tracked to prevent regression)

### Criteria for tech-debt backlog (not register)

A concern belongs in a lighter-weight tracker if:
- It's a localized code quality observation (one file, one developer)
- The fix is obvious and mechanical (rename, add type hint, remove dead code)
- The trigger is perpetual (it's always true, so there's no "activation" event)
- It's documented primarily for completeness, not for risk management

### Demotion target

Before recommending demotions, check whether the project has an existing tech-debt backlog:

1. Check for `reports/tech_debt_backlog.md` or similar
2. Check for GitHub issues labeled `tech-debt` or `backlog`
3. Check for a TODO/backlog section in CLAUDE.md or similar project files

If a backlog exists: recommend demotion to that specific location.
If no backlog exists: note this in the output. Recommend either (a) creating a lightweight `reports/tech_debt_backlog.md` (a simple table: ID, title, location, source — no tier, no trigger, no narrative), or (b) keeping entries in the register but adding a `[backlog]` tag to acknowledge they're tracked for completeness, not active risk management.

Do not create the backlog file — that's the user's decision.

### Output

List of entries recommended for demotion, with rationale and target:
| ID | Title | Reason for Demotion | Target |
|----|-------|---------------------|--------|

Note: This is a recommendation. The user decides whether to move entries.

---

## Phase 8 -- Report (Strategic)

Compile all findings into the Required Output Structure (see SKILL.md).

### Blind Spot Analysis

After completing all other phases, assess what risk categories are NOT represented in the register. Consider:

- **Data provenance:** Are upstream data contracts validated?
- **Reproducibility:** Are random seeds, hardware dependencies, and deterministic execution addressed?
- **Concurrency:** If the system could run in parallel, are shared-state risks tracked?
- **Deployment:** Are rollback, versioning, and operational risks tracked?
- **Security:** Are input validation, auth, and data privacy risks relevant?
- **Domain-specific:** For the project's domain, what risks are unique? (e.g., for ML systems: training/serving skew, data drift, model staleness)

Not all categories apply to every project. Only flag categories that are relevant AND absent.

### Disagreement Quality

For each D-entry, assess:
- Are the perspectives genuinely in tension (not just different emphasis)?
- Is the resolution actionable or theoretical?
- If the resolution names a specific action (e.g., "partial split"), does it have a trigger or timeline?
- Does the resolution reference the specific evidence that resolved the disagreement?

### Strategic Recommendation

Synthesize all findings into actionable guidance:
1. What to fix immediately (structural issues from Phase 1)
2. What to fix before next planning cycle (tier recalibration, trigger rewrites)
3. What to consider for the roadmap (causal cluster root causes)
4. What to demote or archive (signal-to-noise findings)

---

## Phase 9 -- Apply Fixes (both modes, user-confirmed)

After presenting the report and receiving user confirmation ("want me to apply these fixes?" → yes), apply changes directly to the register file.

### What to apply directly (no further confirmation needed)

These are mechanical corrections that don't change the register's meaning:
- **Structural fixes:** Header count corrections, section reordering, duplicate removal
- **Trigger rewrites:** Replacing perpetual/vague/compound triggers with actionable versions
- **Tier rationale additions:** Adding explicit reasoning to existing tier assignments without changing the tier
- **Cross-reference additions:** Adding "See also" links between related entries
- **D-entry enhancements:** Adding trigger conditions to resolutions, adding test file references

### What to apply with the tier change noted

These change the register's risk assessment:
- **Tier changes:** Apply the change and note "Tier recalibrated from X to Y during review-rr (date)" at the end of the narrative. This provides an audit trail.

Note: tier changes do NOT affect header counts (Total/Open/Resolved). They affect the tier distribution, which is not tracked in the header.

### What NOT to apply (recommend only)

These require user judgment or external infrastructure:
- **Entry demotion to tech-debt backlog:** The skill recommends demotion but does not remove entries. The user decides whether and where to move them.
- **Causal cluster section creation:** Recommend the section and its content, but let the user decide whether to add it to the register. This is a structural addition, not a correction.
- **Blind spot registration:** Note missing risk categories but do not create new entries. The user can invoke `register-risk` afterward.

### After applying

- Update `Last Updated` date in the header
- Verify header counts still match actual entry counts
- Use `git add -f` if the register is under a gitignored directory

---

## Phase P1 -- Load Register (Prioritize only)

Read the full register. Extract:

1. All open concerns with their tier, trigger, location, and source
2. All disagreements with their resolution status
3. Causal clusters if a `## Causal Clusters` section exists in the register

If no causal clusters section exists, perform a lightweight clustering pass:
- Group entries by shared file/module (e.g., all VolumeHandler entries)
- Group entries by shared problem type (e.g., all "untested" entries)
- Name each group as a potential cluster

This is a read-only analysis — do not write clusters to the register. The strategic mode is the appropriate place to formalize clusters.

---

## Phase P2 -- Score Clusters (Prioritize only)

For each cluster, compute a priority score:

### Scoring formula

```
cluster_score = (entry_count × avg_tier_weight) / fix_scope
```

**Tier weights:** Tier 1 = 4, Tier 2 = 3, Tier 3 = 2, Tier 4 = 1

**Fix scope** (estimated, qualitative):
- **Single refactor** (scope = 1): One targeted change resolves the cluster. Example: extracting a class, writing an ADR.
- **Multi-file refactor** (scope = 2): Changes across 2-5 files with coordination. Example: splitting a module, changing an interface.
- **Architectural change** (scope = 3): Cross-cutting change requiring design decisions. Example: restructuring packages, changing config propagation.

### Example

Cluster D (Exception handling doctrine): 3 entries, avg tier 3 (weight 2), fix = write an ADR (scope 1)
Score = (3 × 2) / 1 = 6.0

Cluster A (VolumeHandler): 9 entries, avg tier ~3.1 (weight ~1.9), fix = multi-file refactor (scope 2)
Score = (9 × 1.9) / 2 = 8.55

### Output

Table sorted by score descending:
| Rank | Cluster | Entries | Avg Tier | Fix Scope | Score | Quick Win? |
|------|---------|---------|----------|-----------|-------|------------|

Mark "Quick Win" = Yes if fix_scope = 1 and entry_count ≥ 3. These are high-value, low-effort improvements.

---

## Phase P3 -- Score Standalone Entries (Prioritize only)

For entries not in any cluster, score individually:

### Scoring dimensions

1. **Tier weight:** Same as cluster scoring (Tier 1 = 4, Tier 2 = 3, etc.)
2. **Trigger proximity:** How likely is the trigger to fire soon?
   - **Imminent** (×2): The trigger describes something being planned or likely this sprint
   - **Plausible** (×1): The trigger could happen under normal development
   - **Unlikely** (×0.5): The trigger requires unusual circumstances
3. **Fix effort:**
   - **Small** (÷1): Under 30 minutes, localized change
   - **Medium** (÷2): 1-4 hours, may span files
   - **Large** (÷3): Half-day+, requires design

### Formula

```
entry_score = (tier_weight × trigger_proximity) / fix_effort
```

### Output

Table sorted by score descending:
| Rank | ID | Title | Tier | Trigger Proximity | Fix Effort | Score |
|------|-----|-------|------|-------------------|------------|-------|

---

## Phase P4 -- Dependency Analysis (Prioritize only)

Identify entries that cannot be addressed independently:

### Blocked entries

An entry is blocked when:
- Its fix depends on resolving a disagreement first (e.g., C-36 ISP depends on D-01 resolution)
- Its fix requires an external dependency (e.g., parent class constraint in views_pipeline_core)
- Its fix would break artifacts or downstream systems (e.g., C-09 torch.save → state_dict migration)
- Its fix is explicitly deferred in a D-entry resolution (e.g., D-02 leaves architecture as-is)

### Prerequisites

An entry is a prerequisite when:
- Fixing it unblocks other entries (e.g., writing exception handling ADR unblocks C-16, C-21, C-31)
- It's a root-cause entry in a cluster (fixing it resolves cluster symptoms)

### Output

```
### Blocked Items
| ID | Blocked By | Unblocking Action |
|----|-----------|-------------------|

### Prerequisites (fix these first to unblock others)
| ID | Unblocks | Why |
|----|----------|-----|
```

---

## Phase P5 -- Report (Prioritize only)

Compile findings into the Prioritize Report structure (see SKILL.md).

### Recommended Sprint Plan

Select the top 3-5 actionable items considering:

1. **Cluster quick wins first:** High-score clusters with scope = 1 (e.g., write an ADR to resolve 3 entries)
2. **Prerequisites second:** Items that unblock other items
3. **High-score standalone entries third:** High tier, imminent trigger, small fix
4. **Explicitly exclude:** Blocked items, deferred items, items the user has previously declined to address

### Sequencing

Present items in execution order, not just priority order. If item B depends on item A, list A first regardless of score.

### Deferred Items

List items not included in the sprint plan with reason:
- "Blocked by D-01 resolution"
- "Requires architectural change (scope too large for sprint)"
- "Trigger unlikely this cycle"
- "External dependency (views_pipeline_core)"

### Verdict

- **CLEAR PRIORITY:** One cluster or entry has a score significantly higher than the rest (>50% above second place). Recommend starting there.
- **MULTIPLE OPTIONS:** Top 2-3 items have comparable scores. Present trade-offs: "Cluster D is a quick win (ADR) resolving 3 entries; Cluster A is higher total value but requires multi-file refactor."
- **BLOCKED:** The highest-scoring items are all blocked. Recommend the unblocking actions as the sprint plan instead.
