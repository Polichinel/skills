---
name: review-harness
description: Reviews and maintains the writing harness artifacts for a document. Two modes — sync (update artifact statuses against the current document) and prioritize (read harness state and surface what to work on next). Use when user says "sync the harness", "update the harness", "harness sync", "review-harness", "what's next for [document]", "prioritize the writing", "what should I work on", "check the harness", or "harness status". Do NOT use for initializing the harness (use writing-harness), for drafting (use strategic-draft), for critiquing (future persona-critique), or for falsification (use falsify).
---

# Review Harness

## Important

Follow these rules strictly.

- Do not draft prose. This skill reads and updates harness artifacts only.
- Do not create new decisions, findings, or manifesto entries. If you discover something missing, flag it in the report. The writer creates entries during drafting.
- Present the full review before making any changes. Ask: "Want me to apply these updates?" Do not modify artifacts until confirmed.
- Ground every finding in specific IDs (D-XX, F-XX, M-XX, A-NNNN). No vague observations.
- Read the actual document text when checking statuses. Do not infer from memory or conversation context — compare artifact claims against what the text currently says.

## Purpose

The writing harness degrades during drafting: decisions get resolved but stay marked Open, manifesto entries land in text but stay marked "NOT YET LANDED", findings get addressed but aren't updated, anchors drift from revised prose. This skill brings the harness back into alignment with the document and surfaces what needs attention next.

## Modes

### Sync Mode

Update harness artifact statuses to match the current document state.

For each artifact type, compare the artifact's claimed status against what the document actually contains:

- **DECISIONS.md**: Are Open decisions actually still open, or has the text already resolved them? Are Resolved decisions still reflected in the text, or has it drifted?
- **FINDINGS.md**: Are Pending findings still pending, or has the text addressed them? Are Landed findings still substantively present, or have they been diluted?
- **MANIFESTO.md**: Have Explicit-tier entries landed in the text? Have Implicit-tier entries been accidentally surfaced? Are text anchors still accurate?
- **Anchors**: Do anchors still match the formulations in the current text, or has revision created drift?

Invoke with: `/review-harness sync` or "sync the harness"

### Prioritize Mode

Read harness state and produce a ranked action plan for what to work on next.

Surfaces: open decisions by urgency, unresolved findings by severity, manifesto entries not yet landed, sections not yet drafted, and cross-cutting issues (e.g., "three decisions are still open in §3 — resolve those before drafting").

Invoke with: `/review-harness prioritize`, "what should I work on next", or "prioritize the writing"

Default (no mode specified): sync.

## Procedure

Execute phases sequentially. For detailed instructions, consult `references/phases.md`.

### Sync (Phases 1–5, then 6 if confirmed)

1. **Locate Harness and Document** — Find `_dev_materials/*/DECISIONS.md` and the document file
2. **Audit DECISIONS.md** — Compare each entry's status against document text
3. **Audit FINDINGS.md** — Compare each entry's status against document text
4. **Audit MANIFESTO.md** — Check tier statuses and text anchors
5. **Report** — Summary of all status discrepancies with proposed updates
6. **Apply Updates** — (after user confirms) Update statuses, text anchors, and header counts

### Prioritize (Phases P1–P4)

P1. **Load Harness State** — Read all artifacts, count entries by status
P2. **Score Open Items** — Rank by urgency: unresolved decisions blocking drafting > pending critical findings > missing explicit manifesto entries > pending substantive findings > editorial findings
P3. **Identify Dependencies** — Which open items block other open items? Which sections can't be drafted until decisions are resolved?
P4. **Report** — Ranked action plan with rationale

## Required Output Structure

### Sync Report

```
## Harness Sync Report — [document name]

### DECISIONS.md
| ID | Current Status | Proposed Status | Evidence |
|----|---------------|-----------------|----------|
| D-XX | Open | Resolved | §N now contains [specific text] |

### FINDINGS.md
| ID | Current Status | Proposed Status | Evidence |
|----|---------------|-----------------|----------|
| F-XX | Pending | Landed | §N paragraph M addresses this: [quote] |

### MANIFESTO.md
| ID | Tier | Current Status | Proposed Status | Evidence |
|----|------|---------------|-----------------|----------|
| M-XX | Explicit | Missing | Verified | Found in §N: [quote] |

### Anchors
| ID | Status | Issue |
|----|--------|-------|
| A-NNNN | Drifted | Text now says [X], anchor says [Y] |

### Summary
- Decisions: X need status update
- Findings: X need status update, Y potentially diluted
- Manifesto: X entries newly verified, Y still missing
- Anchors: X drifted

Want me to apply these updates?
```

### Prioritize Report

```
## Writing Priority Plan — [document name]

### Immediate (blocking further drafting)
1. [Ranked item with rationale]

### Next Session
1. [Ranked item with rationale]

### Deferred
1. [Item with reason for deferral]

### Document Coverage
- Sections drafted: [list]
- Sections remaining: [list]
- Estimated completion: [X of Y sections]
```

## Verdict

### Sync

- **IN SYNC**: All artifact statuses match the document. No updates needed.
- **STALE**: Status discrepancies found. List count by artifact type.
- **SIGNIFICANTLY STALE**: Major discrepancies — resolved decisions marked Open, landed findings marked Pending, manifesto entries not tracked. Harness is not reflecting reality.

### Prioritize

- **CLEAR NEXT STEP**: One item clearly dominates. Start there.
- **MULTIPLE OPTIONS**: Several items at comparable urgency. Present trade-offs.
- **BLOCKED**: Highest-priority items depend on unresolved decisions or external input. Recommend unblocking actions.

## Performance Notes

- Sync mode must read the actual document, not just the harness. The whole point is comparing the two.
- When checking FINDINGS.md Landed entries, verify the landing is substantive — form without substance is Diluted, not Landed.
- Prioritize mode should be opinionated. Don't list everything equally — rank ruthlessly. The writer needs "do this next," not "here are 15 things."
- If the harness is empty (no entries), say so directly: "The harness has no entries to sync. Either drafting hasn't started, or artifacts weren't being created during drafting."
