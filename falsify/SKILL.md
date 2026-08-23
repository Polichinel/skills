---
name: falsify
description: Runs a Popperian falsification audit. Two modes. CLAIM mode attacks a stated claim about software behavior with structured probes, then generates failing test stubs. GUARD mode attacks an existing test or assertion by mutating production code to find changes that leave the guard green — it answers "would this guard actually catch anything". Use when user says "falsify this", "falsification audit", "prove this wrong", "try to break", "red team this claim", or for guard mode "falsify guard", "is this test real", "would this guard catch anything", "mutation test this", "check my guards". Do NOT use for code review (use expert-code-review), for whole-suite test assessment (use test-review), for diff review (use review-diff), or for writing tests from scratch.
---

# Falsification Audit

## Modes

| mode | input | question | procedure |
|---|---|---|---|
| **Claim** (default) | a falsifiable claim about behavior | *Can I prove this does not work?* | phases 1–10 below |
| **Guard** | an existing test, assertion, or validator | *What could I change in the code that would leave this guard green?* | `references/guard_mutations.md` |

Guard mode is invoked as **`/falsify guard`** with no argument — it defaults to every guard added or
changed on the current branch, the same scope `/review-diff` takes. A path, glob, or commit-ish
narrows it. It runs automatically inside `ship-it` Step 5.5, so in normal use it is not invoked by
hand at all. It exists because the failure it
detects is systemic here: guards that cannot fire were recorded in **9 of 18 repositories**
(`reports/measurements/2026-08-23_agent_failure_pattern_prevalence.md`), and the mechanism is that an
author cannot test what they did not imagine. **Guard mode must therefore run in a subagent with a
clean context** — the auditor may not be the author, and may not read the reasoning that produced the
guard. See `references/guard_mutations.md`, which is normative for that mode.

## Important

Follow these rules strictly.

- Do not execute probes before the user confirms the probe list. Present probes first, then STOP and wait.
- Do not modify any existing files. The only file this skill creates is the failing test file. (Guard mode is the sole exception: it applies mutations to production code and reverts every one — see its rules below.)
- Design all probes before executing any. Commit to what would falsify before looking.
- Do not dismiss a falsifying observation as an edge case. If it falsifies, it falsifies. Consult `references/epistemology.md` on ad hoc rescue.
- Every hard or soft falsification must produce a failing test stub in the output file.
- Minimum viable audit: 3-5 probes from at least 3 different categories.
- If the claim is not falsifiable as stated, stop and help the user reformulate it before proceeding.

**Guard mode only:**

- The auditor may not be the author. Run in a subagent with a clean context, or mark every verdict `UNVERIFIED (not independent)`.
- Do not read the register entry, ADR, or commit message explaining a guard before designing mutations. That is the author's model of failure, and it is the thing under test.
- Every mutation is applied to production code and the guard is executed. Reasoning about whether a mutation would be caught is not a result — record it `UNRUN`, never as caught.
- Revert every mutation and confirm a clean tree before reporting. Guard mode is the only mode that edits production code, and it must leave nothing behind.

## Purpose

After tests pass, linting passes, and code review says clean, this skill asks: "Can I prove it does not work?" It takes a falsifiable claim about software behavior, designs structured probes to attack it, executes them, and produces a findings report plus failing test stubs for anything that breaks.

The epistemological basis is Popper's falsificationism: a claim gains credibility not by passing tests but by surviving serious attempts to refute it. Consult `references/epistemology.md` for the reasoning framework and anti-patterns.

## Procedure — claim mode

Execute these 10 phases sequentially. For detailed instructions on each phase, consult `references/phases.md`. For probe category definitions and selection heuristics, consult `references/probes.md`. **For guard mode, follow `references/guard_mutations.md` instead — it replaces phases 1–8 with G1–G7 and keeps phases 9 and 10.**

