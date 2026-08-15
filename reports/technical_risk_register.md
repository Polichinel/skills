# Technical Risk Register

| Register Info     | Details                              |
|-------------------|--------------------------------------|
| Project           | claude-code-skills                   |
| Owner             | Polichinl (simmaa@prio.org)          |
| Last Updated      | 2026-08-15                           |
| Total Concerns    | 14                                   |
| Open Concerns     | 14                                   |
| Resolved Concerns | 0                                    |

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

### C-01: base_docs template path points at a renumbered vault directory

| Field | Value |
|-------|-------|
| ID | C-01 |
| Tier | 2 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When someone invokes `/init-base-docs` or `/adopt-base-docs` on any project, Phase 1 "Locate Base Docs" fails — verify the path at `references/phases.md:5` resolves, and pick between the two candidate template copies, before running. |
| Location | `init-base-docs/references/phases.md:5`, `adopt-base-docs/references/phases.md:5` |

Both skills instruct "Check `~/brain/8_system/templates/base_docs` for the template directory." `/home/simon/brain/8_system/` does not exist; a filesystem search locates the templates at `/home/simon/brain/5_system/templates/base_docs`, with a second copy at `/home/simon/Documents/scripts/claude_learning/base_docs`. The brain vault was renumbered without updating the two skills that depend on it. Phase 1 of both skills is entirely "Locate Base Docs — Find and validate the base_docs template directory," so the failure is loud rather than silent — but no fallback path is specified and there are now two candidate sources with no stated precedence, so a recovering operator must guess which is canonical. Both governance-bootstrap skills are non-functional as written. Not currently mitigated; no skill validates its external paths before use except `thingit`. Tier rationale: Tier 2 rests on near-certain likelihood rather than on severity — the failure is loud and the fix is a one-line path edit, which makes this the least severe of the three Tier 2 entries. C-02 and C-08 sit at the same tier on the opposite basis: lower likelihood, silent failure. Confirmed at Tier 2 during review-rr strategic review (2026-08-15).

See also C-03 (shared root cause: no mechanical validation of external paths) and C-05 (same class of external-path assumption).

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

### C-03: no validation infrastructure of any kind

| Field | Value |
|-------|-------|
| ID | C-03 |
| Tier | 3 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When someone renames a skill directory, renames a `references/*.md` file, or changes an external path in a `SKILL.md`, manually re-check that every reference path, cross-skill name, and external path still resolves — no script does this. |
| Location | Repository root — absence of `.github/`, of any `.sh`/`.py`/`.yml`/`.toml` file, of any test |

The repository contains no test, no CI workflow, and no validation script; the only executable artifact referenced anywhere (`scripts/validate_thing.sh`) lives outside the repo in `views_platform/þingit/`. Five invariants are cheaply and mechanically verifiable and none is checked: frontmatter validity across all 24 `SKILL.md` files, `references/` path resolution across 40 files, cross-skill name existence, external path availability, and README-to-filesystem consistency. Three of those five are already violated (C-01, C-04) and survived nine commits undetected. This is the root-cause entry for C-01, C-04, and C-05, which are its symptoms. It is also a self-application gap: `README.md:112` asserts "Testing is mandatory critical infrastructure," and `ship-it/SKILL.md` enforces `ruff` and `pytest` gates on target repositories while this repository has neither. Partially mitigated only within `thingit`, whose external 16-check validator demonstrates the pattern the rest of the repo lacks. Tier rationale: held at Tier 3 rather than raised to Tier 2 to avoid double-counting — the severity of this omission is already carried by the symptom entries C-01, C-04, and C-05, each tiered on its own consequence. Tier 3 reflects the residual risk of future undetected drift, not the sum of what it has already caused. Confirmed at Tier 3 during review-rr strategic review (2026-08-15).

Root cause of C-01, C-04, and C-05. See also C-07 (uncommitted state would also be caught by a repository-state check).

---

### C-04: three referenced skills do not exist

| Field | Value |
|-------|-------|
| ID | C-04 |
| Tier | 3 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When someone follows a documented "use X instead" delegation to `clean-architecture-review`, `test-generation`, or `hello-world`, or writes a register entry using the `clean-architecture-review` Source value from `register-risk/references/schema.md:79`, the target skill is not installed. |
| Location | `register-risk/SKILL.md:22`, `register-risk/references/schema.md:79`, `register-risk/references/phases.md:71,83`, `test-review/SKILL.md:3,24`, `README.md:77` |

Three skill names are referenced as though installed and have no corresponding directory. `clean-architecture-review` appears four times across `register-risk`, including in the schema table of valid `Source` values, so this register's own vocabulary admits a source no installed skill can produce. `test-generation` appears in `test-review`'s **frontmatter description** — the text the Claude Code harness uses for dispatch — which is the most load-bearing position an incorrect name can occupy. `hello-world` is advertised in the README's public skill inventory. Because routing between skills is prose-only and never validated (see C-06), a dangling name is indistinguishable from a live one until invocation fails. Not currently mitigated.

Symptom of C-03 (no cross-skill name validation). See also C-06 (same line, `register-risk/SKILL.md:22`, seam-drift aspect).

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

### C-07: a complete skill and an edited skill are outside version control

| Field | Value |
|-------|-------|
| ID | C-07 |
| Tier | 3 |
| Source | repo-assimilation (2026-08-15) |
| Trigger | When someone runs `git clean -fd`, clones this repository fresh, or migrates to another machine, verify that `thingit/` and the `library/SKILL.md` modification were committed first — `/ship-it` Step 4's `git add -u` stages the latter but not the former. |
| Location | `thingit/` (untracked, 128 lines), `library/SKILL.md` (modified, unstaged) |

`git status` reports `?? thingit/` and ` M library/SKILL.md`. `thingit` is a complete and unusually rigorous skill implementing a cross-repo deliberation protocol backed by a 16-check external validator, and it is the only skill in the collection with zero inbound references from anything — including the README — which is consistent with it never having been integrated. The `library/SKILL.md` modification is likewise unreviewed and uncommitted. Loss is irreversible rather than merely inconvenient, which is what places this above Tier 4 despite its single-developer scope. Mitigated in principle by `ship-it/SKILL.md` Step 3, which is designed to stop on exactly this condition ("If untracked files exist that are not in .gitignore: **STOP**"), but that gate has not been run against this working tree.

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

(No resolved concerns yet.)

---

## Register Conventions

- **ID format:** `C-xx` for concerns, `D-xx` for disagreements. IDs are permanent — gaps in numbering indicate merged or resolved entries
- **Sources:** `repo-assimilation`, `expert-review`, `test-review`, `falsification-audit`, `clean-architecture-review`, `pr-review`, `tech-debt-audit`, `incident`, `manual`
- **Resolution:** Move to "Resolved Concerns" with resolution date and summary when addressed
- **Header counts:** Manually maintained — update whenever a concern is added or resolved
- **Governed by:** ADR-001
