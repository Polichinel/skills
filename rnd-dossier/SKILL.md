---
name: rnd-dossier
description: Scaffold and maintain an R&D experimentation dossier — the governed staging area where an ML/research direction is designed, harnessed, pre-registered, run, and logged BEFORE it graduates to an ADR. Verb-dispatched. Trigger - /rnd-dossier <verb>, where <verb> is one of - init (scaffold structure + audit the repo's experimentation harness), preregister (write a pre-analysis plan), log (record an experiment outcome, including negatives), status (assess roadmap position + log integrity + next action), promote (graduate a validated design to a proposed ADR and archive). Do NOT use for code review (expert-code-review), design/methodology critique (expert-method-review), or the risk register (register-risk / review-rr).
---

# R&D Dossier

A dossier is the **scientific method for ML R&D, instrumented with governance**: scaffold → harness → survey literature → critique design → pre-register → execute → log (incl. negatives) → curate → promote. It is the **research staging area** (lives in `reports/`, git-tracked); a validated design exits to a **proposed ADR** (governance). This skill manages the dossier's lifecycle; it does not critique designs (→ `expert-method-review`) or audit code (→ `expert-code-review`).

## Important

- **Verb-dispatched.** Parse the verb from args (`init|preregister|log|status|promote`); if absent, run `status` if a dossier exists, else explain the verbs. One verb per invocation.
- **Read-mostly except where the verb writes.** `init`/`preregister`/`log`/`promote` create or append dossier files; `status` is read-only. Never modify source code or run experiments — the dossier *plans and records*; the user (or other skills) executes.
- **Negatives are first-class.** `log` must make recording a *falsified/negative* result exactly as frictionless as a win. The experiment log is a Popperian record and a **meta-evaluation corpus** (used later to assess the workflow and the skills themselves), not a highlight reel. Preserve the **pre-registration ↔ outcome linkage** on every entry.
- **Respect the seams** (and state them in output): design/method critique → `expert-method-review` (precedes pre-registration); code → `expert-code-review`; the risk register → `register-risk`/`review-rr`; literature survey → `library` (`/library search`, `/library find`, `/library cite` for `01_literature`); citation verification in any associated writing → `verify-sources`; a validated decision → an **ADR** (`init-base-docs`/`adopt-base-docs` machinery), at which point the dossier is archived.
- **Git-tracked.** `reports/` is typically gitignored; `git add -f` dossier files so the program is version-controlled and shareable (confirm with the user once).
- Conventions, doc specs, harness checklist, and templates live in `references/`. Consult them; do not improvise structure.

## Verbs

### `init` — scaffold structure + audit the harness
1. Confirm scope/name with the user; create `reports/<YYYY-MM-DD>_<name>_dossier/`.
2. Seed the document set per `references/structure.md` (`00_README` … `07_experiment_log`). `00_README` is the living spine (purpose, prior-art relationship, doc index, status, next actions).
3. **Audit the repo for the experimentation harness (the crown jewel)** per `references/harness.md`: detect guardrails that *already exist* (reproducibility/seed gate, test-minimum gate, default-off-flag pattern, parity tests, fast retrain-free readout, eval-comparability/baseline) → codify them into `03_harness`; classify invariants (hard / intentionally-changed-by-this-program / respect-while-changing); write the **pre-flight checklist** and flag the gaps. Do not assume a blank slate — discover what's there.
4. Absorb any prior art (existing path/plan docs) into the dossier and mark the originals superseded with a pointer.
5. `git add -f` the dossier; report the structure + the harness gaps as the immediate next work.

### `preregister` — write a pre-analysis plan (the commit-before half of the loop)
Create a pre-analysis plan (template in `references/templates.md`): hypothesis · intervention (the *one* variable) · **skepticism ledger** · pre-registered predictions · **falsifiers (pre-committed)** · method · decision rules. Write it **before** the experiment runs. Link it from `00_README` and the roadmap. (This *follows* an `expert-method-review` of the design and *precedes* execution; `falsify` attacks claims *after*.)

### `log` — record an outcome (the record-after half; negatives first-class)
Append an entry to `07_experiment_log` (template in `references/templates.md`): link to its pre-registration · the one variable changed · driver/artifact/results location · readout · **verdict against the pre-registered falsifiers** (which fired / none) · decision. For a falsified/negative result, write the fuller **postmortem** (template) and link it — *do not* soften or omit it. Update `00_README` status.

### `status` — assess the dossier (read-only)
Report: position on the roadmap (which phase/milestone) · **log integrity** (any pre-registration without a logged outcome? any outcome lacking a pre-registration link? any success-only drift?) · doc sync (README index vs files; superseded pointers resolve) · open gates from the pre-flight checklist · **the single next action**. This is a lightweight self-review, not a methodology critique (→ `expert-method-review`).

### `promote` — graduate to an ADR + archive
When a design is validated: draft a **proposed ADR** from `02_design` into `docs/ADRs/proposed/` (hand off to the base-docs machinery), cross-link the dossier as the evidence trail, route methodological risks to `register-risk`, and move the dossier under `reports/archived/`. The dossier is research; the ADR is the committed decision.

## Required Output Structure (per verb)

- **init:** directory created · doc index (status per doc) · harness audit summary (existing guardrails / gaps) · next actions.
- **preregister:** the plan file path · its hypothesis + falsifiers in brief.
- **log:** the entry (+ postmortem if negative) · README status delta.
- **status:** roadmap position · log-integrity findings · next action.
- **promote:** the proposed-ADR path · risks routed · archival note.

## Performance Notes

- `init` is the heavyweight (the harness audit is repo-assimilation-flavored — take the time to *discover* existing guardrails rather than template a blank one).
- `log` and `status` are fast and frequent — keep them lightweight.
- The dossier's value compounds over time **only if the log stays honest** — guard the negatives-are-first-class rule above all.
- A dossier without a harness (`03`) is not ready to run experiments; `status` should refuse to call a program "ready" until the pre-flight checklist is green.
