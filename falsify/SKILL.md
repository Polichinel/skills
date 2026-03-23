---
name: falsify
description: Runs a Popperian falsification audit against a stated claim about software behavior. Designs and executes structured probes to try to prove the claim wrong, then generates failing test stubs for anything that breaks. Use when user says "falsify this", "falsification audit", "can you prove it doesn't work", "prove this wrong", "try to break", "Popperian audit", "red team this claim", or "audit this claim". Do NOT use for code review (use expert-code-review), for test assessment (use test-review), for diff review (use review-diff), or for writing tests from scratch.
---

# Falsification Audit

## Important

Follow these rules strictly.

- Do not execute probes before the user confirms the probe list. Present probes first, then STOP and wait.
- Do not modify any existing files. The only file this skill creates is the failing test file.
- Design all probes before executing any. Commit to what would falsify before looking.
- Do not dismiss a falsifying observation as an edge case. If it falsifies, it falsifies. Consult `references/epistemology.md` on ad hoc rescue.
- Every hard or soft falsification must produce a failing test stub in the output file.
- Minimum viable audit: 3-5 probes from at least 3 different categories.
- If the claim is not falsifiable as stated, stop and help the user reformulate it before proceeding.

## Purpose

After tests pass, linting passes, and code review says clean, this skill asks: "Can I prove it does not work?" It takes a falsifiable claim about software behavior, designs structured probes to attack it, executes them, and produces a findings report plus failing test stubs for anything that breaks.

The epistemological basis is Popper's falsificationism: a claim gains credibility not by passing tests but by surviving serious attempts to refute it. Consult `references/epistemology.md` for the reasoning framework and anti-patterns.

## Procedure

Execute these 10 phases sequentially. For detailed instructions on each phase, consult `references/phases.md`. For probe category definitions and selection heuristics, consult `references/probes.md`.

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

## Required Output Structure

1. Claim and Hypothesis (original claim, reformulated hypothesis, scope)
2. Probe Plan (table: ID, category, description, risky prediction)
3. Probe Results (per probe: ID, category, prediction, actual outcome, verdict, evidence)
4. Failing Tests (file path, count of test stubs, listing of test function names)
5. Pattern Analysis (cross-cutting themes, systemic issues, recurring bug classes)
6. Verdict (FALSIFIED / CONTESTED / SURVIVED with rationale)

## Severity Levels

- **Hard falsification:** The system produces a wrong answer silently, violates a documented contract (CIC, ADR, docstring), or documentation lies about behavior. The claim is disproven. Must fix before the claim can be reasserted.
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
- Consult `references/epistemology.md` if tempted to weaken a finding or design only probes you know will pass.
