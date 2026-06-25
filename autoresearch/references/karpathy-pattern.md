# The Karpathy pattern — the engine, its discipline, and its limits

Source: Karpathy's `autoresearch` (https://github.com/karpathy/autoresearch). Companion explainers:
datasciencedojo.com/blog/karpathy-autoresearch-explained, deepwiki.com/karpathy/autoresearch. A
generalized Claude-Code port is uditgoenka/autoresearch.

This file holds the **mechanical engine** (the loop, setup, crash handling, resume, ledger) and an honest
account of **what the bare pattern can and cannot do**. Phases 2–4 of `SKILL.md` run this engine; Phases 0,
1, and 5 are the additions that make it safe and useful for our work.

## What it is

An AI agent hands the ML research *loop* to itself and runs it overnight: edit one file, run a fixed-budget
experiment, keep if a single metric improved, else `git revert`, log, repeat. *"By morning it's a clean
record of every change that actually worked."* Karpathy reports ~700 experiments/night and an 11% speedup on
an already-optimized codebase. Design motto: **"one GPU, one file, one metric."**

## The two disciplines worth keeping

These two are genuinely good and non-negotiable; carry them verbatim.

1. **Separation of concerns — immutable harness, single sandbox.** The benchmark + metric live in an
   **immutable eval harness** (`prepare.py`); the agent edits **only** the one `target_file` (`train.py`).
   Editing the harness is *metric-gaming — the one thing that invalidates the whole loop*. `program.md`
   carries the human's objective and constraints. If `immutable:` paths are configured, treat editing them
   as forbidden.
2. **Determinism.** The eval must return the *same* score for the *same* code — score against a **fixed,
   cached** benchmark, not freshly-sampled data. A noisy metric makes keep/discard meaningless: the loop
   "keeps" lucky noise and "discards" real gains. Any randomness (e.g. a stability bootstrap) lives in the
   immutable harness under a fixed seed, never in the sandbox.

**Important limit of these disciplines:** they protect against *gaming* and *noise*. They do **not** protect
against a harness that is honestly built, deterministic, un-gamed, and **wrong** (circular / proxy-divergent).
That gap is what `references/metric-validity.md` and Phase 1 exist to close.

## Setup (Phase 2)

1. **Read config** (`autoresearch.yaml`, project root). Validate required fields; if missing, stop and ask.
2. **Run tag + branch.** Propose a date tag (e.g. `mar16`); create `autoresearch/<tag>` from the current
   branch so experiments are isolated. The branch must not already exist.
3. **Read the target file** (and any context files) to understand the starting point. You may *read*
   anything; you may *edit* only `target_file`.
4. **Ledger in `.gitignore`.** Add `results_file` to `.gitignore` so it survives `git reset --hard`.
5. **Initialize the ledger** with the header: `commit  metric_value  status  description` (tab-separated).
6. **Baseline = experiment zero.** Run the eval on unmodified code; record it. (Note: if the metric is on a
   revised harness, the baseline is the *new* harness's number — old-harness scores are not comparable.)

## The loop (Phase 3)

```
LOOP (until max_iterations, or a stop condition, or interrupt):
  1. THINK      — review ledger + target; state a specific hypothesis in 1–2 sentences. Re-read `program.md`.
  2. IMPLEMENT  — edit ONLY target_file to implement the hypothesis.
  3. COMMIT     — git add <target_file>; git commit -m "experiment: <what changed>".
  4. RUN        — <eval_command> > run.log 2>&1, with a timeout = time_budget. Redirect; never flood context.
  5. MEASURE    — grep metric_pattern from run.log. Empty ⇒ crash (see Crash handling).
  6. GUARD      — if a `guard` is configured, it must PASS. A metric gain that breaks the guard is NOT a keep.
  7. DECIDE     — KEEP iff the metric improved by at least `min_delta` AND the guard holds; else DISCARD via
                  git reset --hard HEAD~1. (See SKILL.md Phase 3 for the "metric is evidence, not truth"
                  exception, and the simplicity criterion below.)
  8. LOG        — append: commit(7) | metric_value | status | description (tabs, not commas).
```

**Simplicity criterion** (applied before keeping): marginal gain + significant added complexity → discard;
gain from *deleting*/simplifying → always keep; large gain + complexity → keep, note the cost; equal metric +
simpler code → keep. When in doubt, prefer simpler code.

**When ideas run dry:** re-read the target fresh; review the ledger for patterns; combine two past wins; try
the opposite of recent failures; try a more radical change; try *removing* code. Think harder, not shorter.

## Crash handling

When the eval crashes (empty metric, non-zero exit, or timeout):
1. `tail -n 50 run.log`.
2. **Fixable bug** (typo, import, shape): fix, re-commit, re-run — max 2 fix attempts per experiment.
   **Fundamental failure** (OOM, won't converge): discard immediately (`git reset --hard HEAD~1`), log `crash`.
3. If the eval exceeds 2× `time_budget`, kill it and treat as a crash.

## Ledger format

Tab-separated. `commit`: short hash (7) — use `0000000` for reverted crashes. `metric_value`: the number —
use **`NA`** for crashes (not `0.000000`, which can masquerade as a valid score when `metric_direction:
higher`). `status`: `keep` | `discard` | `crash`. `description`: brief.

```
commit	metric_value	status	description
a1b2c3d	0.997900	keep	baseline (unmodified)
b2c3d4e	0.993200	keep	increased learning rate to 0.04
c3d4e5f	1.005000	discard	switched to GeLU activation
0000000	NA	crash	doubled model width (OOM)
```

## Resume

Ledger persists on disk; branch persists in git. To resume: re-invoke, read the existing ledger + branch
state, re-confirm Phase 0/1 still hold, then re-enter the loop. Do **not** re-run setup.

## What the bare pattern is good for — and what it is not

**Good for:** wide, cheap, well-specified *search* over a single trustworthy metric (hyperparameters,
architecture, optimizer) where iteration is fast and the score genuinely tracks the goal. Here the loop is
strictly better than hand-tuning, and our governance ceremony is overhead — recognize "search mode" and stay
light.

**Not good for, on its own:**
- *Validating its own metric.* The loop trusts the score; it cannot tell circular/proxy-divergent from real.
- *Expressing "no clean win."* keep/discard has no slot for "the honest answer is no improvement, here's what
  we learned" — yet that is a frequent, valuable result.
- *Delayed / heterogeneous / accountable validation.* The 5-minute-comparable-score model assumes fast,
  homogeneous, automatable evaluation.

The community has already felt these limits: **uditgoenka's productized fork** added a **"guard clause"
(an invariant that must always pass alongside the metric)** and switched from "run forever" to **bounded runs
(default 25) with checkpoint reports**. That is the bare loop rediscovering that a single metric is
insufficient and infinite autonomy is unwise — which is what Phases 1, 3 (guard/bounded), and 5 encode here.
