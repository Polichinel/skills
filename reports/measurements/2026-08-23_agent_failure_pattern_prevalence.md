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

---

# RESULTS — collected 2026-08-23, after the above was committed (`77439f8`)

## Counts, in distinct repositories

| pattern | repos | band | consequence per the fixed table |
|---|---:|---|---|
| **P1** plan-time overproduction | **2** | recurring | small targeted mechanism justified; nothing platform-wide |
| **P2** non-converging fix rounds | **2** | recurring | same |
| **P3** guards that could not fire | **9** | **systemic** | **a platform-level intervention is justified** |

**P3 hits:** views-faoapi, views-postprocessing, views-appwrite, views-crafdapi, views-evaluation,
views-frames, views-impact, views-models, views-pipeline-core.
**P1 and P2 hits:** views-faoapi, views-postprocessing.

## The falsifier fired — I withdraw the plan↔diff gate

The pre-registered rule was: *"P3 systemic, P1 not → the intervention is about verification quality,
not planning. The plan↔diff comparison is **not** warranted and I withdraw it."*

P3 is systemic at 9 repositories. P1 sits at 2 — real, but four and a half times narrower, and both
instances are ones a human already caught in-flight. **The gate I proposed before collecting data is
not what the evidence supports, and it is withdrawn.**

## What the search got wrong on the way, and it is the register's own C-18

The first P1 sweep returned four files across three repositories. On reading them, three were false
positives: *"nobody asked what else in `file.py` pages"* (views-pipeline-core, twice) is
**under**-investigation, the opposite of overproduction, and views-hydranet's *"the independent
cross-check nobody asked for"* is a ten-line validation table framed as a virtue. A fourth sweep on
broader terms returned nine repositories, of which the readable hits were views-appwrite naming
scope creep **prospectively** as a risk, and views-baseline and views-hydranet recording proposals
**declined** as over-engineered — evidence of the discipline working, counted as evidence of its
failure.

Had I reported file counts, P1 would have read as 9 repositories and systemic. That is C-18 exactly,
committed inside the measurement written to avoid it.

## The finding that was not pre-registered, and matters more than the counts

P3's mechanism is stated precisely in two independent repositories, and it is not a discipline
problem.

**views-postprocessing** (2026-08-12): *"The author proposed thirteen forms and proved all thirteen
caught. An independent review proposed twenty-nine."*

**views-frames**: *"a check written to catch that can itself pass vacuously in at least three ways,
and **every one of them was found by someone other than its author**."*

**An author cannot test what they did not imagine.** No instruction fixes that, because the failure
is in the author's model of what could go wrong, and the guard is written from that same model. It
is why 19,229 lines of tests in views-faoapi did not catch eight weeks of empty deliveries, and why
1.46 lines of test per line of source bought nothing.

## Interventions already measured on this platform

Recorded here because they were tested in production incidents, with outcomes, and none needs to be
invented.

| intervention | measured outcome | source |
|---|---|---|
| **Adversarial mutation reviewer** — briefed *only* to supply mutants the author had not thought of | *"the single highest-value input of the arc."* Five parallel reviewers found what **four rounds of self-review had not** | views-postprocessing 2026-08-12 |
| **The one-home rule** — reasoning lives in the register; ADRs record decisions, never implementation | #248 took **twelve** commits; #243, the first under the rule, took **five**. *"the only intervention that moved the number"* | same |
| **No number without a command in the same turn** — nothing reaches a comment, commit or ADR unmeasured | adopted mid-sprint after a figure was posted wrong, corrected, and the correction was also wrong | same |
| **Refusing to chase** — write down what is *not* being fixed, and why | *"prevented a sixth round"* | same |
| **Deletion as default remedy** | three of five stories were net deletions; each closed its defect more completely than a repair | same |
| **Maintainer intervention mid-flight** | nine stories of widening became three; shipped | same |

## A second unregistered finding: the prose, not the code

views-postprocessing measured **341 lines of code against 452 lines of docs and register** in that
arc — *"one and a third lines of prose for every line of code. And nearly every defect the reviews
found lived in the prose, not the code."* Its diagnosis of the engine is mechanical and worth
carrying: an ADR that describes current implementation *becomes a second copy of the code and rots
on every change*. Most of #248's twelve commits were repairing implementation descriptions that
should never have been in an ADR.

This directly contradicts the initial diagnosis in that same incident (*"the guard surface is
bloated"*, which produced a wrong acceptance criterion). The corrected finding: **the prose was
bloated; the guards were mostly missing.**

## Limits of this result

- **Detection tracks reading effort.** P1 and P2 were confirmed only in the two post-mortems I read
  in full. Other repositories were searched, not read. Both counts are lower bounds and the gap
  between 2 and 9 is partly an artefact of how deeply each corpus was examined.
- **P3 is likely under-counted for the opposite reason.** A guard that cannot fire is invisible until
  someone notices; nine repositories recorded it, and nothing suggests the search is exhausted.
- **Two repositories dominate the qualitative evidence.** views-faoapi and views-postprocessing
  wrote the most detailed post-mortems, which is why they supply most of the mechanism. Diligence,
  not incidence.
