---
name: expert-method-review
description: Library-grounded, multi-persona critique of ML/research DESIGN and METHODOLOGY — the gap between expert-code-review (code quality) and persona-critique/falsify (academic argument). Use when deciding WHAT to build/model and WHY — loss/likelihood, inductive bias, architecture, uncertainty representation, evaluation, experiment design — judged against the paper library and the data-generating process. Trigger: /expert-method-review.
---

# Expert Method Review

## Important

Follow these rules strictly.

- This is a **design / methodology** review. It is NOT code review (→ `expert-code-review`) and NOT academic-argument critique (→ `persona-critique` / `falsify`). If the target is code quality or a finished paper's argument, stop and redirect.
- Operate on a **design/plan/idea artifact**: a dossier `02_design`, a pre-analysis plan, a roadmap, an ADR-in-waiting, or a stated research idea. Not a codebase, not prose.
- Evaluate each persona **independently**. Do not merge perspectives. **The disagreements are the product.**
- **Ground every critique in the library** — prefer the **`library` skill** (`/library search|find|cite`) for retrieval/citation, falling back to the filesystem (`~/brain/9_library`). And/or named literature. No hand-waving "the literature says." Cite specific work, and produce an explicit **gaps-to-fetch** list. This grounding is what separates this skill from generic ML advice — it is mandatory.
- Personas are **named figures with documented, principled stances** (`references/personas.md`). Construct them faithfully from their real positions. Do **not** caricature. If a persona's actual stance on a point is unknown, say so rather than invent it.
- **The user is the chair, not a panelist.** The panel exists to surface views the chair might miss — never seat a persona of the user (echo chamber). Domain coverage uses the seats defined in `references/personas.md`.
- **Read-only.** Produce a critique + register-compatible methodological risks. Do not implement, edit code, or run experiments.

## Purpose

Fill the gap between "how it's built" (code review) and "is the claim sound" (paper critique): **what should we build, modeled which way, and why — judged against the literature and the data-generating process.** Unlike the artifact-evaluating reviews, this one is **generative**: it proposes what to consider building and names what's methodologically *absent*, grounded in the library. It is the systematized version of a strong design conversation among opinionated experts who do not agree.

## Procedure

Execute these 6 phases sequentially. For the persona casting pool, panel-selection guidance, and fault lines, consult `references/personas.md`.

1. **Parse target & scope the decisions.** Read the design/plan. Identify the specific **modeling decisions under review** (e.g. output likelihood, inductive bias, architecture, uncertainty representation, loss, evaluation metric, experiment design) and characterise the **data-generating process** the design must respect.
2. **Assemble the panel (task-selected).** From `references/personas.md`, seat named personas that (a) **span the axes** of the decisions under review and (b) **guarantee ≥2 opposing sides** on each live fault line. State the panel and *why these seats*. (A repo-default core is suggested in `references/personas.md`; the user may override.)
3. **Library grounding.** Use the **`library` skill** (`/library search "<topic>"`, `/library find`, `/library cite`) to locate relevant holdings (fall back to grepping `~/brain/9_library`); map each seated persona to their anchors; build a **"have vs missing → fetch"** list. Flag where a decision rests on literature we do not hold. (The `library` skill is the same claim-centric corpus `01_literature` uses — don't reimplement search.)
4. **Independent persona critiques.** Each persona, in their own principles and voice: endorse or challenge the modeling choices; name missing baselines / untested assumptions / standard methods; propose what to build instead or additionally; cite library/literature. 2–4 grounded points each. **No merging.**
5. **Key disagreements.** Surface the fault lines explicitly — who opposes whom, on what, and why each side has merit. This is the highest-value output.
6. **Synthesis & recommendation.** What to implement and in what order; what's methodologically missing; what to fetch; and the strongest dissent to keep live. Format register-worthy methodological gaps as concern entries.

## Required Output Structure

1. **Target & Decisions Under Review** (the design + the specific modeling decisions + the DGP)
2. **Panel** (personas seated, with rationale and the fault lines they cover)
3. **Library Grounding** (relevant holdings cited + gaps to fetch)
4. **Independent Critiques** (per persona — strengths/challenges/what-to-build, grounded)
5. **Key Disagreements** (the fault lines, with the merit of each side)
6. **Synthesis & Recommendation** (what to build, in what order, what's missing, strongest dissent)
7. **Methodological Risks** (register-compatible: ID, tier, trigger, location/artifact, narrative)

## Risk Register Integration

Format Critical/High methodological gaps in register-compatible form (ID, tier, trigger, source, location, narrative). Do **not** append to the register — output the findings and let the user invoke `register-risk` (which handles dedup, tiering, linking). Same intake pattern as `expert-code-review` / `test-review`.

## Seams (where this skill hands off)

- **Code quality** → `expert-code-review`. **A paper's argument / a claim to attack** → `persona-critique` / `falsify`. **Reproducibility** (seeds, multi-seed, ablation discipline) → a *harness check*, not a persona here.
- This review **precedes** the dossier's **pre-analysis plan** (it shapes *what is worth testing*; pre-registration then commits predictions+falsifiers; `falsify` attacks claims *after*).
- A design this review validates **graduates to a proposed ADR**; methodological risks it finds flow to **`register-risk`**.

## Scaling (multi-agent)

For a thorough run, **fan the personas out as parallel agents** — one per seat, each independently reading the target and searching the library — then a synthesis pass that extracts the disagreements. Parallel agents *enforce* the independence the method depends on (no cross-contamination between seats). A quick pass may run the personas inline/sequentially. Either way, complete every seated persona before synthesising.

## Performance Notes

- Quality over speed. Complete all seated personas before synthesis; do not shortcut the disagreement phase.
- Library grounding is non-negotiable — a critique that cites no specific work (held or to-fetch) is not done.
- Faithful personas: ground stances in the figure's documented positions; flag uncertainty rather than fabricate.
- Default to **task-selected** panels (4–7 seats) sized to the decision; resist seating the whole pool.
