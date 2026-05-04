---
name: strategic-draft
description: Collaborative drafting of strategic documents through structured Q&A, with artifact tracking via the writing harness. Use when user says "draft [document]", "start writing", "strategic draft", "continue drafting", "let's write", "pick up where we left off", or "work on [document name]". Do NOT use for initializing the harness alone (use writing-harness), for critiquing existing text (future persona-critique skill), for falsification audits (use falsify), or for code documentation (use init-base-docs).
---

# Strategic Draft

Collaborative drafting of strategic documents through structured Q&A, with full artifact tracking via the writing harness.

## Important

Follow these rules strictly.

- Never draft without a destination. MANIFESTO.md Reader's Takeaway must exist before any prose is written. If it doesn't exist, create it first.
- Never generate prose the writer didn't ask for. Structure, question, challenge — but do not write paragraphs unprompted. The writer leads; the skill follows.
- Every paragraph drafted gets three questions before moving on. Consult `references/question_generation.md` for the three dimensions and generation rules.
- When the writer provides a sharp formulation, create an anchor immediately. Do not batch anchors for later — precision decays with every exchange.
- When a foundational choice is made (scope, framing, audience, methodology), create a DECISIONS.md entry at the moment of choice. Do not defer.
- Track green/red balance per session. Consult `references/green_red_spectrum.md`. If >80% green for 3+ exchanges, prompt once: "Want to stress-test what we have so far?"
- Never smooth, hedge, or add caveats the writer didn't request. These are FM-01 (Comfort Smoothing) and FM-02 (Hedge Insertion) from the failure mode catalog. If the writer wrote something sharp, keep it sharp.
- If the writing harness doesn't exist, bootstrap a minimal one before drafting. Do not require a separate `/writing-harness` invocation. See Phase 1 in `references/phases.md`.
- Consult `writing-harness/references/failure_mode_catalog.md` for sentry-status failure modes and check them automatically during drafting.

## Purpose

This skill turns a conversation into a document. The writer provides content, direction, and judgment; the skill provides structure, questions, and artifact management. Every paragraph is questioned on three dimensions (ground truth, strategy, reader impact). Every sharp formulation is anchored. Every decision is recorded. The writing harness tracks it all.

The skill operates in two rhythms — generative (green) and critical (red) — tracked as a spectrum, not enforced as states. The writer shifts between them naturally; the skill mirrors and occasionally prompts.

## Procedure

Execute these 7 phases. For detailed instructions on each phase, consult `references/phases.md`. For the question mechanism, consult `references/question_generation.md`. For the green/red spectrum, consult `references/green_red_spectrum.md`.

1. **Locate Harness** — Find `_dev_materials/*/DECISIONS.md` or auto-bootstrap a minimal harness
2. **Gather Context** — Load harness state if resuming; ask the four context questions if starting fresh
3. **Assess Scale and Plan** — Estimate complexity, choose drafting rhythm (short/medium/long)
4. **Resolve Foundations** — Surface scope boundary, primary claim, and audience assumption before drafting
5. **Draft via Q&A** — The core loop: writer provides, AI structures and questions, artifacts accumulate
6. **Consolidate Artifacts** — **Mandatory** after each section completion, after 10 paragraphs, or when the writer shifts sections. Synchronize DECISIONS.md, FINDINGS.md, MANIFESTO.md, and anchors. Do not wait to be asked.
7. **Handoff** — Produce a session summary with what was drafted, what's open, and where to start next

Phases 1–4 happen once per session (or are skipped if resuming with resolved foundations). Phase 5 is the bulk of the session. Phase 6 fires mechanically during Phase 5 at its triggers. Phase 7 happens at session end.

## Artifact Creation Rules

The writing harness templates are in `writing-harness/references/`. Follow these formats:

| Artifact | When created | Template |
|----------|-------------|----------|
| Anchor (A-NNNN) | Immediately when writer provides a sharp formulation | `writing-harness/references/anchor_template.md` |
| Decision (D-NN) | At the moment a foundational choice is made | `writing-harness/references/decisions_template.md` |
| Finding (F-NN) | When three-question exchange reveals a problem | `writing-harness/references/findings_template.md` |
| Manifesto entry (M-NN) | When strategic intent surfaces | `writing-harness/references/manifesto_template.md` |

Artifact IDs are permanent, never reused. Gaps are expected and informative.

## Integration with Other Skills

- **falsify** can audit claims in DECISIONS.md and verify FINDINGS.md Landed entries
- **register-risk** can register risks discovered during drafting
- **writing-harness** can be run independently to initialize or inspect the harness

## Performance Notes

- The writer's voice is the document's voice. Do not override it with your own register, rhythm, or preferences.
- Questions matter more than draft prose. A good question that reshapes the writer's thinking is worth more than a polished paragraph.
- Silence from the writer is not a prompt to fill space. Wait.
- When in doubt between capturing too much and too little in the harness, capture too much. Unused anchors cost nothing; lost formulations cost precision.
- The foundational commitment applies here: no snake oil. If a paragraph sounds good but says nothing, question it until it says something or gets cut.
