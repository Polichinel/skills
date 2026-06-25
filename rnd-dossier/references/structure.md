# Dossier Structure

The canonical layout `init` creates. Mirrors the established repo convention (`reports/archived/<date>_<name>_dossier/` with numbered, dated docs). Domain-general; `reports/2026-06-05_distributional_head_dossier/` is the worked exemplar.

## Location & naming

- `reports/<YYYY-MM-DD>_<name>_dossier/` — dated subdirectory; `<name>` is the focused program (e.g. `distributional_head`).
- Numbered docs `NN_<topic>.md`. `00_README` is **living** (updated continuously); the rest are point-in-time artifacts dated in-header.
- **git-tracked** via `git add -f` (the `reports/` working area is usually gitignored).
- On close, the whole directory moves to `reports/archived/`.

## The document set

| # | File | Role | Living? |
|---|------|------|---------|
| 00 | `README` | **spine**: purpose (1 para), relationship to prior art / ADRs, document index (status per doc), the experimentation-harness at a glance, a living **next-actions** checklist, conventions | yes |
| 01 | `literature` | annotated bibliography (via the `library` skill / corpus) — per source: what it is + **what we take from it**; grouped by role; an explicit **gaps-to-fetch** list | append |
| 02 | `design` | the architecture/approach + the *why*; the modeling decisions and their justification. **Graduates to an ADR on `promote`.** Often absorbs prior path/proposal docs (mark originals superseded). | revise |
| 03 | `harness_and_invariants` | **the crown jewel** — the guardrails that make experimentation safe (see `harness.md`): invariant taxonomy, the standing harness, the new harness this program needs, the pre-flight checklist | revise |
| 04 | `roadmap` | phased, **gated** implementation + experiment sequencing; dependency graph; milestones; decision points | revise |
| 05 | `analysis_plan` | the first experiment(s), **pre-registered** (hypotheses, predictions, falsifiers, metrics, controls) — see `templates.md`. Subsequent experiments get their own `preregister` artifacts. | append |
| 06 | `glossary` | shared vocabulary (the program introduces new terms; define them once) | append |
| 07 | `experiment_log` | **append-only** ledger of every run + outcome, **including negatives/postmortems**; each entry links its pre-registration and its verdict-vs-falsifiers | append-only |

Risks fold into the repo's **risk register** (`register-risk`), not the dossier. Pre-analysis plans for individual experiments may live as `NN_preanalysis_<name>.md` in the dossier (or top-level `reports/preanalysis_*.md`), always linked from `00_README` and `07`.

## 00_README spine (sections)

1. Purpose (one paragraph). 2. Relationship to prior work / which ADRs it complements or will become. 3. Document index (table, status per doc). 4. Harness at a glance (pointer to `03` + the "already exists vs to-build" summary). 5. Current state & **next actions** (living checklist). 6. Conventions (numbering, dating, git-tracking, archival).

## Lifecycle

`init` (scaffold + harness audit) → [`expert-method-review` on `02_design`] → `preregister` → *(execute — other skills/scripts)* → `log` (incl. negatives) → `status` (gate checks) → iterate → `promote` (→ proposed ADR + archive). The dossier is the **staging area**; the ADR is the **committed decision**. Don't let designs validate without an exit ramp — orphaned dossiers are the failure mode.
