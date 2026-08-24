# Technical Risk Register

| Register Info     | Details                              |
|-------------------|--------------------------------------|
| Project           | claude-code-skills                   |
| Owner             | Polichinl (simmaa@prio.org)          |
| Last Updated      | 2026-08-24                           |
| Total Concerns    | 19                                   |
| Open Concerns     | 15                                   |
| Resolved Concerns | 4                                    |

---

## Tier Definitions

| Tier | Severity | Description |
|------|----------|-------------|
| 1 | Critical | Silent data corruption or model output correctness risk. Requires immediate attention. |
| 2 | High | Structural fragility that will cause failures under realistic change scenarios. |
| 3 | Medium | Maintainability or coupling issues that increase cost of change. |
| 4 | Low | Code quality concerns that do not affect correctness or reliability. |

---

## Open Concerns

### C-19: the guard-mode gate shipped with the defect its own catalogue calls M6 — correct, and never runs

| Field | Value |
|-------|-------|
| ID | C-19 |
| Tier | 2 |
| Source | pr-review (2026-08-24, reported by the views-pipeline-core session) |
| Trigger | Before treating "ship-it will catch it" as coverage for anything — a decorative guard, an unaudited fix, a test added in a hurry — check whether the branch in question was actually shipped through `ship-it`. If any commit reached the remote by raw `git push`, the gate did not fire and there is no audit record. |
| Location | `ship-it/SKILL.md` (Step 5.5), `falsify/references/guard_mutations.md` (M6, which names this exact failure), `scripts/install-hooks.sh` (the pre-push hook precedent this does not use) |

Guard mode was wired into `ship-it` Step 5.5 on 2026-08-23 so that guards are audited without anyone naming a test file. The step is correct — subagent with a clean context, gates the push rather than the commit, stops on DECORATIVE or WEAK. It fires only if someone invokes `ship-it`, and nothing requires that.

Reported by the session working on views-pipeline-core PR #483, which verified Step 5.5 does what it claims and then observed that **every commit on that branch reached the remote by raw `git push`, including the commits that added guards.** The gate has never fired there. Bypass rate in the only repository with data: 100%.

**The 100% is one branch, and the source said so before I did.** It is a single branch whose author had the tool available and did not reach for it, which may measure that author rather than the gate. Treat it as an existence proof that the bypass is trivially available, not as a rate. What is not sample-dependent is the structure: nothing in the design requires `ship-it`, so the gate's coverage equals the fraction of pushes that happen to go through it, and that fraction is unmeasured everywhere else.

This is M6 from guard mode's own mutation catalogue — *"Correct, and never runs"* — whose recorded instances are views-faoapi's `smoke.py check_coverage` (a correct assertion that runs only when a human deploys) and this register's own C-15 (the external-paths check, skipped in CI). A guard published as protection, credited as coverage, and executed by nobody, is the failure the skill was built to detect, committed in the skill that detects it.

The fix is not more instruction. `scripts/install-hooks.sh` already establishes the pattern: a pre-push hook is deterministic and cannot be skipped by choosing a different command. A hook cannot run the audit itself — that needs a model — but it can refuse a push whose commits touch tests and carry no audit record. Not built; recorded, because building it unprompted is the pattern this repository spent 2026-08-23 measuring.

See also C-15 (same shape, same repository, different artifact — the strongest check runs nowhere by default) and C-16 (the other place where an instrument reports on itself and cannot distinguish working from absent).

Related, from the same reporter: views-pipeline-core C-304 generalises the prose-drift diagnosis this exchange started from. Measured across four artifacts, mechanism-naming density did **not** predict correction count — the artifact with the lowest density had nearly the most corrections. What rotted there was prose copying *observables* of other kinds: verdict strings lifted from a renderer, a behavioural claim that was true when written and false two commits later, and a fact about the world that had already changed. The rule is wider than ADRs describing code: **any prose that copies any observable rots when the observable moves.** That applies directly to this register, which quotes line counts, finding counts and verdicts throughout.

---

### C-18: a cross-repo census was published as measurement into 16 issue trackers, and its negative claims were wrong in 3 of 11 cases