1. **Parse Claim** -- Extract a precise falsifiable hypothesis from the user's claim
2. **Scan Context** -- Locate governance docs (CICs, ADRs, ARCHITECTURE.md), test suites, and source code relevant to the claim
3. **Derive Probes** -- Auto-generate probes from governance docs and standard categories
4. **Present Probes** -- Show the probe list to the user. **STOP** and wait for confirmation.
5. **Predict Outcomes** -- For each probe, record the expected outcome before execution
6. **Execute Probes** -- Run probes as read-only analysis and targeted script execution
7. **Classify Findings** -- Assign severity: hard falsification, soft falsification, or observation
8. **Generate Test Stubs** -- Write failing test file for all hard and soft falsifications
9. **Pattern Analysis** -- Look across findings for systemic issues and recurring bug classes
10. **Report** -- Structured output with all results and verdict

## Required Output Structure — guard mode

1. Independence statement (was the auditor the author? was the context clean?) — first, because every other line depends on it
2. Guards enumerated (count, and how they were found)
3. Mutation Plan (table: guard, category M1–M7, mutation, predicted caught/survives)
4. Mutation Results (per mutation: applied, guard run, caught / SURVIVED / UNRUN, evidence)
5. Verdict per guard (DECORATIVE / WEAK / HOLDS / UNVERIFIED), survivors named individually
6. Tree state (confirmation that every mutation was reverted)
7. Pattern Analysis and Verdict (phases 9–10, unchanged)

## Required Output Structure — claim mode

1. Claim and Hypothesis (original claim, reformulated hypothesis, scope)
2. Probe Plan (table: ID, category, description, risky prediction)
3. Probe Results (per probe: ID, category, prediction, actual outcome, verdict, evidence)
4. Failing Tests (file path, count of test stubs, listing of test function names)
5. Pattern Analysis (cross-cutting themes, systemic issues, recurring bug classes)
6. Verdict (FALSIFIED / CONTESTED / SURVIVED with rationale)

## Risk Register Integration

Format hard and soft falsifications in register-compatible format (ID, tier, trigger, source, location, narrative). Do not append directly to the register — output the findings and let the user invoke `register-risk` to handle deduplication, tier validation, and registration. The failing test stubs and register entries serve complementary purposes: tests enforce the fix, register entries track the risk.

## Severity Levels

- **Hard falsification:** The system produces a wrong answer silently, violates a documented contract (CIC, ADR, docstring), documentation lies about behavior, or the artifact omits a topic that its field requires and a reviewer would reject for. The claim is disproven. Must fix before the claim can be reasserted.
- **Soft falsification:** Unexpected behavior that is not dangerous but undermines confidence. Missing validation, undocumented edge case, surprising default. Should fix.
- **Observation:** Behavior is technically correct but surprising or poorly documented. Worth noting. Does not falsify the claim.

## Verdict

- **FALSIFIED:** One or more hard falsifications found. The claim is disproven. Report count of hard and soft findings.
- **CONTESTED:** No hard falsifications, but soft falsifications weaken the claim. Report count of soft findings.
- **SURVIVED:** All probes passed. The claim has survived this audit. Note: survived means withstood this specific set of probes, not proven true. Confidence is proportional to probe severity and diversity.

## Performance Notes

- The intellectual honesty of this skill is its value. Do not design probes you expect to pass.
- The risky prediction step (Phase 5) is mandatory. It distinguishes genuine testing from post-hoc rationalization.
- Do not retroactively add probes to claim you predicted a finding you discovered during execution. Record unexpected discoveries as bonus observations.
- Quality of probes matters more than quantity. Five well-targeted probes beat twenty shallow ones.
- When a claim spans multiple modules, ensure probes cover integration boundaries, not just individual modules.
- For research artifacts and novel methods, include at least one Category H (Adequacy) probe. The most important finding in a falsification campaign is often an omission, not an error. See `references/epistemology.md` on claim scope.
- When the user provides only narrow, artifact-internal claims across multiple rounds, suggest a broader adequacy claim. Narrow claims cannot detect omissions — see the two-pass discipline in `references/epistemology.md`.
- Consult `references/epistemology.md` if tempted to weaken a finding or design only probes you know will pass.
