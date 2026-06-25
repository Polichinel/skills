# Validating the evaluation — before you trust a single number

Read this in **Phase 1**. It exists because of one hard-won lesson:

> **A metric can be deterministic, un-gamed, reproducible — and still wrong.**

The Karpathy disciplines (immutable harness, fixed seed) defend against *gaming* and *noise*. They do
**nothing** against a metric that is circular, a divergent proxy, or Goodhart-able. The survey
(`references/autoresearch-survey.md`) calls the resulting failure **authority borrowing**: a good score is
presented as if it established *validity*, when validity — "is the question→method→execution→conclusion
chain warranted?" — was never tested. A single-metric loop is an authority-borrowing machine by
construction. Phase 1 is the antidote: **falsify the benchmark before the loop is allowed to trust it.**

This is the same move that is Step 0 of a publish (run `/falsify` on the artifact). Here the *artifact under
suspicion is the evaluation itself.* You may literally invoke `/falsify` on the benchmark.

## The worked example — the `map_hdi` lab (why this file exists)

A real autoresearch run in this repo (`research/map_hdi/`, ledger `results.tsv`, write-up `NOTE.md`):

- Goal: find a better point estimate (mode/MAP) for conflict posteriors. Metric `tower_score`, lower better.
- The benchmark stored a `true_mode` that was **itself a histogram argmax**.
- The loop's **best** result: `0.3335 — point = sample histogram-MAP (oracle binning)`. It won *because a
  histogram-MAP matches a histogram-argmax oracle by sharing its binning.* **Circular.**
- The real fix (the C-32 median-proximity tie-break) scored `0.359` — "worse" — and was **discarded**.

Followed literally, the bare loop would have **shipped the circular artifact and rejected the real fix.**
What caught it was not the loop but two **read-only diagnostics** that interrogated the metric:
- `point_pass.py` re-scored against the **analytic** mode (non-circular). The incumbent's edge shrank or
  reversed, and on `low_zi_active` cells the histogram oracle was *hiding* a large failure: **0.24 circular
  vs 0.82–1.07 analytic.**
- `density_sweep.py` showed the real ambiguity was **multimodality**, not anything the metric was rewarding.

Outcome: not a metric win, but a *decision* — ship the tower-tip + a bimodality flag (ADR-019; C-32/C-33),
and leave a principled convergent mode open (#89). The score got *worse*; the science got *better*.

## The Phase-1 checklist

Run these before trusting any ranking. Any "yes" (or "can't rule out") is a **stop-and-investigate**, not a
footnote.

1. **Circularity.** Does the metric's oracle / label / target share *construction* with the thing being
   optimized? (Same binning, same model family, same preprocessing, same heuristic.) If the optimizer can
   win by *resembling the scorer* rather than *being right*, the metric is circular. — *map_hdi: true_mode =
   histogram argmax; histogram-MAP wins by sharing binning.*
2. **Proxy divergence.** Re-score the top candidates against an **independent secondary measure** (a
   different oracle, a held-out construction, an analytic ground truth, expert judgment). Does the ranking
   **hold or reverse**? If it reverses, the primary metric is a divergent proxy. (Configure `secondary_metric`
   for this.) — *map_hdi: analytic re-scoring reversed the ranking.*
3. **Goodhart pressure.** Is the metric optimizable in *degenerate* ways that don't serve the goal? (Exploit
   a tie-break, a boundary, a smoothing constant, a tiny tail.) If a cheap degenerate edit moves the score,
   the score is gameable even without touching the harness.
4. **Coverage / adequacy.** Does the benchmark span the *real* distribution the result must generalize to,
   or does it average over a regime where the metric is blind? A headline mean can **hide** a catastrophic
   sub-population. — *map_hdi: the aggregate oracle hid the `low_zi_active` failure.*
5. **Significance floor.** Is the smallest "improvement" the loop will keep larger than the metric's own
   noise floor? If not, the loop ratchets on noise. (Set `min_delta` accordingly; see determinism in
   `references/karpathy-pattern.md`.)
6. **Construct validity.** Does the number actually measure the thing in the Phase-0 charter, or a
   convenient stand-in? ("We wanted a *principled* mode; the metric rewards *proximity to a histogram
   argmax*" — not the same thing.)

## What to do with the result

- **Metric survives Phase 1** → proceed to the loop, and re-run checks 1–2 periodically (a metric can become
  divergent as the search pushes into its blind spots).
- **Metric is circular / divergent / inadequate** → the honest output is *"fix the harness first"* (the
  benchmark is the deliverable, not `target_file`). Note: you may **not** edit the immutable harness inside a
  run to "fix" it — that is gaming. Surface it, stop, and let the human revise the harness (then re-baseline).
- **Either way, diagnostics are first-class.** Read-only probes that interrogate the metric/benchmark (like
  `point_pass.py`) are not loop iterations and don't touch the immutable harness — but they are often where
  the real finding lives. See the diagnostics lane in `SKILL.md` Phase 4.

The governing instinct: **distrust the measure.** A green number is the easiest place to hide a wrong
result — in this lab and in any publish.