| Field | Value |
|-------|-------|
| ID | C-18 |
| Tier | 3 |
| Source | manual (2026-08-23) |
| Trigger | When work driven from this repository is about to assert a **negative** about another repository — "no enforcement test", "no contract", "not declared" — and that assertion will be published as a GitHub issue, comment, or report: verify by the property, not by the search. If that is not possible, state the detection method and what forms it would miss, in the published text. |
| Location | No in-repo artifact holds the census — it existed only in conversation and now in 16 external issue bodies. `docs/design/converge-blueprint.md:226-229` is the nearest record, and mentions the campaign without the measurements. |

On 2026-08-18 an import-topology census across all views_platform repositories was filed as an investigative issue in sixteen of them. Eleven of those issues asserted `enforcement test: **none**`. Three were false: `views-bayesian` had a 200-line `tests/test_layer_boundaries.py` guarding seven of ten packages, `views-postprocessing` had `tests/test_clone_readiness.py` (named in its own ADR-002 as the mechanical enforcer of the `contract/ ↛ unfao/` seam), and `views-baseline` had a permanent acyclicity guard inside a `/falsify` artifact. The detection method searched for `[tool.importlinter]` blocks and import-enforcement-shaped filenames, so every guard named for something else was invisible to it — and absence of a match was published as absence of the property.

That is the same C-350/C-351 shape the issues themselves are about: an assertion about a proxy standing in for an assertion about the property. The cost is not hypothetical — `views-bayesian#4` recommended building a guard that already existed, and `views-baseline#83` recommended doing nothing on the grounds the repo was too small, when it in fact already held the property by a better mechanism. Corrections are posted on all three. The eight remaining "none" claims were re-checked and stand.

Tier 3 rather than 2: the failure produces wasted or misdirected work in other repositories, not incorrect behaviour in any running system. It escalates if a negative claim of this kind is ever used to justify **removing** an existing guard.

See also C-15 (`check_skill_names` has the same shape — backtick-and-slash detection publishes silence about bare prose mentions) and C-17 (an absence that was never recorded as deliberate).

---

### C-17: the rule's record of what it deliberately excludes has one entry, and lives where neither Claude nor a reader will see it

| Field | Value |
|-------|-------|
| ID | C-17 |
| Tier | 3 |
| Source | manual (2026-08-23) |
| Trigger | When you next believe a preference is missing from `~/.claude/rules/design-preferences.md` and are about to add it: check whether it was ever in Appendix A first, and record the answer as a "deliberately not here" line **whether or not you add the ruling**. An unrecorded absence is the thing that invites the next addition. |
| Location | `~/.claude/rules/design-preferences.md:22-25` (the sole exclusion note, inside a block HTML comment stripped before the file enters context), `docs/design/converge-blueprint.md:394` (Appendix A, the normative source) |

The rule file carries exactly one record of a deliberate omission — acyclic dependencies, excluded because import-linter enforces them deterministically. Everything else the rule does not say is indistinguishable from an oversight. On 2026-08-23 that surfaced: test-driven development was believed to be part of the rule, was not, and had never been in Appendix A either — the source mentions testing four times and every one is a *property* of finished code (`easy to test`, `tested`, `testability`), never a process. The compression was faithful; the gap was in the record of scope, not in the rule.

The exclusion note is also doubly invisible. It sits inside the HTML comment that is stripped before Claude sees the file, and nothing surfaces it to a human either — the rule is never opened in normal use, because the whole point of a path-scoped rule is that it loads without being asked for. So the one mechanism guarding against unbounded growth is the mechanism least likely to be read.

Tier 3: the failure mode is additive. Each unrecorded absence invites a patch, each patch is a line whose *why* is weaker than the eight that were compressed from a source document, and the file grows in exactly the way the design cited (arXiv 2608.11095, +226% instruction growth, rewrites resuming growth faster) was built to avoid.

