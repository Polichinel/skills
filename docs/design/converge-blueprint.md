# Blueprint: `converge` — coding philosophy as a standing constraint plus a drift check

| Field | Value |
|-------|-------|
| Status | **Design — not yet built.** No skill, no CLAUDE.md change has been made |
| Date | 2026-08-15 |
| Author | Simon (Polichinel), with Claude Opus 5 |
| Supersedes | The manually pasted prompt reproduced in Appendix A |
| Open | One further input from Simon, pending — see §9 |

---

## 1. Provenance — what problem this solves

Simon repeatedly pastes a ~1,200-word coding-philosophy prompt by hand before giving an agent implementation work. The full text is preserved verbatim in **Appendix A** and is the normative source for everything below.

The trigger for this design was the question "should this be a skill?" — asked without a settled answer. The investigation that followed changed the question.

---

## 2. Diagnosis — the document is two things in one coat

The pasted prompt does two jobs with different mechanical requirements.

**Job 1 — a standing constraint (~90% of the text).** "When implementing the tasks we agreed on, treat the following as my design preferences." This must apply passively to every implementation task and must be in context *before the first line of code is written*. A skill cannot reliably do this: skills dispatch on description match, and a skill described as "use whenever writing code" may load after the code already exists.

**Job 2 — an active decision procedure (~10%).** Four passages produce a *verdict* rather than a preference:
- Does this abstraction earn its existence? (Minimum Machinery)
- Is this a real third occurrence with real shared structure, or DRY reflex? (WET before DRY)
- Is this refactor converging, or generating open-ended work? (Convergence)
- **Should we stop?** (the explicit stop condition)

That is procedural, produces an output, and is only sometimes relevant — which is precisely the documented test for a skill.

---

## 3. Evidence — the literature review

Conducted 2026-08-15. This section exists so the reasoning survives without re-reading the sources.

### 3.1 Sources

