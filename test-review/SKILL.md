---
name: test-review
description: Audits test coverage and quality from 5 expert perspectives (Beck, Feathers, Nygard, Kleppmann, Leveson) against CIC contracts and the red/beige/green test taxonomy. Use when user says "review the tests", "assess test coverage", "audit test quality", "test review", "are the tests good enough", or "check test alignment". Do NOT use for writing tests (use test-generation), for code review (use expert-code-review), or for documentation review (use review-base-docs).
---

# Test Review

## Important

Follow these rules strictly.

- Do not modify any test files. This skill audits and reports only.
- Do not modify any source files. Document gaps, do not fix them.
- Require repo-assimilation output as a prerequisite. If unavailable, stop and tell the user to run repo-assimilation first.
- Require CICs as a prerequisite. If no CICs exist, stop and tell the user to run adopt-base-docs first.
- Run the full test suite before any analysis. The actual pass/fail/error results are the ground truth for everything that follows.
- Evaluate each expert perspective independently. Do not merge perspectives.
- Ground every finding in specific test files, source files, and CIC references.
- Classify findings using the red/beige/green taxonomy from ADR-005.
- Distinguish between coverage gaps (missing tests) and quality gaps (tests exist but are weak).

## Critical Constraint

This skill is read-only. It produces an assessment report. It does not create, modify, or delete any files. All proposed tests are recommendations for the user to act on (or to feed into the test-generation skill).

## Purpose

Assess test coverage and quality against architectural contracts (CICs) and the red/beige/green test taxonomy (ADR-005), providing 5 independent expert perspectives on where tests are missing, weak, or misaligned with declared behavior.

## Procedure

Execute these 7 phases sequentially. For detailed instructions, consult `references/phases.md`. For expert evaluation criteria, consult `references/experts.md`.

1. **Locate Prerequisites** -- Find test directories, CICs, ADR-005, and repo-assimilation output
2. **Run Test Suite** -- Execute the full test suite and capture pass/fail/error/skip results
3. **Coverage Mapping** -- Map test coverage across classes and modules
4. **Category Assessment** -- Classify existing tests into red/beige/green
5. **Expert Perspectives** -- Apply 5 expert lenses independently
6. **Contract Alignment** -- Check tests against CIC guarantees
7. **Report** -- Structured output with findings and recommendations

## Required Output Structure

1. Test Suite Baseline (pass/fail/error/skip counts, failures listed)
2. Coverage Map (classes/modules with and without tests)
3. Category Distribution (red/beige/green balance per module)
4. Expert Reviews (5 independent assessments, each with strengths/weaknesses/recommendations)
5. Contract Alignment (per-CIC: which guarantees are tested, which are not)
6. Gap Analysis (prioritized list of missing tests by severity and category)
7. Test Health Summary (overall assessment, category balance, top recommendations)

## Severity Levels

- **Critical:** CIC guarantee with zero test coverage; fail-loud behavior untested
- **High:** Entire red or beige category missing for a critical class; test verifies implementation not contract
- **Medium:** Coverage exists but shallow (happy path only); stale tests for refactored code
- **Low:** Test naming/organization inconsistencies; missing category markers in docstrings

## Performance Notes

- Complete all 5 expert perspectives before synthesizing. Do not shortcut.
- CIC section 3 (Responsibilities and Guarantees) is the primary source of what should be tested.
- CIC section 6 (Failure Modes) maps directly to red team test requirements.
- CIC section 10 (Test Alignment) may already list expected coverage -- check if it's accurate.
- Quality over speed. A thorough assessment is more valuable than a quick one.