See also C-18 (an unrecorded negative, published) and C-16 (the other blind spot in this rule's instrumentation).

---

### C-16: the rule-load breadcrumb proves a load happened, not that the rule arrived

| Field | Value |
|-------|-------|
| ID | C-16 |
| Tier | 3 |
| Source | manual (2026-08-23) |
| Trigger | When the design preferences appear not to be followed and you reach for `~/.claude/logs/instructions.jsonl` as evidence: it cannot answer that question. Check the rule file's own size and frontmatter first — an empty, truncated, or broken-frontmatter file produces a log entry identical to a healthy one. |
| Location | `~/.claude/hooks/log-instructions.sh:24` (`bytes: ((.file_content // "") \| length)`), `~/.claude/logs/instructions.jsonl`, `~/.claude/rules/design-preferences.md` — all three outside this repository and therefore outside `scripts/validate_skills.py` entirely |

The `InstructionsLoaded` payload carries no `file_content` field, so the `bytes` value the hook was written to record is `0` on 76 of 77 logged loads. What the log proves is that Claude Code matched the path glob and attempted the load — file path, `load_reason`, session, cwd, timestamp. What it cannot distinguish is a rule that arrived in full from one that arrived empty.

This matters because `docs/design/converge-blueprint.md:228-229` names this log as *the* evidence for the open question of whether the rule earns its place at all. It is good evidence for reach — 77 loads, 14 sessions, 13 directories, none in a prose session, which is the scoping working. It is no evidence at all for content. The gap is in the harness, not the hook: no other field in the payload substitutes.

Tier 3: nothing corrupts if the rule silently empties — code simply gets written without the preferences, which is the pre-2026-08-17 baseline and was measured to pass four evals unaided. The cost is that the one instrument built to answer "is this working" would read identically in the case where it had stopped.

See also C-14 (the same family: an invariant stated in prose, enforced by nothing, invisible when violated) and C-15 (the validator's enforcement gap — this is a fourth artifact it cannot reach, because it lives outside the repository).

---

### C-15: the validator's strongest check runs nowhere by default, and it has two documented blind spots

| Field | Value |
|-------|-------|
| ID | C-15 |
| Tier | 3 |
| Source | pr-review (2026-08-17) |
| Trigger | When cloning this repository onto a new machine, run `bash scripts/install-hooks.sh` before trusting CI — without it the external-paths check, the only thing that catches C-01, executes in no automated place at all. |
| Location | `.github/workflows/validate.yml` (`--skip external-paths`), `scripts/install-hooks.sh`, `scripts/validate_skills.py` (`check_skill_names` docstring, `prose_files` docstring, `KNOWN_NONSKILLS`) |

`scripts/validate_skills.py` closes C-03, but three gaps are known and deliberate rather than accidental, and all three are the sort a future reader would otherwise assume away.

**Enforcement.** external-paths resolves `~/brain/...`, which exists only on this machine, so CI skips it. It is enforced by a pre-push hook that must be installed per clone. A fresh clone has full CI and zero protection against C-01 recurring.

**Detection — bare prose.** `check_skill_names` matches backticked and slash-command forms. Two of C-04's four historical sites were bare mentions in running prose and are not detected. Proximity-based detection was attempted and withdrawn: it false-positived on ordinary hyphenated adjectives (`whole-codebase`, `version-controlled`, `large-scale`), each needing another filter, which is guard accumulation ending in a check nobody trusts.

**Detection — `reports/`.** Excluded from prose checks. The reason is structural, not convenience: a register that tracks dangling-name concerns necessarily contains dangling names. Section-aware scanning was tried — skipping Resolved Concerns still leaves hits in *open* entries, including this one, because open entries discuss the same history. The cost is real: the stale `clean-architecture-review` Source value fixed by hand in this change lived in `reports/`, so a recurrence there would go unseen.

Tier 3 rather than 2: every gap degrades to a loud failure at invocation rather than silent corruption — a broken `base_docs` path stops `init-base-docs` at Phase 1, it does not produce a wrong governance tree. The cost is rediscovery by hand, which is what C-01 and C-04 already cost once.

See also C-14 (prose-only invariants failing silently — same family, different artifact).

---


### C-02: graphify embeds an 800-line program that auto-installs a package and drifts from its pinned version

| Field | Value |
|-------|-------|
| ID | C-02 |
| Tier | 2 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | Two independent conditions. **(a)** When someone runs `/graphify` on a machine where `import graphify` fails, Step 1 silently runs `pip install graphifyy -q` and then retries with `--break-system-packages` — verify what is being installed, and against which Python interpreter, before letting it proceed. **(b)** When `graphifyy` is upgraded past the `0.4.6` recorded in `graphify/.graphify_version`, verify the embedded call sites in `SKILL.md` still match the library API. Nothing checks either condition. |
| Location | `graphify/SKILL.md:62-89` (install block), `graphify/SKILL.md` (1,276 lines / 54,664 bytes, 30+ embedded Python blocks through line 1,270), `graphify/.graphify_version` |

`graphify` is the only skill that ships a full program inside its prompt rather than instructions for one — 20x the median `SKILL.md` size, larger than any complete `references/` tree in the repo — and it violates the progressive-disclosure pattern `README.md:98-104` declares universal and that the other 23 skills follow. Two compounding failures. First, Step 1 installs a PyPI package unprompted, falling back to `pip install graphifyy -q --break-system-packages`: a system-level mutation performed without user confirmation, with output suppressed by `-q` and `2>&1 | tail -3` so a failed or partial install is invisible. Second, `.graphify_version` pins `0.4.6` but nothing compares it against the installed package, so roughly 800 lines of embedded call-site code can silently diverge from the library API it targets, producing malformed graphs rather than errors. The skill's own "Honesty Rules" section (line 1,270) governs edge provenance (EXTRACTED/INFERRED/AMBIGUOUS), not either of these. Not currently mitigated.

See also C-09 (C-02 is the extreme case of the flat-vs-split layout inconsistency).

---


### C-05: single-user absolute paths hardcoded across five skills

| Field | Value |
|-------|-------|
| ID | C-05 |
| Tier | 3 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When someone uploads an individual skill folder via Claude.ai Settings > Capabilities > Skills — an installation mode `README.md:94` explicitly offers — or clones this repository onto a second machine, verify that the hardcoded `/home/simon/...` paths in `library/SKILL.md` and `thingit/SKILL.md` resolve. |
| Location | `library/SKILL.md` (~20 occurrences of `/home/simon/brain/9_library/library_system`), `thingit/SKILL.md:14,21`, `expert-method-review/SKILL.md:15`, `verify-sources/SKILL.md:56`, `persona-critique/SKILL.md:62` |

`library` hardcodes a fully-qualified single-user absolute path roughly twenty times, including inside every executable bash block, and `thingit` hardcodes `/home/simon/Documents/scripts/views_platform/þingit/`. `README.md:94` offers "upload individual skill folders" as a supported installation path, under which neither skill can function. The tilde-relative variants in `expert-method-review`, `verify-sources`, and `persona-critique` are marginally more portable but still assume a specific vault layout — precisely the assumption whose violation produced C-01. No skill declares its external dependencies in frontmatter or checks them before use. Mitigated only in `thingit`, whose Step 0 `ls`/`cat` on `$ROOT` fails loudly and immediately.

Symptom of C-03. See also C-01 (the same assumption already broken for `base_docs`) and C-09 (`library`'s flat layout is why its hardcoded paths sit inside executable bash blocks in the prompt file).

---

### C-06: cross-skill seam contracts are stored in triplicate with no generation

| Field | Value |
|-------|-------|
| ID | C-06 |
| Tier | 3 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When someone changes what a skill owns or produces — for example altering `verify-sources`' delegation condition to `/library verify`, or changing which directories `strategic-draft`'s minimal bootstrap creates — verify all three copies of the contract: the README seams table and both participating `SKILL.md` files. |
| Location | `README.md:83-90`, `verify-sources/SKILL.md:168-173`, `expert-method-review/SKILL.md:56`, `persona-critique/SKILL.md:56`, `rnd-dossier/SKILL.md:15`, `register-risk/SKILL.md:22`, `writing-harness/SKILL.md:66-70`, `strategic-draft/SKILL.md:57-61` |

Six responsibility boundaries are documented in the README seams table and restated in prose inside both participating skills — three copies of each contract, none generated from the others. The design is deliberate (`README.md:81`: "Skills compose through filesystem artifacts, not programmatic APIs") and the seams themselves are unusually well specified, naming who owns what and how the other side delegates. The cost is dual maintenance: a one-sided edit leaves two stale descriptions behind with no detection mechanism, and the affected skills continue to run while routing work to the wrong owner. Commit `7cb1d9c` ("formalize cross-skill seams") introduced the triplication in bulk, so all six pairs share the same drift exposure. Not currently mitigated.

Related to C-03 (a generated or validated seams table would close this). See also C-04 (same line, `register-risk/SKILL.md:22`, dangling-name aspect) and D-01, which records the deliberate trade-off that produces this cost — C-06 is the residual price of that choice, not a defect in it.

---

### C-08: autoresearch loop correctness rests entirely on prose, with the hardening config keys optional

| Field | Value |
|-------|-------|
| ID | C-08 |
| Tier | 2 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When someone runs `/autoresearch` against a project whose `autoresearch.yaml` omits `immutable:`, `guard:`, `secondary_metric:`, or `min_delta:` — all four are documented as optional and back-compatible — verify Phase 1's metric-validity conclusions independently before trusting the resulting NOTE. |
| Location | `autoresearch/SKILL.md:12` (immutable-paths rule), `autoresearch/SKILL.md:112` (determinism requirement), `autoresearch/SKILL.md:55-61` (Phase 3 loop), `autoresearch/SKILL.md:87-101` (optional config keys) |

The loop's correctness rests on three invariants enforced by prose alone: only `target_file` may be edited; the evaluation harness is immutable "even when the metric is found to be bad"; and the metric must be deterministic against a fixed cached benchmark. Violating any of them produces a clean `results.tsv`, a monotonically improving metric, and a confident research NOTE — the failure is invisible in every artifact the skill emits. The skill's own text records that this already happened once: a bare keep-if-the-metric-improved loop run on the `map_hdi` benchmark "would have kept a *circular* result and discarded the *real* fix" (`autoresearch/SKILL.md:30`), which is why the Phase 1 metric-validity gate exists. But Phase 1 is a checklist a model works through, not a check a machine runs, and the four config keys that would harden it are optional with no warning emitted when absent. A Tier 1 case can be argued — the identified path is: optional keys omitted, loop edits the harness or optimizes a noisy metric, artifacts stay clean, downstream conclusion is wrong with no error signal. Tier 1 was considered and rejected on three grounds: the corruption lands in a downstream research conclusion rather than in data this repository owns; the likelihood is conjunctive rather than near-certain, requiring omitted config *and* a flawed metric *and* Phase 1 failing to catch it; and two explicit mitigations exist — the Phase 0–1 gates, which can halt a run as a successful outcome (`autoresearch/SKILL.md:10`), and the L2 posture at `autoresearch/SKILL.md:16`, "the human holds closure," which places a required human verification step between the loop's output and any decision built on it. Adjudicated and held at Tier 2 during review-rr strategic review (2026-08-15).

Distinct from C-03 in that no test of this repository would catch it — the risk is in the protocol design, not in unverified files.

---

### C-09: flat-versus-split skill layout is inconsistent and untracked to size

| Field | Value |
|-------|-------|
| ID | C-09 |
| Tier | 4 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When someone adds a new skill, decide flat-versus-split deliberately and record the reason in the README skill table — no rule exists, and `README.md:98-104` documents only the split. |
| Location | `graphify/SKILL.md` (1,276 lines, flat), `library/SKILL.md` (475, flat), `verify-sources/SKILL.md` (181, flat), `ship-it/SKILL.md` (84, flat), `thingit/SKILL.md` (128, flat) versus `init-repo/SKILL.md` (129, split), `tech-debt-cleanup/SKILL.md` (64, split) |

Five skills are flat single files and nineteen use the `SKILL.md` + `references/` split, and the choice does not track size: `library` at 475 lines is flat while `tech-debt-cleanup` at 64 lines is split. `README.md:98-104` presents the split as the structure, without qualification. The practical cost is context budget — a flat skill loads its entire body on description match, so invoking `/library` pulls roughly 20KB of embedded bash into context before the user's subcommand is even known. No correctness or reliability impact, and scope is a single developer, which places this at Tier 4.

See also C-02 (the same inconsistency taken to an extreme that does carry correctness risk) and C-05 (`library`'s flat layout is why its hardcoded paths sit inside executable bash blocks).

---

### C-10: skills ingest untrusted external content into their own reasoning with no isolation

| Field | Value |
|-------|-------|
| ID | C-10 |
| Tier | 2 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When someone runs `/graphify add <url>` against a page they do not control, or `/library add` on a PDF from an untrusted source, read what was written into `./raw` or `papers/` before the extraction step consumes it — the pipeline auto-advances without a review gate. |
| Location | `graphify/SKILL.md` ("For `/graphify add`" section), `library/SKILL.md:230-330` (`add` extraction phases), `verify-sources/SKILL.md:93-105` (Phase 5 PDF reading) |

Several skills fetch or read content from outside the repository and feed it directly into their own reasoning. `/graphify add <url>` ingests arbitrary web pages, YouTube audio via `yt-dlp`, Twitter/X posts, arXiv abstracts, PDFs, and images into `./raw`, and on success "automatically run[s] the `--update` pipeline" that hands them to entity extraction — no human sees the fetched text between retrieval and consumption. `library add` extracts claims from PDF text, and `verify-sources` Phase 5 reads source PDFs to adjudicate citation accuracy. Instructions embedded in any of that content are indistinguishable from the content itself once it reaches the model, and the failure is silent: a poisoned extraction produces a well-formed graph or a confident verification verdict. `library` and `verify-sources` are partially mitigated by HITL review gates (`library/SKILL.md:14`); `graphify`'s add path has none. Not otherwise mitigated.

A validator cannot close this one — unlike C-01, C-04, and C-05, the gap needs a design decision about isolation and review gating, not a detection script. See also C-12 (both concern the boundary between a skill and state it does not control).

---

### C-11: no mid-protocol abort or resume semantics outside autoresearch

| Field | Value |
|-------|-------|
| ID | C-11 |
| Tier | 3 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When a multi-phase skill is interrupted after it has begun writing — context exhaustion, a denied tool call, a user stop — inspect the artifact directory for partial state before re-invoking, because re-running from the start will append rather than resume. |
| Location | `register-risk/references/phases.md:154-172` (Phase 5 appends entries then updates counts), `rnd-dossier/SKILL.md:31-32` (`log` appends), `strategic-draft/SKILL.md:39` (Phase 6 consolidation), `writing-harness/SKILL.md:19-31` (creates 8 paths) |

Most skills in this repository write artifacts incrementally across phases rather than atomically at the end. `register-risk` Phase 5 writes entries and only then reconciles header counts, so an abort between the two leaves a register whose declared totals disagree with its contents. `strategic-draft` Phase 6 synchronises four artifacts in sequence. `rnd-dossier log` appends to the experiment log and then updates `00_README`. None of these defines what a resumed invocation should do with half-written state, and re-invocation generally re-executes from Phase 1. `autoresearch` is the sole exception, with an explicit resume contract — the ledger persists on disk and the branch in git, so a re-invocation reads both and continues (`autoresearch/references/karpathy-pattern.md:95`). The cost is duplicated or orphaned artifact state that a later reader cannot distinguish from intentional content.

See also C-14 (a partial write that drops or duplicates an ID is the silent-corruption case of this concern).

---

### C-12: no concurrency guard on shared artifacts

| Field | Value |
|-------|-------|
| ID | C-12 |
| Tier | 3 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When two Claude sessions are open against the same repository — a common pattern when one is drafting and one is reviewing — confirm they are not both invoking a skill that writes the same artifact before letting the second proceed. |
| Location | `reports/technical_risk_register.md` (this file), `_dev_materials/<slug>/` (writing harness artifacts), `reports/<date>_<name>_dossier/07_experiment_log` |

Every artifact this repository's skills manage is read-modify-written with no lock, no compare-and-swap, and no detection of concurrent modification. Two sessions running `/register-risk` against this register would each read the current entry set, each compute the next free `C-xx`, and each write — the second silently overwriting the first, or assigning a duplicate ID. The same applies to `/strategic-draft` and `/review-harness` on one `_dev_materials/<slug>/` harness, and to `/rnd-dossier log` on one experiment log. The concern is sharpened by the fact that the author has already solved this problem elsewhere: `thingit` implements a full turn-taking protocol — a `baton.md` program counter, a stop-if-not-your-seat rule, one commit per turn, and a 16-check validator (`thingit/SKILL.md:110-121`) — but it governs cross-repo deliberation in `views_platform/þingit/` and protects nothing in this repository. Not mitigated.

Needs a design decision rather than a detection script. See also C-10 (both concern state the skill does not exclusively control) and C-11 (an interrupted write and a concurrent write produce the same corrupt end state).

---

### C-13: no declared skill version or changelog

| Field | Value |
|-------|-------|
| ID | C-13 |
| Tier | 4 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When someone uploads a skill folder to Claude.ai per `README.md:94` and later needs to know which revision is deployed, or reports that a skill "used to work better," check what identifies the running version — nothing in the folder does. |
| Location | `graphify/.graphify_version` (only version marker in the repo; tracks the external `graphifyy` package, not the skill), all 24 `SKILL.md` frontmatter blocks (no `version:` field), repository root (no CHANGELOG) |

No skill declares a version. The single version marker in the repository, `graphify/.graphify_version`, pins the external `graphifyy` package rather than the skill that calls it, and nothing compares it against what is installed (see C-02). There is no changelog, so a behavioural regression introduced by a `SKILL.md` edit cannot be attributed to a revision without reading git history. This sits at Tier 4 rather than Tier 3 because git already provides both history and rollback for anyone working in the repository, which covers the primary use case. The residual exposure is narrow: skill folders uploaded individually via Claude.ai Settings — an installation path `README.md:94` explicitly offers — travel without git, and carry nothing that identifies which revision they are.

Detectable and partly closable by the C-03 validator (a frontmatter `version:` field check). See also C-02 (version drift between a skill and the package it drives).

---

### C-14: artifact-integrity invariants are prose-only and fail silently

| Field | Value |
|-------|-------|
| ID | C-14 |
| Tier | 3 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When a skill assigns a new artifact ID — `/register-risk` Phase 5, `/strategic-draft` creating a `D-NN` or `A-NNNN` — verify the ID has never been used in that scope, including by entries since resolved or removed, because nothing else will. |
| Location | `writing-harness/SKILL.md:74` (ID permanence rule), `register-risk/references/schema.md:52` (same rule for `C-xx`/`D-xx`), `register-risk/SKILL.md:17` (header-count maintenance), `reports/technical_risk_register.md` (this file) |

The artifacts these skills manage carry integrity invariants stated in prose and enforced by nothing. `writing-harness/SKILL.md:74` requires that "All IDs are permanent, never reused. Gaps are expected and informative," and `register-risk/references/schema.md:52` restates it for this register — but no mechanism prevents a reused ID, and a reused ID is undetectable by inspection: a second `D-03` looks exactly as valid as the first, while every cross-reference pointing at `D-03` silently becomes ambiguous. The same class covers header counts maintained by hand (`register-risk/SKILL.md:17`) and any edit that drops an entry while leaving the declared totals intact. The failure mode is corruption of the governance record itself, which is the artifact these skills exist to protect. Currently mitigated only by the reviewer's attention during `/review-rr triage`, which does check ID sequencing and header accuracy — but only when someone remembers to run it.

Detectable by the C-03 validator (ID uniqueness and count reconciliation are mechanical checks). See also C-11 (an interrupted write is one way an ID or count is dropped).

---

## Disagreements

### D-01: skills compose through filesystem artifacts rather than programmatic APIs

| Field | Value |
|-------|-------|
| ID | D-01 |
| Source | repo-assimilation (2026-08-15) |
| Perspectives | **Composition-by-artifact (prevailing)** — `README.md:81` commits the collection to filesystem composition: each skill owns a concern and others consume its output through files. This is what lets any skill folder be uploaded to Claude.ai on its own (`README.md:94`), keeps the collection free of an import graph, and means no skill can break another by changing an internal. **Contract-drift objection** — the six seam contracts in `README.md:83-90` are restated inside both participating skills, so each contract exists in three uncoordinated copies. A one-sided edit leaves two stale descriptions and no mechanism detects it, because no validator can check that three natural-language descriptions of ownership still agree (registered as C-06) |
| Resolution | **Accepted trade-off.** Composition-by-artifact stands — independent installability is a load-bearing property of the collection, and an import graph would forfeit it to solve a documentation problem. The drift cost is accepted and mitigated by convention rather than eliminated: the `README.md` seams table is the single normative source, and the skill-side copies should reference it rather than restate it. **Revisit trigger:** the first seam drift that causes an actual misroute — a skill delegating to the wrong owner because its local copy of the contract was stale |

---

## Resolved Concerns

### C-01: base_docs template path points at a renumbered vault directory — RESOLVED

| Field | Value |
|-------|-------|
| ID | C-01 |
| Resolved | 2026-08-17 |
| Resolution | Path corrected to `~/brain/5_system/templates/base_docs` in both `init-base-docs/references/phases.md:5` and `adopt-base-docs/references/phases.md:5`. Canonical copy confirmed by checking all six artifacts the skills require (`ADRs/`, `CICs/`, `contributor_protocols/`, `standards/`, `INSTANTIATION_CHECKLIST.md`, `validate_docs.sh`) — all present in `5_system`, only the first two in the `claude_learning` copy, which is now named in the text as a known-incomplete decoy. Recurrence is caught by `scripts/validate_skills.py` (external-paths check), mutation-tested — but **that check cannot run in CI**, because it resolves `~/brain/...` which exists only on this machine. It is enforced by the pre-push hook (`scripts/install-hooks.sh`), which must be installed per clone. On a machine without the hook, nothing catches this. |

---

### C-03: no validation infrastructure of any kind — RESOLVED

| Field | Value |
|-------|-------|
| ID | C-03 |
| Resolved | 2026-08-17 |
| Resolution | `scripts/validate_skills.py` checks all five invariants this entry named: frontmatter validity, `references/` path resolution, cross-skill name existence, external path availability, README-to-filesystem consistency. Wired to `.github/workflows/validate.yml`; external-paths is reported but not enforced in CI because `~/brain/...` exists only on the author's machine. Mutation-tested. C-01's path is caught. C-04 is caught in its backticked, table-row and slash-command forms — **not** in bare running prose, which was two of its four historical sites; earlier attempts at prose detection false-positived on ordinary hyphenated adjectives and were withdrawn rather than grown into a filter list nobody trusts. First run found three live defects: two unqualified `references/schema.md` paths and three installed skills missing from the README. |

---

### C-04: three referenced skills do not exist — RESOLVED

| Field | Value |
|-------|-------|
| ID | C-04 |
| Resolved | 2026-08-16 |
| Resolution | All seven dangling references removed: `clean-architecture-review` from `register-risk/SKILL.md:22`, `references/schema.md` (Source table row) and `references/phases.md` (×2); `test-generation` from `test-review/SKILL.md` frontmatter and body; `hello-world` and its Utility table from `README.md`. The register's own Conventions line was carrying the same stale Source value and was corrected too. Verified: zero references remain outside C-04's own entry. |

---

### C-07: a complete skill and an edited skill are outside version control — RESOLVED

| Field | Value |
|-------|-------|
| ID | C-07 |
| Resolved | 2026-08-15 |
| Resolution | Commit `156d0c4` brought both paths under version control: the previously untracked `thingit/` skill (128 lines) and the unstaged `library/SKILL.md` modification (ADR-019 PDF naming convention plus the `add_confirm_metadata` atomic rename workflow), alongside the register and ADR-001. The `library/SKILL.md` diff was read before staging rather than committed unreviewed. |

---

## Register Conventions

- **ID format:** `C-xx` for concerns, `D-xx` for disagreements. IDs are permanent — gaps in numbering indicate merged or resolved entries
- **Sources:** `repo-assimilation`, `expert-review`, `test-review`, `falsification-audit`, `pr-review`, `tech-debt-audit`, `incident`, `manual`
- **Resolution:** Move to "Resolved Concerns" with resolution date and summary when addressed
- **Header counts:** Manually maintained — update whenever a concern is added or resolved
- **Governed by:** ADR-001
