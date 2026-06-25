# House style — how we run a lab

Read this in **Phase 0** (scope) and **Phase 5** (close-out). It tailors the generic loop to how we
actually work, which differs from a generic user in three ways: we are **L2** (the human holds closure), we
**distrust the measure**, and a lab's real output is a **decision with evidence**, not a branch of kept
commits.

## We are L2 — the human holds closure

The agent *executes* the loop; the human (Simon) *decides what it means* and owns every irreversible or
outward step. Concretely:

- **Never take an irreversible / outward action without naming the exact step first** — merging to a
  default branch, publishing, tagging, deleting, anything hard to undo. Approval for one step is not
  approval for the next.
- **Bounded by default, not "run forever."** Default to `max_iterations` (≈25) with a **checkpoint
  synthesis** every N iterations (what's been tried, what the ledger shows, whether to continue or pivot).
  Unbounded autonomy is opt-in (`max_iterations: null`) and even then it checkpoints. The original Karpathy
  "run until interrupted, never ask" is an L4 posture; we are L2.
- The autonomy line is the survey's: the agent may substitute a lot of *task execution*, but **decision
  authority, rejection, stopping, and responsibility stay human.** Running more experiments does not move us
  up the autonomy spectrum (see `references/autoresearch-survey.md`).

## Stop-and-report conditions

Halt the loop and surface to the human (do not silently continue or "fix" your way past) when:

- Phase 1 finds the **metric is circular / divergent / inadequate** — the harness is the problem, and you may
  not edit the immutable harness inside a run.
- A change would require touching an **immutable path** or a **sibling repo** to make progress.
- The result implies an **irreversible/outward action** (merge, publish, tag).
- The loop has **plateaued** (K checkpoints with no meaningful gain) — report the plateau and the best
  honest read, rather than grinding.
- Anything **surprising** that the charter didn't anticipate.

## "No clean win" is a valid, valuable outcome

The keep/discard loop has no native way to say "the honest answer is *no improvement*, and here is what we
learned." We do. A lab that ends with *"the metric can't be beaten without gaming it; the real ambiguity is
X; the recommendation is Y"* is a **success**, not a failure. The `map_hdi` lab's most valuable output was
exactly this shape. Do not manufacture a win to have a win.

## Diagnostics vs experiments

Two different activities; keep them distinct:

- **Experiments** edit `target_file`, are committed, scored, and kept/discarded. They climb the metric.
- **Diagnostics** are *read-only probes* that interrogate the metric/benchmark/result (re-score against a
  secondary measure, sweep a parameter, inspect per-cell behavior). They are **not** loop iterations, are
  **not** scored on the ledger, and must **not** touch the immutable harness.

The lesson of `map_hdi`: the loop produced a circular "win"; the *diagnostics* (`point_pass.py`,
`density_sweep.py`) produced the actual insight. Treat diagnostics as first-class — when the metric surprises
you or Phase 1 raises a flag, write a diagnostic before trusting another experiment.

## Close-out & governance handoff (Phase 5)

A lab ends with a **decision backed by evidence**, routed into our governance — never just a dangling branch.
The `map_hdi` template: lab → **`NOTE.md`** → **ADR-019** → register **C-32/C-33** → graduated production
code. Required closing steps:

1. **Research NOTE.** Write up what was tried, what the metric did, what the diagnostics showed, and the
   decision (including "no clean win"). This is the provenance artifact — the survey's fifth dimension — the
   thing that lets a future reader reconstruct and trust (or overturn) the conclusion.
2. **Commit the evidence.** Commit the **final ledger + NOTE** (the ledger is gitignored *during* the run so
   it survives resets; at the end it becomes the committed evidence trail). Lab code stays tracked but
   un-gated; the production code, if anything graduates, is the source of truth.
3. **Route the decision.** If the lab concludes something actionable, open/extend an **ADR** and a
   **risk-register** entry (via `/register-risk`), and let the human ratify. Graduating code into a package
   is an additive change that goes through the normal gate + review + their acceptance — not something the
   loop ships.

## Relationship to the other house skills

The autoresearch skill does not re-implement what we already have — it composes:

- **`/falsify`** — the Phase-1 tool. Run it *on the benchmark* to attack the metric's validity, exactly as
  it's run on an artifact before a publish.
- **`/register-risk`** — the Phase-5 intake for any concern/decision the lab surfaces.
- **`/review-diff`, the gate (lint/type/100%-coverage/floor), ADRs/CICs** — the path any graduated code
  takes into production. The lab proves the idea; the governance ships it.

The through-line: the loop is the cheap part. Validity, rejection of weak directions, and provenance are the
work — and they are exactly the parts we already have machinery for. Use it.
