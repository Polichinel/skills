# Is the faoapi failure pattern platform-wide, or one bad week?

**Date:** 2026-08-23
**Status:** PRE-REGISTERED — this file was written and committed **before any data was collected.**
**Method borrowed from:** `views-faoapi/reports/measurements/2026-08-23_codebase_navigability.md`,
which pre-committed its interpretation table and was then contradicted by its own data in one
direction. That is the standard this measurement is held to.

## Why pre-register

The question is whether to build a mechanism in the skills repository. I proposed one (a plan↔diff
comparison) from a single incident. Generalising from n=1 is what the faoapi post-mortem's own
navigability measurement was designed to prevent — and that measurement *did* overturn its
expectation. Without a table fixed in advance I will find the pattern I went looking for.

## Hypothesis

The three failures recorded in `views-faoapi/reports/post_mortems/2026-08-23_two_months_of_empty_deliveries.md`
recur across views_platform, and are therefore worth a mechanism rather than a correction.

## Corpus

Fixed before collection: **70 post-mortems across 9 repositories**, and **1,307 `C-` entries across
16 registers**. `views-pipeline-core` and `views-stepshifter` have post-mortems but no register;
`views-lstm-lab` has a register but no post-mortems. Nothing is excluded.

## The three patterns, operationally defined

A **hit** requires an explicit statement in the record. Inference from surrounding narrative is a
near-miss, counted separately, never promoted.

**P1 — Plan-time overproduction.** Delivered work substantially exceeded what was asked, *and* the
excess originated in a plan or design the agent authored, rather than in drift during
implementation.
*Hit:* the record says something was not requested, not asked for, or self-proposed.
*Near-miss:* scope creep noted without attribution to a plan.

**P2 — Non-converging fix rounds.** Two or more successive rounds where a later round found defects
**created by** the earlier fix.
*Hit:* the record states a fix introduced the next defect.
*Near-miss:* repeated rounds recorded without a stated causal link between them.

**P3 — Guard never seen to fail.** An assertion, guard, test, or validator that could not fire, or
was credited with protection it did not provide.
*Hit:* the record states the check was vacuous, could never fire, tested the wrong thing, or passed
against the defect it was written to catch.
*Near-miss:* a guard found insufficient, without the claim that it could not fire.

## Interpretation table — fixed in advance

Counted in **distinct repositories**, not occurrences. Ten hits in one repo is one repo.

| repos showing the pattern | reading | consequence |
|---|---|---|
| 0–1 | faoapi-specific | **Do not build for it.** Correct it in faoapi and stop. |
| 2–3 | recurring | A small, targeted mechanism is justified. Nothing platform-wide. |
| 4+ | systemic | A platform-level gate is justified. |

## What the result decides

- **P1 systemic, P3 not** → the intervention belongs at plan approval. The plan↔diff comparison is
  warranted.
- **P3 systemic, P1 not** → the intervention is about verification quality, not planning. The
  plan↔diff comparison is **not** warranted and I withdraw it; faoapi#450 covers the real problem.
- **P2 systemic** → the intervention is a stop rule at the round boundary, which is neither of the
  above.
- **All three below 2** → the faoapi week was an outlier. Build nothing here.

## The falsifier, stated plainly

**If P1 appears in fewer than two repositories, the plan↔diff gate I recommended is unjustified and
this document will say so.** I proposed it before collecting any data and have an interest in it
surviving.

## Known limits of this method

- **The corpus is self-reported.** Post-mortems record what someone chose to write down. A repo with
  no post-mortems is not a repo with no failures; `views-models` has 138 register entries and zero
  post-mortems.
- **Detection is by search over text.** Guards that could not fire are invisible unless someone
  noticed and wrote it down — the same blind spot recorded as C-18 in this register, where a search
  for a form was published as a claim about a property.
- **Recording effort is not uniform.** faoapi has 194 entries and 6 post-mortems; bayesian has 20
  and none. Higher counts may measure diligence rather than incidence, and the table above therefore
  counts repositories rather than events.
