---
name: review-rr
description: Reviews, curates, and prioritizes the repository's technical risk register. Three modes — triage (quick structural check after registration), strategic (deep causal analysis for calibration), and prioritize (ranked work plan for sprint planning). Use when user says "review the risk register", "audit the register", "curate the register", "triage the register", "review-rr", "risk register review", "are the risks prioritized correctly", "what should we fix first", "prioritize the register", "what risks matter most", or "plan from the register". Do NOT use for adding risks (use register-risk), for finding risks (use expert-code-review, test-review, falsify, etc.), or for fixing risks (fix the code directly).
---

# Review Risk Register

## Important

Follow these rules strictly.

- Do not add new risks during a review. If you discover a missing concern, note it in the Blind Spots section — do not register it. The user can invoke register-risk afterward.
- Do not remove entries. Flag entries for removal or merger in the report; the user decides.
- Do not modify source code. This skill reads and curates the register only.
- Complete all applicable checks before proposing any changes. Present the full review, then ask if the user wants fixes applied.
- In strategic mode, complete every analysis dimension. Do not shortcut.
- Ground every finding in specific entry IDs. No vague observations.

## Critical Constraint

This skill reviews and proposes changes to the register. It does not apply changes until the user confirms. Present the review first, then ask: "Want me to apply these fixes?"

## Purpose

The risk register is a living governance artifact. Without periodic curation, it degrades: entries accumulate without deduplication, tiers drift, triggers become perpetual, and the register becomes noise instead of signal. This skill provides three modes: structural validation, analytical calibration, and actionable prioritization.

## Modes

### Triage Mode

Fast structural check. Run after every `register-risk` invocation or before shipping.

Checks: header count accuracy, section ordering, duplicate detection, formatting compliance, cross-reference integrity.

Invoke with: `/review-rr triage` or "triage the register"

### Strategic Mode

Deep analytical review. Run quarterly or when the register exceeds 30 entries.

Includes everything in triage plus: causal clustering, tier recalibration, trigger quality audit, signal-to-noise analysis, blind spot analysis, disagreement quality, and actionability scoring.

Invoke with: `/review-rr strategic` or "full review of the risk register"

### Prioritize Mode

Ranked work plan. Run before sprint planning or when asking "what should I fix next?"

Reads the register and produces a prioritized action plan: which clusters or entries to address, in what order, with effort/impact scoring and dependency analysis. Does not modify the register.

Invoke with: `/review-rr prioritize`, "prioritize the register", "what should we fix first", or "plan from the register"

Default (no mode specified): strategic.

## Procedure

Execute phases sequentially. For detailed instructions on each phase, consult `references/phases.md`. For the analytical framework used in strategic mode, consult `references/analysis.md`.

### Triage (Phases 1-3, then 9 if confirmed)

1. **Structural Integrity** -- Header counts, section ordering, ID sequencing, formatting
2. **Deduplication Scan** -- Compare all entries pairwise for overlap
3. **Report** -- Summary of structural issues with proposed fixes
9. **Apply Fixes** -- (after user confirms) Apply mechanical corrections directly

### Strategic (Phases 1-9, with 9 after user confirms)

1. **Structural Integrity** -- (same as triage)
2. **Deduplication Scan** -- (same as triage)
3. **Tier Calibration** -- Check each tier assignment against criteria and peers
4. **Causal Clustering** -- Identify root causes shared by multiple concerns
5. **Trigger Quality** -- Audit every trigger for actionability
6. **Signal-to-Noise** -- Assess whether all entries warrant register tracking
7. **Blind Spot Analysis** -- Identify risk categories not represented
8. **Report** -- Full analytical report with proposed changes and strategic recommendations
9. **Apply Fixes** -- (after user confirms) Apply direct changes; recommend-only for demotions, clusters, blind spots

### Prioritize (Phases P1-P5)

P1. **Load Register** -- Read register and identify causal clusters (from register or by analysis)
P2. **Score Clusters** -- Rank clusters by (entry count × avg tier severity) / estimated fix scope
P3. **Score Standalone Entries** -- Rank unclustered entries by tier, trigger proximity, and fix effort
P4. **Dependency Analysis** -- Identify entries blocked by external constraints or prerequisites
P5. **Report** -- Ranked work plan with rationale

## Required Output Structure

### Triage Report

1. Structural Checks (pass/fail per check, fixes needed)
2. Duplicates Found (entry pairs, overlap type, recommended action)
3. Verdict (CLEAN / NEEDS FIX + count of issues)

### Strategic Report

1. Structural Checks (pass/fail per check)
2. Duplicates Found (entry pairs, overlap type)
3. Tier Calibration (inconsistencies found, proposed changes with rationale)
4. Causal Clusters (root cause → symptom IDs, cluster name, recommended action)
5. Trigger Quality (weak triggers listed, proposed rewrites)
6. Signal-to-Noise (entries that should be demoted to tech-debt backlog)
7. Blind Spots (risk categories absent from register)
8. Disagreement Quality (assessment of D-entries)
9. Summary Table (all proposed changes: entry ID, change type, rationale)
10. Strategic Recommendation (what to fix first, what to defer, planning guidance)

### Prioritize Report

1. Cluster Rankings (table: rank, cluster name, entries, avg tier, fix scope, score)
2. Standalone Rankings (table: rank, entry ID, tier, trigger proximity, fix effort)
3. Blocked Items (entries with external dependencies or prerequisites)
4. Recommended Sprint Plan (top 3-5 items with rationale and sequencing)
5. Deferred Items (items to revisit next cycle with reason for deferral)

## Verdict

### Prioritize

- **CLEAR PRIORITY:** One cluster or entry dominates the ranking. Start there.
- **MULTIPLE OPTIONS:** Several items have comparable scores. Present trade-offs and let user choose.
- **BLOCKED:** Highest-priority items depend on external constraints. Recommend unblocking actions.

### Triage

- **CLEAN:** All structural checks pass. No duplicates. Header counts correct.
- **NEEDS FIX:** Structural issues found. List count and severity.

### Strategic

- **WELL-CALIBRATED:** No tier inconsistencies, no duplicates, causal clusters documented, triggers actionable.
- **NEEDS CURATION:** Issues found but register is fundamentally sound. List recommended changes.
- **NEEDS OVERHAUL:** Significant structural or calibration problems. Register is not serving its governance purpose effectively.

## Performance Notes

- Triage should be fast (under 2 minutes of analysis). Do not over-analyze in triage mode.
- Strategic mode should be thorough. Quality over speed. Read every entry carefully.
- The causal clustering analysis (Phase 4) is the highest-value output of strategic mode. It transforms a flat list into actionable strategy.
- When the register exceeds 40 entries, the signal-to-noise analysis becomes critical — at that size, the register risks becoming a write-only artifact.
- The blind spot analysis should consider the project's domain. A conflict forecasting system has different risk categories than a web application.
