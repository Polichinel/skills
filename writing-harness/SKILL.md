---
name: writing-harness
description: Initializes and manages the writing harness artifact structure for strategic documents. Creates DECISIONS.md (drift defense), FINDINGS.md (findings ledger), MANIFESTO.md (implicit/explicit strategy), and anchors/ (precision skip connections) in _dev_materials/. Use when user says "init writing harness", "set up writing harness", "initialize harness for", or "create writing artifacts for". Do NOT use for drafting, critiquing, or revising — those are separate skills that consume harness artifacts.
---

# Writing Harness

Initialize and manage the artifact structure that writing skills operate on.

## Important

- This skill creates the artifact substrate. It does not draft, critique, or revise documents.
- All artifacts follow strict structure, flexible depth: the scaffold (metadata tables, IDs, status values) is mandatory; content within fields scales to the document.
- The harness location is `_dev_materials/<document_slug>/` within the project directory.
- DECISIONS.md is the sentinel file — other skills discover active writing projects by scanning for it.

## What This Skill Creates

When invoked, initialize the harness by creating the directory structure and populating templates:

```
_dev_materials/<document_slug>/
├── DECISIONS.md              # From references/decisions_template.md
├── FINDINGS.md               # From references/findings_template.md
├── MANIFESTO.md              # From references/manifesto_template.md
├── anchors/                  # Empty directory, ready for skip connections
├── critiques/                # Empty directory, ready for persona outputs
├── falsification/            # Empty directory, ready for audit outputs
└── external_feedback/        # Empty directory, ready for third-party input
```

## Procedure

### Step 1: Gather Context

Ask the writer:
1. What is the document? (working title, purpose)
2. Who reads this? What do they do after reading it?
3. What would make this fail even if it's well-written?
4. What institutional documents, reference materials, or prior correspondence exists that the audience would recognize as their language?

Do NOT ask "what genre is this?" — the genre is the shadow cast by the answers above.

### Step 2: Create Directory and Artifacts

1. Determine `<document_slug>` from the working title (lowercase, underscores, concise)
2. Create the directory structure
3. Copy and fill the three template files:
   - DECISIONS.md: fill Document name and dates
   - FINDINGS.md: fill Document name and dates
   - MANIFESTO.md: fill Document name, Audience (from Step 1), and draft the Reader's Takeaway (from the writer's answers about purpose and reader)

### Step 3: Seed Initial Content

Based on the writer's answers in Step 1:

**MANIFESTO.md**: Propose initial entries across all three tiers. Ask the writer to confirm or adjust. Pay particular attention to the Must Stay Implicit tier — ask: "Is there anything that needs to be felt but never stated?"

**DECISIONS.md**: If foundational questions are already apparent (document scope, strategic choices, audience framing), create D-01, D-02... entries with Status: Open.

**anchors/**: If the writer provides reference materials or prior work, create anchor files capturing specific claims or formulations from those sources. Tag the Source field accurately.

### Step 4: Confirm and Advise

Show the writer what was created. Confirm the MANIFESTO.md Reader's Takeaway captures the destination correctly. Note which skills can now operate on this harness:
- `falsify` can audit claims in DECISIONS.md and verify FINDINGS.md entries
- Future persona-critique and strategic-draft skills will read and write these artifacts

## Artifact Cross-References

All IDs are permanent, never reused. Gaps are expected and informative.

| Artifact | Prefix | Scope |
|----------|--------|-------|
| Decisions | D-NN | Per document |
| Findings | F-NN | Per document |
| Manifesto entries | M-NN | Per document |
| Anchors | A-NNNN | Per document |
| Failure modes | FM-NN | Global catalog |

Cross-references use these prefixes. E.g., a FINDINGS.md entry might say "See D-03" to link a finding to its governing decision.

## The Failure Mode Catalog

Consult `references/failure_mode_catalog.md` for the 29 cataloged failure modes. This catalog is persistent across projects and grows over time. Status levels:

- **Discovery**: seen < 3 times. Available as context for scout personas.
- **Known**: seen >= 3 times across 2+ documents. Skills mention as known risk.
- **Sentry**: >= 5 times AND mechanical detection defined. Checked automatically.

When a finding maps to a cataloged FM-XX, log it in the catalog's occurrence table. If the occurrence threshold is reached, prompt the writer to consider graduation.

## Foundational Commitment

No snake oil. Speed and ambition are fine. Hollow packaging is not. If the harness or any skill operating on it produces output that is well-packaged but hollow, it has failed its primary obligation. Every mechanism — dilution defense, provenance tracking, honesty-as-strategy — serves this commitment.

## Performance Notes

- Take your time to do this thoroughly
- Quality is more important than speed
- Do not skip validation steps
