# The AutoResearch map — where this skill sits, and what it's judged against

Source: *AutoResearch AI: Towards AI-Powered Research Automation for Scientific Discovery* (Tie et al.,
arXiv **2605.23204v1**, May 2026). Local copy: `~/brain/9_library/incoming/autoresearch/2605.23204v1.pdf`
(§4 Evaluation and §6.4 Reliability/Auditability are the most relevant). This file distills the parts that
should shape how a lab is scoped, run, and judged. Read it in **Phase 0** (scope) and **Phase 1**
(validate the evaluation).

The one-line takeaway: **this skill is an L2 tool, and the hard part of a lab is not execution — it is
validity, rejection of weak directions, and provenance.** The loop automates the easy part.

## The autonomy spectrum (L0–L4)

The survey frames research automation not as "more AI" but as a *redistribution of control, execution,
validation, and accountability* across the workflow. Five levels:

- **L0 — Human Only.** AI absent from the research loop.
- **L1 — Human-Led, AI-Assisted.** AI accelerates bounded cognitive tasks (search, drafting, lightweight
  analysis); humans decide, execute, validate, and own every consequential judgment.
- **L2 — Human-Verified, AI-Executed.** AI executes substantive multi-step work — edits files, runs
  analyses, invokes tools, produces intermediate artifacts — but **scientific authority for verification,
  acceptance, and accountability stays human-held.** "Vibe Research."
- **L3 — AI-Led, Human-Assisted.** AI organizes larger spans of the workflow (grounding, planning,
  rejection, revision); humans supervise and intervene in high-risk/uncertain cases. A *stricter frontier*,
  not a realized regime.
- **L4 — AI-Autonomous.** End-to-end closure without humans structurally necessary. The survey is explicit:
  **"No current system meets that standard."** L4 is "an analytical upper bound rather than a realized
  target."

**This skill operates at L2.** The agent executes the loop; the human (Simon) holds closure — accepting
results, ratifying decisions, merging, publishing. The survey's central warning is precisely against
drifting past this: *"the principal evaluative risk is to mistake productivity gain for stronger autonomy…
Pipeline breadth may increase task substitution, but it does not imply AI-led autonomy unless decision
authority, rejection, stopping, and responsibility are also redistributed away from routine human
verification."* A loop that runs 500 experiments overnight is still L2 if a human decides what the result
means.

## The five scientific-quality dimensions

The survey's evaluation frame: scientific quality is **five jointly necessary judgment targets**, distinct
from the *evidence instruments* (benchmarks, reruns, expert review) used to support them. A benchmark score
is one piece of evidence, **not** a scientific judgment.

| Dimension | The question it asks |
|---|---|
| **Novelty** | Does the workflow advance understanding beyond literature-adjacent recombination? (Non-obvious, plausibly useful, expands the search space. *"Novelty is not exhausted by unfamiliarity."*) |
| **Validity** | Is the full **question → method → execution → conclusion** chain warranted? Methodological adequacy, execution correctness, evidence–claim alignment. *The decisive criterion.* |
| **Impact** | Does it matter beyond local task completion? (Least captured by standard benchmarks; most easily faked by weak proxies — leaderboard movement, paper acceptance.) |
| **Reliability** | Does it behave consistently enough to be *trusted as an instrument*? Rerun stability, sensitivity to seed/prompt, failure exposure & recovery. |
| **Provenance** | Are claims, data, artifacts, interventions **traceable after the run ends**? The condition under which correction and post-hoc verification remain possible. |

### The central error: "authority borrowing"

The most important sentence in §4 for us: *"the central evaluation error in current AutoResearch practice is
therefore not simply under-measurement, but **authority borrowing**: a system is often presented as if
strength on one dimension implied strength on all the others."*

> Novelty without validity is speculation. Validity without provenance is hard to trust. Reliability without
> impact is operational competence without scientific importance.

A single-metric autoresearch loop is an **authority-borrowing machine by construction**: it measures one
narrow proxy (often reliability/local performance) and the kept-commit branch *presents* that as if it
established validity. The `map_hdi` lab is the worked example — see `references/metric-validity.md`. This is
why Phase 1 (validate the evaluation) exists.

### Validity, specifically, names the map_hdi failure

> "A workflow can be original, coherent, and even reproducible in a narrow sense while still **failing
> validity if its conclusions are unsupported, its controls are weak, or its analysis is mismatched to the
> question.**"

A deterministic, un-gamed, reproducible metric that is *circular* (analysis mismatched to the question) is a
validity failure even though it passes every reliability check. The loop cannot see this; only an explicit
validity probe can.

## Autonomy assessment (the other axis)

Scientific quality is one side; the survey pairs it with **autonomy assessment** — four variables that
determine what autonomy claim the evidence actually supports: **task substitution, decision authority,
workflow closure, responsibility retention.** For our labs this is the L2 checklist: the agent may substitute
a lot of *task* execution, but decision authority / rejection / stopping / responsibility stay with the
human. Keep that line bright (see `references/house-style.md`).

## The domain-conditioned ceiling

The survey's thesis: the autonomy ceiling is **domain-conditioned**, not uniform. Higher autonomy is more
credible where artifacts are *structured, executable, and rapidly verifiable* (computational/formal sciences);
more limited where claims depend on *delayed validation, heterogeneous evidence, embodiment, or institutional
accountability*.

Implication for scope (Phase 0): a `views-frames`-style lab — numpy code, a deterministic benchmark, a
fast eval — sits at the **favorable** end. That is exactly where a tight metric loop is *most* useful and
*most* dangerous: useful because iteration is cheap and verifiable; dangerous because a clean, fast,
reproducible score is the easiest place to mistake a circular proxy for a real result.
