# The Experimentation Harness (init's crown jewel)

The harness is *what makes experimentation safe* — the guardrails that stop a research program from (a) corrupting the stable system or (b) producing uninterpretable results. `init` **audits the repo for guardrails that already exist** and codifies them into `03_harness_and_invariants`, then flags the gaps. Do **not** template a blank harness — discover the real one (repo-assimilation-flavored).

## A. Invariant taxonomy (classify, don't lump)

The cardinal mistake is treating every current behavior as sacred. Split into three:

1. **Hard invariants — never break** (any experiment that violates one is invalid). E.g. fail-loud/no-silent-clamp, output-contract/parity, reproducibility, "the stable baseline stays the default and byte-identical when the new path is off," full suite green.
2. **Deliberately changed by this program (behind a flag).** State *what current behavior we intend to replace and how*, so reviewers don't defend it. Each change behind a default-off flag.
3. **Respect while changing.** Things not targeted but breakable in passing (e.g. a stability property, a sampling regime, a coupling) — call them out.

Source any existing constraints table (e.g. a prior `paths_forward`/design doc's design-constraints) and re-classify into these three.

## B. The standing harness — audit the repo for these (reuse, don't reinvent)

Detect and codify whatever the repo already has; flag any that are missing:

| Mechanism | What to look for |
|---|---|
| **Default-off feature flags** | config schema accepts a new option that defaults to current behavior; new path provably inert when off |
| **Parity / regression gates** | full test suite + a minimum-test gate; output-parity tests between paths; contract/CIC sync; TDD discipline |
| **Reproducibility** | seed/entropy lock; deterministic-algorithms flag; parameter/manifest audit; (note: bitwise GPU reproducibility is usually *not* guaranteed — say so) |
| **Fast, cheap readout** | a retrain-free / sub-minute probe that filters before expensive runs (so you don't burn a long job to learn what seconds would tell you) |
| **Evaluation comparability** | a *locked baseline* + a fixed metric protocol (proper scores; calibration; per-step trajectory) so new results compare honestly to old |
| **Run discipline** | one-heavy-job-at-a-time; resource ceilings; background + completion-notify; artifacts preserved/timestamped; config trap-restore around config-mutating runs |
| **Negative-result discipline** | a place and norm for postmortems (falsifications recorded, not buried) |
| **Hardware/runtime gates** | hard fail-loud if the expected accelerator/env is unavailable (no silent CPU fallback); verify the job is actually using the intended device |

## C. New harness this program needs (gaps to build first)

List what's *missing* for this specific program — e.g. a validated/loss numerics + its tests, a sampling path + tests, a calibration harness, NaN/Inf guards, a parity test proving the new path off == baseline. These are the real "before you experiment" work and gate the first run.

## D. Pre-flight checklist (must be green before the FIRST experiment)

A concrete checklist instance, e.g.:
- [ ] the new mechanism implemented + unit-tested (the numerically delicate part first) — **blocker**
- [ ] registered via the repo's extension seam (OCP), not by modifying the dispatcher
- [ ] behind a default-off flag; baseline byte-identical with it off
- [ ] fail-loud guards (NaN/Inf, device, contract) — no silent degradation
- [ ] full suite + lint green; contracts/CICs synced
- [ ] pre-analysis plan pre-registered (hypothesis + falsifiers + metrics vs the locked baseline)
- [ ] the fast readout adapted to the new path
- [ ] new failure modes noted for the risk register

`status` should refuse to call a program "ready to run" until this checklist is green.

## E. Decision/experiment protocol (the rules of engagement)

- **One variable at a time** (the bisect lesson) — each behind its own flag.
- **Pre-register, then run** (commit hypothesis + falsifiers before execution).
- **Cheap readout before expensive** (fast probe → only then the long run).
- **Falsifier honesty** — a pre-registered falsifier that fires kills the hypothesis; document it, don't rescue ad hoc.
- **Magnitude/behavior-neutral by construction** — improvements should come from better representation/method, not from masking (clamps, caps) that merely hide the symptom.

> Reassurance to surface in `init`'s report: much of B usually *already exists* — the honest finding "~70% of the harness is in place" is common and good. The new build is C (the program-specific mechanism + its tests + calibration).