| Source | Note |
|---|---|
| `The-Complete-Guide-to-Building-Skills-for-Claude.pdf` | Anthropic official, 30pp, already sitting in this repo, previously unopened |
| [Steering Claude Code: when to use CLAUDE.md, skills, hooks, and subagents](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) | Anthropic. Directly on this question |
| [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Live doc, substantially expanded beyond the PDF |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | Supporting |

### 3.2 The decisive rule

From the steering guide, verbatim:

> Build commands, directory layout, monorepo structure, **coding conventions, team norms** all fit naturally here [CLAUDE.md].

> Instructions that are **procedural** — like deploy workflows, release checklists, or review processes — belong in a skill rather than in CLAUDE.md.

> **If a rule must apply to all work, it is a fact, not a procedure**; put it in CLAUDE.md where it is always in context, or enforce it with a hook if it must hold deterministically. **Reserve skills for knowledge that is only sometimes relevant.**

"Coding conventions" is close to a literal description of Appendix A. The split in §2 is therefore the documented rule, not an aesthetic preference.

### 3.3 Constraints this imposes

- **CLAUDE.md budget: under 200 lines total.** Every line loads in every session and, per the guide, "dilutes adherence to instructions that actually matter." Appendix A verbatim would be 150+ lines and would consume nearly the whole budget while diluting itself. Compression is therefore required, not chosen. Simon's global `CLAUDE.md` is currently **3 lines**, so headroom exists.
- **SKILL.md body under 500 lines**; references one level deep from SKILL.md; reference files over 100 lines need a table of contents.
- **`description`: ≤1024 chars, third person, must state both what it does and when to use it**, and should carry negative triggers to prevent over-firing.
- **Naming**: gerund form mildly preferred (`converging`), but "inconsistent patterns within your skill collection" is listed under *Avoid*, and all 24 existing skills are non-gerund. Consistency wins; `converge` stands.
- **Enablement threshold**: the PDF advises evaluating whether more than 20–50 skills are enabled simultaneously. This repo has **24**. Adding skills is no longer free — the same context-budget concern already registered as C-02 and C-09.

### 3.4 The finding that cuts against current practice

PDF p.26, on model "laziness":

> Add explicit encouragement: *"Take your time to do this thoroughly / Quality is more important than speed / Do not skip validation steps."*
> **Note: Adding this to user prompts is more effective than in SKILL.md.**

Every one of the 24 existing skills ends with a `## Performance Notes` section doing exactly this. Anthropic's own guide says that placement is the weaker one. This is corroborating evidence for the design: behavioural steering lands harder outside `SKILL.md`.

### 3.5 Counter-evidence, recorded honestly

The literature is not unanimous. Public `coding-standards/SKILL.md` implementations exist in the wild, so shipping a philosophy as a skill is a thing people do. Anthropic's own rule is nonetheless unambiguous and points at CLAUDE.md for the bulk.

---

## 4. Failure modes — what actually goes wrong (evaluation-first)

The docs state:

> **Create evaluations BEFORE writing extensive documentation.** This ensures your Skill solves real problems rather than documenting imagined ones.

Simon confirmed **all four** failure modes occur, and that he pastes the prompt at **both** timings — up front on larger tasks, and again as a correction when drift appears anyway. This is what establishes that both halves are load-bearing.

| # | Failure mode | When it bites | Mechanism |
|---|---|---|---|
| 1 | **Over-engineering up front** — factories, interfaces, base classes, config layers for problems that didn't need them | Before code exists | **CLAUDE.md** — only a standing constraint can shape what gets built |
| 2 | **Scope creep mid-task** — redesigning adjacent code, renaming, restructuring untouched modules | After drift starts | **skill** — live intervention |
| 3 | **Premature abstraction (DRY reflex)** — two similar things get a shared helper immediately, usually the wrong one | At a decision point | **skill** — third-occurrence gate |
| 4 | **Never finishing** — working, understandable code keeps being reorganised toward a cleaner theoretical architecture | At the end | **skill** — stop verdict |

Prevention (#1) cannot be a skill. Interventions (#2–4) should not be CLAUDE.md.

---

## 5. Design

### 5.1 Half one — CLAUDE.md digest (~45 lines)

Target: `~/.claude/CLAUDE.md`, appended to the existing 3-line file.

Carries only operative rules, no exposition:
- The priority ordering: correctness → clarity → simplicity → testability → maintainability → extensibility → elegance
- Minimum Machinery — every abstraction, layer, wrapper, indirection earns its existence
- WET before DRY — 1st direct, 2nd duplicate acceptable, 3rd examine; abstraction still not mandatory
- Direct Representation — small distance between what code means and what it does
- Explicit State — no hidden globals, magic discovery, implicit mutation
- Scope discipline — smallest coherent change; note larger problems rather than expanding
- The stop condition
- SOLID and the component principles, explicitly flagged as heuristics, with the "do not introduce interfaces/factories/DI merely to demonstrate these" clause
- Repository should scream what it does; no `utils`/`helpers`/`common` dumping grounds
- A pointer naming `converge/references/philosophy.md` as the normative full text

Cut entirely: all exposition. Per the authoring guide, "Default assumption: Claude is already very smart" — it knows what SRP is. What it needs is Simon's *ruling* on SRP, which is "use judgment, do not build machinery to demonstrate it."

### 5.2 Half two — the `converge` skill

Draft frontmatter (third person, what + when + negative triggers, within 1024 chars):

```yaml
name: converge
description: Checks whether work in progress is converging on a finished state or
  generating open-ended refactoring. Audits whether each abstraction, layer, and
  indirection earns its existence, whether the change has drifted beyond the agreed
  task, whether a proposed abstraction is a real third occurrence or DRY reflex, and
  whether the implementation is done enough to stop. Use when the user says
  "converge", "is this over-engineered", "should I stop", "is this scope creep",
  "should I abstract this yet", or "is this done". Do NOT use for finding bugs (use
  expert-code-review), for pre-ship diff review (use review-diff), or for cleanup
  work itself (use tech-debt-cleanup).
```

Body: four checks mapping 1:1 onto failure modes #1–#4, then a verdict. Estimated ~80 lines, well inside the 500-line ceiling.

**Verdict vocabulary — deliberately subtractive.** Three of four outcomes reduce scope:

| Verdict | Meaning |
|---|---|
| **TRIM** | Machinery present that has not earned its existence — name what to remove |
| **NARROW** | Change has drifted past the agreed task — name what to hand back |
| **HOLD** | Not a real third occurrence, or shared concept is superficial — do not abstract yet |
| **STOP** | Correct, tested, understandable, reasonably extensible, appropriately simple, consistent with surroundings — ship it |

`references/philosophy.md` holds Appendix A verbatim with a table of contents, one level deep from SKILL.md.

### 5.3 The seam — why this is worth building

Every analysis skill in this repo **adds** work. `expert-code-review` has eight expert seats (Martin, GoF, Feathers, Nygard, Kleppmann, Ousterhout, Hickey, Beck) and every one of them is instructed to "identify," "assess," "evaluate." There is no seat whose job is to say *this is good enough*. `falsify` attacks claims. `review-rr` prioritises work. `tech-debt-cleanup` is work. The register those skills feed currently stands at 13 open concerns.

`converge` is the only skill that can **remove** work. That makes it orthogonal to all 24 existing skills, and it is the counterweight that makes the rest safe to run at volume.

Proposed entry for the README seams table:

| Boundary | Skill A owns | Skill B owns | Seam |
|----------|-------------|-------------|------|
| **converge** vs **expert-code-review** | Whether the work is finished and has earned its machinery | Whether the work is correct and well-structured across 8 expert lenses | Code review finds work; converge decides whether more work is justified. Run converge *after* a review to decide which findings to act on |
| **converge** vs **review-diff** | Is this change *done* and *scoped* | Is this change *readable and maintainable* before shipping | review-diff gates quality; converge gates scope and stopping |
| **converge** vs **tech-debt-cleanup** | Whether cleanup is warranted at all | How to perform cleanup safely once warranted | converge precedes cleanup and can veto it |

---

## 6. Evaluation plan — run before writing instructions

Three evals, one per intervention failure mode. Establish the baseline **without** the skill first. Any eval Claude already passes unaided means that part of the skill documents an imagined problem and should not be written.

| # | Scenario | Pass condition |
|---|---|---|
| E1 | Task that invites a registry or factory for a two-case problem | No factory/registry/abstract base appears; a direct implementation is produced |
| E2 | Task adjacent to code structured differently from the target file | Change stays in its lane; the structural observation is *noted*, not acted on |
| E3 | Working, tested, slightly inelegant code presented for assessment | Stops. Does not propose a cleaner theoretical architecture |

E1 principally tests the CLAUDE.md digest; E2 and E3 test the skill. A fourth eval for the DRY reflex (three similar functions, ask whether to abstract) should be added if E1–E3 prove informative.

---

## 7. Considered and rejected

| Option | Why rejected |
|---|---|
| **Skill only** | Cannot prevent failure mode #1. Skills dispatch on description match and may load after the code is written. Simon confirmed he pastes up front, which a skill cannot replicate |
| **CLAUDE.md only** | Simplest, and satisfies Minimum Machinery — but leaves failure modes #2–4 with no invocable check. Simon confirmed he also pastes mid-task as a correction, so this half is real |
| **Hook** | The steering guide reserves hooks for "anything that should happen deterministically" and warns "when there's something that absolutely must not happen, an instruction is the wrong tool." Appendix A is explicitly *"design preferences, not religious rules"* — nothing here is a hard guardrail. Eliminated by Simon's own framing |
| **Output style** | Carries the highest instruction-following weight and never gets compacted, which is genuinely attractive for surviving long sessions. Rejected as too heavy: output styles reshape core behaviour broadly, well past the scope of a design-preference document. **Worth revisiting** if the CLAUDE.md digest proves to decay over long implementation sessions |
| **A 9th seat in `expert-code-review`** | Cheapest option — add a convergence persona arguing against the other eight. Rejected because it solves none of the passive-constraint job and subordinates the philosophy to a review skill. **Still worth doing later as a complement**, not a substitute |
| **An `rnd-dossier`** | That skill is scoped to ML/research experimentation — pre-registration, experiment logs, falsifiers. Forcing a coding-philosophy design into it would violate Appendix A's own Minimum Machinery rule |

---

## 8. Risks and known costs

1. **Duplication between the digest and `philosophy.md`.** The same contract in two places with no generation — structurally identical to C-06 and D-01 in the risk register. Mitigation: `philosophy.md` is normative and the digest says so explicitly. Accepted, not eliminated.
2. **Skill count.** 24 skills against a documented 20–50 evaluate-your-enablement threshold. Adding a 25th has a real context cost. Related: C-02, C-09.
3. **Global scope.** A global `CLAUDE.md` applies to every repository, including third-party code with different conventions. Mitigation: an explicit deference clause — the philosophy yields to a repo's established conventions. **Unresolved** — see §9.
4. **The digest could dilute rather than steer.** If it grows past ~50 lines it starts competing with the instructions it is meant to support. Enforce the budget.
5. **`converge` could become another finder.** If the verdict drifts toward listing problems, it has become a ninth expert seat and failed. The subtractive verdict vocabulary is the guard; watch it in practice.

---

## 9. Open — decisions not yet made

- [ ] **Simon has one further input to add.** Reserved; this section is the slot for it. *(pending)*
- [ ] Global vs per-project scope for the digest, and whether to include a deference clause (risk 3)
- [ ] Whether to run the §6 evals before or after drafting the skill body — the docs say before
- [ ] Final name: `converge` vs `converging` (gerund) vs `earn-it` (rhymes with `ship-it`)
- [ ] Whether to add the convergence seat to `expert-code-review` as a follow-up

---

## 10. Build order, once unblocked

1. Resolve §9.
2. Run E1–E3 baseline **without** any new mechanism; record what actually fails.
3. Write the CLAUDE.md digest. Re-run E1. Measure.
4. Write `converge/references/philosophy.md` (Appendix A verbatim + TOC).
5. Write `converge/SKILL.md` — only the checks that E1–E3 proved necessary.
6. Re-run all evals with both halves in place.
7. Add the §5.3 seam rows to `README.md`.
8. Commit.

---

## 11. Evidence from views_platform

Investigation run 2026-08-15 across 21 risk registers (~27,000 lines) and 24 post-mortems (~3,200 lines) in `~/Documents/scripts/views_platform`. Read-only; nothing in that tree was modified.

**This section is additive.** §§1–10 record what was reasoned from first principles before any of this was read, and are left standing unchanged. Where the evidence contradicts them it is said plainly here and the original claim is not edited. Deciding what to do about a contradiction is a separate call, with §9 still open.

### 11.1 Convergence data (Q2)

| Repo | Total | Open | Resolved | Rate | Recorded curation / exit states |
|---|---:|---:|---:|---:|---|
| views-datafactory | 349 | 42 | 304 | **87%** | `[DEFER]`, demoted→tech-debt, merged IDs, separate `register_changelog.md`, guard test |
| views-frames | 78 | 14 | 64 | **82%** | disagreements tracked separately |
| views-postprocessing | 102 | 22 | 80 | **78%** | — |
| þingit | 13 | 4 | 9 | **69%** | scope note delegating content risks to another register |
| views-faoapi | 160 | 54 | 106 | **66%** | 5 demoted→tech-debt |
| views-baseline | 38 | 12 | 25 | **66%** | `Withdrawn` state |
| views-reporting | 78 | 11 | 67 | **86%** | — |
| views-models | 147 | 64 | 43+22 mit. | ~44% | **7 exit states**; `review-rr strategic` 2026-07-31 |
| views-hydranet | 285 | 133 | 152 | **53%** | `[DEMOTED]` + Tech-Debt Backlog; `review-rr strategic` 2026-08-15 took open 145→120 |
| views-appwrite | 64 | 52 | 12 | 19% | live/dormant split (37/15) |
| views-r2darts2 | 19 | 14 | 5 | 26% | — |
| views-stepshifter | 36 | 32 | 2 | 6% | `Invalidated` state |
| views-crafdapi | 26 | 25 | 1 | 4% | — |
| views-lstm-lab | 23 | 23 | 0 | **0%** | none |
| views-impact | 29 | 29 | 0 | **0%** | none |

The separator is not repo age or size — `views-datafactory` is the largest register and the most converged. It is **whether a curation pass was ever run and whether exit states other than "resolved" exist.** Every register above 60% has at least one of deferral, demotion, withdrawal, dormancy, or merging. Every register at 0% has only open/resolved.

### 11.2 Findings

**F1 — CORRECTED 2026-08-17. Was wrong. See `register_convergence.png`.**
*A drain, not a brake.* `review-rr` removes items already identified; it does nothing about the rate they arrive. Across 509 register commits in 10 repos: **51 concerns arrive per week, 33 resolve — net +10.5 open per week.** Nine of ten repos rise monotonically; `views-hydranet` went 14 → 142 open in four months, and the 2026-08-15 pass that took it 145→120 was undone in two days. One counter-example, and it is the useful part: `views-postprocessing` absorbed 78 concerns and ended where it started (22 → 22). 52 entries record a reopen, retraction or revert, so "resolved" is not terminal.

**F2 — QUALIFIES §4.** *Architecture is a minority failure class.*
Root-cause taxonomy across the 24 post-mortems: roughly **8 data/correctness** (grid-id leak, 603 unmapped GAUL cells, RNG drift, stale zarr, pre-deploy checks), **7 ML/method negative results** (locked dropout, gated ZINB core, explosion/rollout, hard-gate escalations, target compression, multi-target, Cramér distance), **4 process/governance** (falsification process, both eftirmál, epic 339), **4 architecture/complexity** (extraction, ontology liberation, data backbone, hydranet roadmap). The blueprint's four failure modes are real but account for roughly a sixth of recorded incidents. §4's evaluation-first premise holds; its implied *weight* does not.

**F3 — CONTRADICTS the §2/§4 premise.** *The philosophy is already operating, in Simon's own vocabulary, inside the registers.*
The vocabulary sweep found it being applied at live decision points, by agents, unprompted:
- *"the user's **WET-before-DRY preference** says write 3 times before abstracting"* — his rule, cited by name, in a register entry
- *"Kernel factory rejected as **over-abstraction** — duplication is structurally intentional"*
- *"the balancer does not **earn its place**"* — the philosophy's own phrase
- *"a polymorphic interface would be speculative (**YAGNI/ISP**: don't force an interface nobody dispatches on)"*
- *"defer composition as **gold-plating** (revisit only if #100 adds a second consumer — REP/CCP)"*
- *"fixing an unused function mid-epic is **scope creep**"*
- *"a **premature abstraction** would have outlived the implementation it existed to unify"*

The pasted prompt is not introducing a missing constraint. It is already propagating.

**F4 — SUPPORTS §5.1 (WET before DRY). Strongest single confirmation in the corpus.**
`views-reporting/documentation/extraction_postmortem.md`: *"**WET-before-DRY was the right call.** Moving code as exact copies, without simultaneous refactoring, kept each PR reviewable and individually revertible. The temptation to 'fix it while we're moving it' was real … but mixing extraction with remediation would have made every PR a gamble instead of a mechanical step. The refactoring happened afterward, on stable ground, with tests in place."* An 8,285-LOC extraction, 20 PRs, validating the rule by name.

**F5 — QUALIFIES §5.1 (Minimum Machinery). The deliberate counter-evidence hunt (Q3).**
Three incidents were fixed by *adding* structure, not removing it:
- `views-hydranet/.../2026-02-02_final_post_mortem_and_roadmap.md` — *"The common thread was **Implicit Knowledge**. The code 'guessed' where the Time, ID, and Spatial dimensions were using magic numbers … When the data structure shifted, the code didn't fail — it drifted."* Fixed by adding the `VolumeHandler` custodian, a role ledger, and a Planner/Lens split. This validates **Explicit State** while cutting against **Minimum Machinery**, and the tension is real: the same `VolumeHandler` is the worked example of responsibility accumulation in `review-rr/references/analysis.md`. Machinery added correctly, then over-accumulated.
- `extraction_postmortem.md` C-01 — a module-level singleton corrupted **20% of MAP estimates** under joblib threads, silently, shipping for an unknown duration. *"Module-level mutable singletons in a library that uses joblib are a Tier 1 risk by default."*
- `evaluation_ontology_liberation` — *"**The config is the contract.** Moving from implicit inference (prefix → transformation → metric space) to explicit declaration made every failure mode visible."*

And one unrecorded tension: `post_mortem_data_backbone.md` builds a `ReferenceGeometryReader` Protocol for a **single** implementation, justified as *"If we want to switch to fiona or pyogrio later, nothing else changes"* — textbook speculative generality, cited approvingly as *"Uncle Bob's dependency inversion,"* and **not logged as a regret anywhere.** Appendix A forbids exactly this. The digest needs a qualifier: minimum machinery is a rule about *speculative* machinery, not about structure that makes state explicit.

**F6 — REVISES §8 risk 5 and constrains §5.2.** *A check that fires on correct behaviour destroys its own authority.*
`þingit/eftirmál_02.md` §3(f): *"**a check that fires on correct behaviour teaches people to ignore checks.** V9 is currently in that state."* §3(e): the length cap *"fires on everyone and therefore teaches nothing"* — the doubter spent *"six editing passes across two turns chasing 2.6% of a soft cap and at one point made the file longer."* That is a governance mechanism manufacturing exactly the churn `converge` exists to stop. If `converge` returns TRIM or NARROW on well-scoped work, it will be ignored within weeks. §8 risk 5 anticipated the failure; this names the mechanism and gives it a measured precedent.

**F7 — RECASTS §1 and §4.** *The dominant recorded cost is process machinery, not code machinery.*
`eftirmál_02.md` §4, the operator's own words:
- *"The cognitive load of you saying 'one item', 'two small things', etc is immense and soul crushing."*
- *"I have not been able to work on any of the involved repos or move forward"* — and *"it's been quite demanding in tokens."*
- *"I barely understand 1, 2, 3, or 4 because of jargon and shorthand. I have no idea if we are at a good place or if this is now completely inbred garbage."*
- *"How can I ratify when I don't know what I am ratifying?"*

§5's one-sentence lesson: the mechanism *"is worth nothing to the person paying for it unless every artifact that reaches them is written in language they can act on without a translator."* The blueprint aims a brake at over-engineered **code**. The loudest recorded pain is over-engineered **process** — and `converge` would be more process. That does not sink it, but it means the skill must be judged on the operator's cognitive load, not only on the code it improves.

**F8 — ADDS a fifth failure mode not in §4.** *Wrong-diagnosis thrashing.*
Two independent occurrences:
- `post_mortem_data_backbone.md`: *"I went down a rabbit hole of `uv pip install`, `.venv/bin/python -m pytest`, and other hacks — the user rightfully stopped me. The second time … I started doing the same thing before catching myself."* Lesson: *"Diagnose the root cause before trying workarounds."*
- `postmortem_pgm_forecast_stripe_grid_id_leak.md` §7: *"**First diagnosis was wrong: blamed the plotting tool.** … That was confidently stated and **wrong**."*

Confident wrong diagnosis followed by escalating workarounds is distinct from all four §4 modes, is operator-visible, and is arguably more expensive.

### 11.3 Null result

**No post-mortem in the corpus attributes an incident to over-engineering as its root cause.** Zero of 24. Over-abstraction appears in registers as a *decision avoided* (F3), never in a post-mortem as a *failure suffered*. Failure mode #1 in §4 is real as a tendency Simon corrects for, but it has not yet caused a recorded incident. E1 in §6 should be expected to come back weak.

### 11.4 Observations (Q4, capped — recorded for a later pass, not chased)

- **Minimum Machinery, discovered independently for governance.** `eftirmál_02` §6: *"**Deliberately not proposed: more roles, more clauses, more checks.** `eftirmál_01` produced eleven improvements and all eleven were built; the marginal one is worth less than the last."*
- **Conversion tracking as the honesty measure.** `eftirmál_02` §7 tracks rows-created → rows-closed per matter: *"It is the only honest measure of the mechanism, and it is the one the operator asked for."* §6's evals could adopt this.
- **Line numbers are the wrong citation unit.** `views-evaluation`: *"`Location` fields name files and symbols, not line numbers — line numbers drift as soon as anything is inserted above them."* The skills register cites line numbers throughout.
- **Exit-state taxonomies vary widely** — `views-models` runs seven (Open / Mitigated / Resolved / Accepted / Partially Resolved / Subsumed / Merged); `views-appwrite` has live vs dormant; `views-baseline` has Withdrawn; `views-stepshifter` has Invalidated.
- **`views-metric-lab/reports/technical_risk_register.md` is a byte-identical stale copy** of `views-lab00`'s, still titled "views-lab00".
- **`views-hydranet/tests/test_risk_register_integrity.py`** and `views-datafactory`'s `test_falsification_merge_readiness.py` (an 8,000-char search-window guard) are mechanical register checks — the thing C-03 and C-14 say the skills repo lacks.

### 11.5 Examined, not relevant

`postmortem_epic_339` (scope-of-review lessons, cross-repo verification — relevant to review practice, not to `converge`) · `un_fao_delivery` pre/post-run pair · `pre_deploy_post_mortem` ×2 · `postmortem_cm_unmapped_gaul_cells` · `postmortem_training_nondeterminism_init_rng_drift` · `postmortem_locked_dropout_negative_result` · `postmortem_gated_zinbcore` · `09_postmortem_explosion_needs_rollout` · `postmortem_exp01_hard_gate_drops_escalations` · `11_postmortem` (target compression) · `post_mortem_multi_target_investigation` · `post_mortem_report` · `cramer_distance/POSTMORTEM.md` · `views-bayesian/meta/lessons_log.md` (template, near-empty) · `eftirmál_01` (superseded by `_02` for these questions).

### 11.6 Coverage and honesty notes

- 21 registers: headers read in full; bodies swept mechanically, not read. `views-datafactory`'s `register_changelog.md` and archive were **not** read — capped per Q4.
- 24 post-mortems: 6 read in full, 18 classified by structure and root-cause sections. The plan said read all in full; this is a **logged cap**, not silent truncation. The 18 are all data/ML incident reports whose titles and root-cause headings were sufficient to classify for F2.
- **Conflict of interest:** §§1–10 and this section have the same author. F1, F2, F3, F5 and the §11.3 null result all cut against the blueprint; they are reported because Q3 and verification step 5 exist to force the attempt. A reader should still weight this section as self-assessment.

---

## Appendix A — the source document, verbatim

Preserved exactly as pasted. This is the normative text; the CLAUDE.md digest is a derived summary of it.

> When implementing the **task or tasks we have agreed on**, treat the following as my **design preferences, not religious rules**. Use judgment.
>
> The goal is not architectural purity. The goal is a codebase that is correct, clear, robust, easy to change, easy to test, and that **converges rather than generating endless refactoring work**.
>
> ## Low-level design
>
> Prefer the SOLID principles where they genuinely improve the design:
>
> * **SRP — Single Responsibility Principle:** one class/module should have one main reason to change.
> * **OCP — Open/Closed Principle:** prefer designs that can be extended without repeatedly rewriting stable code.
> * **LSP — Liskov Substitution Principle:** subtypes should behave correctly wherever their parent type is expected.
> * **ISP — Interface Segregation Principle:** do not force callers to depend on methods they do not need.
> * **DIP — Dependency Inversion Principle:** high-level logic should depend on appropriate abstractions rather than unstable implementation details.
>
> Do not introduce interfaces, base classes, factories, wrappers, or dependency injection merely to demonstrate these principles.
>
> ## High-level architecture
>
> Prefer:
>
> * **REP — Reuse/Release Equivalence Principle:** things reused together should be released together.
> * **CCP — Common Closure Principle:** things that change together should live together.
> * **CRP — Common Reuse Principle:** things not reused together should not be forced together.
> * **ADP — Acyclic Dependencies Principle:** component dependencies should not form cycles.
> * **SDP — Stable Dependencies Principle:** dependencies should point toward more stable components.
> * **SAP — Stable Abstractions Principle:** stable components should contain enough abstraction to survive expected change.
>
> Again, use these as heuristics, not as reasons to invent components.
>
> ## Repository structure
>
> The repository should **scream what it does**.
>
> * Files and folders should be clearly separated by responsibility.
> * The package structure should make the major concepts and workflows obvious.
> * A file should normally contain one main class or one main concept.
> * Multiple classes in the same file should be the exception, not the default.
> * Keep classes together only when they are genuinely tightly coupled and form one coherent unit.
> * Inheritance-related classes may sometimes belong together, but do not let this encourage large inheritance trees.
> * Prefer composition over inheritance when composition expresses the relationship more directly.
> * Do not create dumping-ground `utils`, `helpers`, `common`, or similarly vague modules for unrelated things.
> * If a file accumulates loosely related helpers, constants, types, and classes, treat that as a signal that the boundaries may be wrong.
> * A new developer should be able to inspect the directory tree and quickly understand what the system does and where its major responsibilities live.
>
> ## Keep the implementation lean
>
> Balance the architectural principles above with the following.
>
> ### Minimum Machinery
>
> Use the least machinery that solves the actual problem clearly and correctly.
>
> Every new:
>
> * abstraction,
> * layer,
> * class,
> * interface,
> * registry,
> * factory,
> * wrapper,
> * configuration mechanism,
> * indirection,
> * or framework
>
> must earn its existence.
>
> Do not solve hypothetical future requirements unless there is a concrete reason to believe they are coming and the current design would make them unnecessarily difficult.
>
> Prefer a simple function over a class when a function is enough.
>
> Prefer a direct call over an indirection when the indirection buys nothing.
>
> Prefer a small explicit implementation over a general framework for a problem that is not yet general.
>
> ### Direct Representation
>
> Represent the actual problem as directly as possible.
>
> Prefer straightforward data structures, functions, pipeline stages, and transformations that correspond closely to the domain over elaborate architectural representations of them.
>
> The distance between **what the code means** and **what the code does** should be small.
>
> ### Explicit State
>
> Keep important state, configuration, inputs, outputs, dependencies, and side effects visible and traceable.
>
> Avoid:
>
> * hidden global state,
> * magic discovery,
> * implicit mutation,
> * surprising side effects,
> * behavior controlled indirectly from unrelated parts of the codebase.
>
> For ML pipelines in particular, make it easy to understand:
>
> * what data enters a stage,
> * what transformation happens,
> * what configuration controls it,
> * what model or artifact is produced,
> * and where the result goes next.
>
> ### WET before DRY
>
> Prefer **WET before DRY**.
>
> Duplication is often cheaper than the wrong abstraction.
>
> Do not generalize simply because two pieces of code look similar.
>
> Allow concrete implementations to exist long enough for the true common structure to become clear.
>
> As a rough heuristic:
>
> * First occurrence: implement it directly.
> * Second occurrence: duplication is acceptable.
> * Third occurrence: examine whether a real abstraction has emerged.
>
> Even then, abstraction is not mandatory.
>
> Abstract only when:
>
> 1. the shared concept is real rather than superficial,
> 2. the abstraction makes the system easier to understand or change,
> 3. the abstraction has a clear responsibility,
> 4. and the resulting system is simpler overall.
>
> Do not replace obvious duplication with an abstraction that is harder to understand than the duplicated code.
>
> ### Convergence
>
> The codebase should move toward a finished state.
>
> Refactoring should normally do at least one of the following:
>
> * solve a concrete problem,
> * remove meaningful complexity,
> * clarify an important boundary,
> * eliminate a demonstrated source of bugs,
> * make testing materially easier,
> * or make an expected change materially easier.
>
> Do not continue reorganizing working, understandable code simply because another theoretically cleaner architecture exists.
>
> Do not turn every implementation task into an architectural cleanup.
>
> Do not create new work solely because a principle can be applied more perfectly.
>
> If the implementation is:
>
> * correct,
> * tested,
> * understandable,
> * reasonably extensible,
> * appropriately simple,
> * and consistent with the surrounding codebase,
>
> **stop.**
>
> ## Prefer local improvement over rewrites
>
> When modifying an existing system, preserve working structures unless there is a concrete reason to replace them.
>
> Prefer the smallest coherent change that leaves the surrounding code better than you found it.
>
> Do not redesign unrelated parts of the repository as collateral work.
>
> If a larger architectural problem is discovered but does not need to be solved for the current task, note it rather than automatically expanding the scope.
>
> ## Overall priority
>
> When these principles conflict, optimize roughly in this order:
>
> **correctness → clarity → simplicity → testability → maintainability → extensibility → elegance**
>
> Architecture is a means, not an end.
>
> Prefer **direct, explicit, boring code that is finished** over a theoretically beautiful architecture that keeps generating more work.
>
> Good architecture should reduce the cost of change. It should not itself become a permanent source of change.
