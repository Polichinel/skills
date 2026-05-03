# Review Risk Register: Analytical Framework

This document provides the reasoning framework for the strategic review mode. Consult it when making judgment calls about tier calibration, causal clustering, or signal-to-noise assessment.

---

## The Purpose of a Risk Register

A risk register is not a bug tracker, a tech-debt backlog, or a code review checklist. It is a **governance artifact** that tracks risks with three properties:

1. **Non-obvious trigger:** The risk materializes under specific conditions that someone might not anticipate
2. **Disproportionate impact:** The consequence exceeds what you'd expect from the trigger
3. **Cross-cutting concern:** The risk affects more than the person who encounters it

If a concern has none of these properties, it belongs in a lighter-weight tracker (GitHub issues, tech-debt backlog, TODO comments).

---

## Tier Calibration Principles

### The impact-likelihood trap

Risk registers often conflate impact and likelihood. A concern with catastrophic impact but near-zero likelihood (e.g., "if PRIO-GRID assigns GID 0 to a valid cell, data is silently dropped") gets the same tier as a concern with moderate impact and high likelihood (e.g., "adding a new loss function requires modifying choose_loss()").

The tier system should measure **expected risk** — roughly impact × likelihood. When calibrating:
- If impact is catastrophic but trigger is essentially impossible, Tier 3 or 4 is appropriate with a note explaining the reasoning
- If impact is moderate but trigger is near-certain, Tier 2 or 3 is appropriate
- If both are low, Tier 4
- If both are high, Tier 1 or 2

### Peer comparison

The most reliable calibration method is comparing entries within the same tier. After all entries are assigned, read the full list at each tier:

- Do all Tier 2 entries feel equally urgent?
- Would you fix all Tier 3 entries before any Tier 4 entries?
- Are there Tier 4 entries that are more severe than some Tier 3 entries?

Inconsistencies at tier boundaries are common and should be surfaced.

### The "standing concern" problem

Some entries describe conditions that are always true — they're not risks waiting to materialize, they're properties of the system. Examples:
- "VolumeHandler has 780 lines" — always true
- "`utils/` contains 20 files" — always true
- "Config returns dict after validation" — always true

These are valid observations but poor register entries because there's no trigger event. They're better framed as motivations for refactoring, tracked in a roadmap or tech-debt backlog.

---

## Causal Clustering Theory

### Why clusters matter

A flat list of 40 concerns overwhelms. A developer reads it and thinks "everything is broken." Causal clustering reframes: "There are 4 structural issues, each manifesting as several symptoms. Addressing the 4 root causes would resolve 25 of the 40 concerns."

This is the difference between a register that paralyzes and one that guides.

### How to identify root causes

A root cause is not the most severe symptom — it's the structural decision (or lack of decision) that creates multiple symptoms.

**Test:** If you could go back in time and make one different architectural choice, which concerns would not exist?

Example:
- If VolumeHandler had been split into VolumeOps + VolumeOutput from the start: C-36 (ISP), C-37 (SAP), C-39 (dependency rule) would not exist. C-08 (flip coupling) and C-13/C-14 (mutation) would still exist because they're internal to volume operations.
- Root cause: "PredictionFrame output was added to VolumeHandler instead of extracted into a dedicated component."

### Cluster naming discipline

The cluster name should identify the decision, not the component:
- "VolumeHandler accumulated output responsibility" — identifies the decision
- "VolumeHandler problems" — identifies the component (too broad)

Good names are falsifiable: you can check whether a proposed fix actually addresses the named decision.

---

## Signal-to-Noise Assessment

### The register growth problem

Registers grow monotonically unless actively curated. Each audit skill adds entries. Nobody removes entries because removing feels like ignoring risk. Over time, the register becomes a comprehensive catalog of imperfections — accurate but useless.

The cure is not removal but stratification. Not all observations need the same tracking weight.

### Three-track model

| Track | Purpose | Format | Review cadence |
|-------|---------|--------|---------------|
| Risk register | Non-obvious risks with disproportionate impact | Full entry with tier, trigger, narrative | Quarterly |
| Tech-debt backlog | Mechanical improvements with known fixes | One-liner with location and action | Per-sprint |
| Accepted trade-offs | Conscious design decisions not to fix | Disagreement entry (D-xx) with resolution | Annual |

