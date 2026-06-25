---
name: autoresearch
description: Scopes and runs a falsification-first experiment lab — validates the metric, then iteratively modifies a designated file to optimize it, and closes with a decision + evidence. Use when the user says "autoresearch", "run experiments", "optimize this metric", "experiment loop", "autonomous optimization", or "run the research loop". Do NOT use for one-off code changes, code review, refactoring, test writing, or manual debugging.
---

## Important

Follow these rules strictly.

* **Scope before you optimize.** Do not enter the loop until the goal is clear and the metric has survived a validity check (Phases 0–1). "This isn't the right tool" and "fix the harness first" are valid, successful outcomes.
* **The metric is evidence, not truth.** Optimize it, but never trust it blindly — a metric can be deterministic, un-gamed, and still *wrong* (circular / proxy-divergent). Distrust the measure.
* Do not modify any file other than the designated `target_file`. Never edit the evaluation harness, metric, or `immutable:` paths — that is metric-gaming, the one thing that invalidates the whole loop. This holds **even when the metric is found to be bad**: surface it and stop; do not "fix" the harness inside a run.
* Do not install new packages or add dependencies beyond what already exists.
* Do not skip the baseline. The first experiment is always the unmodified code.
* Always commit before running an experiment. Always revert (`git reset --hard HEAD~1`) on a discard or fundamental failure. Always log every experiment — keep, discard, and crash.
* **L2 — the human holds closure.** Run bounded by default, checkpoint as you go, and stop-and-report on the conditions in `references/house-style.md`. Never take an irreversible or outward action (merge to a default branch, publish, tag, delete) without naming the exact step first.
* Close with a decision and its evidence (a NOTE + the committed ledger), not a dangling branch of commits.

## Purpose

Run a **falsification-first experiment lab**: scope what's actually being asked, validate that the metric
measures it, optimize via an autonomous edit→run→keep/discard loop, and close with a decision routed into
governance. Each experiment is a git commit; improvements are kept, regressions discarded.

The optimization engine is **Karpathy's autoresearch** pattern (https://github.com/karpathy/autoresearch —
"one GPU, one file, one metric"). The framing is the **AutoResearch survey** (arXiv 2605.23204): this is an
**L2 "Vibe Research"** tool — the agent executes, the human verifies and owns closure. The survey's lesson,
learned the hard way in our own `map_hdi` lab, drives the design: **execution is the easy part; validity,
rejection of weak directions, and provenance are the work.** A bare keep-if-the-metric-improved loop, run on
our `map_hdi` benchmark, would have kept a *circular* result and discarded the *real* fix — so this skill
puts a metric-validity gate before the loop and a decision/evidence handoff after it.

## Procedure

Six phases. Phases 0 and 1 can **halt the run** (a successful outcome). Depth lives in `references/`.

**Phase 0 — Scope & fit.** Establish a one-paragraph charter: *what are we trying to learn or improve, what
does "done" look like, and is this a single-metric hill-climb or a hypothesis-driven investigation where "no
clean win" is a real answer?* If a metric loop isn't the right shape, say so and stop — name the better
approach. Consult `references/house-style.md` (L2 posture) and `references/autoresearch-survey.md` (where this
sits on the autonomy spectrum and the favorable-but-dangerous domains).

**Phase 1 — Validate the evaluation (falsify the benchmark).** Before the loop is allowed to trust the
metric, attack it: **circularity** (does the oracle share construction with the optimization target?),
**proxy divergence** (re-score top candidates against an independent `secondary_metric` — does the ranking
hold or reverse?), **Goodhart pressure**, **coverage/adequacy**, **significance floor**. A metric can be
deterministic + un-gamed + still wrong. Work `references/metric-validity.md` as a checklist; you may run
`/falsify` on the benchmark. If the metric is circular/divergent/inadequate, **stop — the harness is the
deliverable** (and you may not edit it inside a run).

**Phase 2 — Setup.** Read `autoresearch.yaml`; create the isolated `autoresearch/<tag>` branch; read the
target; put the ledger in `.gitignore`; establish the baseline as experiment zero. Mechanics in
`references/karpathy-pattern.md`.

**Phase 3 — Bounded experiment loop.** `THINK → IMPLEMENT → COMMIT → RUN → MEASURE → GUARD → DECIDE → LOG`,
bounded by `max_iterations` with checkpoint synthesis. **KEEP** iff the metric improved by at least
`min_delta` **and** the `guard` (if configured) still holds — a metric gain that breaks the guard is not a
keep. The "metric is evidence, not truth" exception: once Phase 1 has shown the metric is a flawed proxy, a
metric-*worse* but principled change can be the right keep — flag it loudly and record why. Loop mechanics,
crash handling, simplicity criterion, resume, and ledger format (use the **`NA`** crash sentinel, not
`0.000000`) are in `references/karpathy-pattern.md`.

**Phase 4 — Diagnostics lane.** When the metric surprises you or Phase 1 raised a flag, write a **read-only
diagnostic** that interrogates the metric/benchmark/result (re-score, sweep, per-cell inspect). Diagnostics
are not loop iterations, are not on the ledger, and must not touch the immutable harness — but they are often
where the real finding lives (they were, in `map_hdi`). See `references/house-style.md`.

**Phase 5 — Close-out & handoff.** Synthesize a **research NOTE** (what was tried, what the metric did, what
diagnostics showed, the decision — including "no clean win"). **Commit the final ledger + NOTE** as the
evidence artifact. Route any actionable decision into an **ADR + risk-register** entry (`/register-risk`) for
the human to ratify; graduating code into a package goes through the normal gate + review, not the loop.
Consult `references/house-style.md`.

## Configuration

Read from `autoresearch.yaml` in the project root. If it does not exist, help the user write one in Phase 0
(do not guess values). **Required:**

```yaml
target_file: train.py                    # The ONLY file the loop may edit
eval_command: uv run train.py            # Command that produces the metric
metric_name: val_bpb                     # Human-readable metric name
metric_direction: lower                  # "lower" or "higher" is better
metric_pattern: "^val_bpb:\\s+(\\S+)"    # Regex to extract the metric from output
```

**Optional** (all back-compatible; older configs without these still work):

```yaml
time_budget: 300            # Max seconds per experiment (default 300)
results_file: results.tsv   # Ledger path (default results.tsv)
program: program.md         # Objective + guardrails; re-read at every THINK
immutable:                  # Paths the loop must NEVER edit (the eval harness)
  - benchmark/
  - run_eval.py
goal: "..."                 # Plain-language objective for the Phase-0 charter
guard: "uv run pytest -q"   # Invariant that must PASS alongside the metric (Phase 3)
secondary_metric: "..."     # Independent cross-check command for Phase-1 proxy-divergence
min_delta: 0.001            # Smallest improvement worth keeping (above the noise floor)
max_iterations: 25          # Bounded by default; null = unbounded opt-in (still checkpoints)
```

## Performance Notes

- The loop is the cheap part. Spend the rigor on Phase 1 (is the metric real?) and Phase 5 (what did we
  actually learn, and where does it go?). That is where labs succeed or quietly mislead.
- Recognize **search mode** vs **decide-and-ship mode**: for wide, cheap, well-specified search over a
  *trustworthy* metric, stay light and let the loop run; for anything feeding a decision, the governance
  weight is the point.
- Diagnostics over experiments when the metric surprises you. A read-only probe that explains *why* beats
  another blind edit.
- Determinism is mandatory: score against a fixed, cached benchmark; any randomness lives in the immutable
  harness under a fixed seed. A noisy metric makes keep/discard meaningless.
- Redirect eval output to `run.log`; never let it flood context. Grep the metric back out.