The strategic review should recommend which track each entry belongs on.

### Demotion criteria

Consider demoting to tech-debt backlog if ALL of the following are true:
1. The fix is mechanical (no design decision required)
2. The scope is single-file (one developer can fix it without coordination)
3. The trigger is perpetual (the concern is always active, not event-triggered)
4. The tier is 4 (no correctness or reliability impact)

If ANY criterion fails, keep in the register.

---

## Blind Spot Detection

### Domain-agnostic categories

Every software system should have risks tracked in these categories. If a category is empty, either the risk doesn't exist (good) or it hasn't been looked for (blind spot):

1. **Data integrity:** Silent corruption, loss, or misrepresentation
2. **Boundary contracts:** What happens at system edges (input, output, API)
3. **Failure propagation:** How errors cascade through the system
4. **State management:** Mutation, concurrency, persistence
5. **Testability:** What can't be tested and why
6. **Operational:** Deployment, monitoring, recovery

### Domain-specific categories

Depend on the project's domain. For ML/forecasting systems:
- Training/serving skew
- Data drift detection
- Model versioning and rollback
- Reproducibility (seeds, hardware, non-determinism)
- Feature leakage

For web applications:
- Authentication and authorization
- Input sanitization
- Rate limiting and abuse
- PII handling

The reviewer should identify which domain-specific categories are relevant and check whether risks in those categories are tracked.

---

## Disagreement Assessment

### What makes a good disagreement entry

A D-entry is valuable when:
- The perspectives represent genuine tension (not just emphasis difference)
- Both sides have meritorious arguments grounded in evidence
- The resolution explains why one perspective prevailed, not just which one
- The resolution is actionable (names a specific future action) or explicitly deferred

### What makes a poor disagreement entry

- Perspectives are really just "do it now" vs "do it later" — that's a prioritization question, not a disagreement
- Resolution is theoretical ("recommended" without timeline or trigger)
- The disagreement has been resolved by subsequent code changes but the entry wasn't updated

---

## Prioritization Principles

### Why prioritize from the register

A register with 30+ entries is a list of everything that's wrong. A prioritized register answers "what should I do next?" The difference is the difference between anxiety and agency.

### The cluster advantage

Fixing a root cause resolves multiple entries. A cluster with 6 entries and a single-refactor fix is higher value than fixing 6 standalone Tier 4 entries individually — even if each standalone entry is easier.

The scoring formula captures this: `(entry_count × avg_tier_weight) / fix_scope`. A cluster of 6 Tier 3 entries with scope 2 scores (6 × 2) / 2 = 6.0. Six standalone Tier 4 entries with scope 1 each score 1.0 each. The cluster is clearly the better use of time.

### Trigger proximity

Not all risks are equally imminent. A trigger that says "when adding a new model architecture" is irrelevant if no new architecture is planned. A trigger that says "when modifying the training loop" is imminent if training loop refactoring is on the roadmap.

Trigger proximity should be assessed relative to the project's current plans — what the user has told you, what's on the roadmap, what recent changes suggest is coming next.

### The quick-win heuristic

A "quick win" is a cluster where:
- Fix scope = 1 (single targeted change, like writing an ADR or extracting a class)
- Entry count ≥ 3 (resolves multiple concerns at once)

Quick wins should always appear near the top of the sprint plan regardless of absolute score, because their cost is low and their benefit is disproportionate. Writing an exception handling ADR that resolves 3 entries takes an hour and clears 7.7% of the register.

### Blocked items

Some entries cannot be addressed regardless of priority:
- **External dependencies:** The fix requires changes to a library or upstream system outside the project
- **Artifact constraints:** The fix would invalidate existing data, models, or deployments (e.g., D-02)
- **Unresolved disagreements:** The fix depends on a design decision that hasn't been made (e.g., D-01)

Blocked items should be listed separately with their unblocking action. Sometimes the highest-value sprint item is not fixing a concern but unblocking one — e.g., making a design decision on D-01 to unblock C-36, C-37, C-39.
