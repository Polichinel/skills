# Test Review: Detailed Phase Instructions

## Phase 1 -- Locate Prerequisites

### Find repo-assimilation output (required)
Check if repo-assimilation has been run in this session or a previous session. Look for assimilation output provided by the user or available from a prior conversation.

If no assimilation output is available, **STOP** and tell the user:

> "This skill requires repo-assimilation output as a prerequisite. The assimilation provides the structural understanding needed to evaluate test coverage in context. Please run 'assimilate this repo' first, then re-invoke test-review."

Extract from assimilation output:
- Repository structure and module boundaries
- Core classes and their roles
- Dependency graph (which components interact)
- Known technical risks and fragilities

### Find test directories
Search for test files using common patterns:
- `tests/`, `test/`, `spec/`
- Files matching `test_*.py`, `*_test.py`, `*_spec.py`
- Files matching `test_*.js`, `*.test.js`, `*.spec.js`
- Framework-specific locations (pytest, unittest, jest, mocha, etc.)

Count total test files and test functions/methods.

### Find CICs (required)
Locate the `CICs/` directory, typically under `docs/`. Read `CICs/README.md` for the list of active contracts.

If no CICs exist, **STOP** and tell the user:

> "This skill requires CIC (Class Intent Contract) documentation as a prerequisite. CICs define what each class promises, which defines what tests should verify. Please run 'adopt base docs' first, then re-invoke test-review."

### Find ADR-005
Locate ADR-005 (Testing as Mandatory Critical Infrastructure) for the red/beige/green taxonomy definitions. If ADR-005 does not exist or is deferred, use the standard definitions:
- **Red:** Adversarial tests -- attack surface, boundary abuse, malicious input, failure injection
- **Beige:** Realistic neutral usage -- decision-support safety, interaction correctness, operational scenarios
- **Green:** Correctness and resilience -- invariants, transformations, CI backbone, happy path + edge cases

### Inventory
Report:
- Assimilation output: available (summary of key structural findings)
- Number of test files found and their locations
- Number of CICs found and their classes
- ADR-005 status (present/absent/deferred)
- Test framework(s) detected

---

## Phase 2 -- Run Test Suite

Execute the full test suite to establish ground truth before any analysis.

### Detect and run
1. Identify the test runner from the project (pytest, unittest, jest, mocha, cargo test, go test, etc.)
2. Run the full suite with verbose output to capture individual test results
3. If a coverage tool is available (pytest-cov, coverage.py, istanbul, etc.), run with coverage enabled

### Capture results
Record:
- **Total tests:** count of all test functions/methods
- **Passed:** count and list
- **Failed:** count and list with failure messages
- **Errors:** count and list with error messages
- **Skipped:** count and list with skip reasons
- **Duration:** total wall-clock time

### Baseline assessment
- If any tests fail: note these as the current state. Do NOT attempt to fix them. Failing tests are important context -- they may indicate known issues, flaky tests, or active regressions.
- If tests cannot run at all (missing dependencies, broken imports): report the blocker and proceed with static analysis only. Note this limitation prominently in the report.
- If coverage data is available: record line/branch coverage percentages per module.

### Output

| Metric | Value |
|--------|-------|
| Total tests | N |
| Passed | N |
| Failed | N |
| Errors | N |
| Skipped | N |
| Duration | Xs |
| Coverage | N% (if available) |

**Failing tests:**
| Test | File | Failure Reason |
|------|------|----------------|

**Skipped tests:**
| Test | File | Skip Reason |
|------|------|-------------|

---

## Phase 3 -- Coverage Mapping

### Class-level mapping
For each class that has a CIC:
1. Identify the source file and class
2. Search for test files that import or reference this class
3. List which public methods have at least one test
4. List which public methods have zero tests

### Module-level mapping
For each top-level module/package:
1. Count source files vs test files
2. Identify modules with no test coverage at all
3. Identify test files that don't correspond to any source file (orphaned tests)

### Output

| Class (CIC) | Source File | Test File(s) | Methods Tested | Methods Untested | Coverage |
|-------------|------------|--------------|---------------|-----------------|----------|

| Module | Source Files | Test Files | Ratio | Notes |
|--------|------------|------------|-------|-------|

---

## Phase 4 -- Category Assessment

### Classify existing tests
Read each test file and classify individual test functions into red/beige/green:

**Red team indicators:**
- Tests with names containing: `invalid`, `malicious`, `attack`, `abuse`, `inject`, `overflow`, `corrupt`, `unauthorized`
- Tests that pass deliberately bad input
- Tests that verify exceptions/errors are raised
- Tests that verify security boundaries
- Tests for timeout, resource exhaustion, or denial conditions

**Beige team indicators:**
- Tests with realistic multi-step scenarios
- Tests that combine multiple components in realistic workflows
- Tests for decision-support correctness (does the output support good decisions?)
- Tests for operational scenarios (startup, shutdown, configuration change)
- Tests for interaction patterns between components
- Tests that verify monitoring/logging outputs

**Green team indicators:**
- Tests for correct output given valid input
- Tests for state transitions and invariants
- Tests for data transformation correctness
- Tests for boundary values (min, max, empty, one)
- Tests for idempotency and determinism
- Standard unit tests and integration tests

### Distribution analysis
Calculate per-module and overall:
- Count of red / beige / green tests
- Percentage distribution
- Flag modules with zero red or zero beige coverage (common gaps)

### Output

| Module | Red | Beige | Green | Total | Balance Assessment |
|--------|-----|-------|-------|-------|--------------------|

---

## Phase 5 -- Expert Perspectives

Apply each of the 5 expert perspectives independently. For detailed evaluation criteria, consult `references/experts.md`.

### Process per expert:
1. Read through all test files with the expert's specific lens
2. Read through CICs for context on what behavior matters
3. Identify strengths (what the tests do well from this perspective)
4. Identify weaknesses (what the tests miss from this perspective)
5. Provide specific, actionable recommendations

### Expert order:
1. **Kent Beck** (TDD, cross-cutting) -- test design quality and feedback loops
2. **Michael Feathers** (Safe Change, cross-cutting) -- change safety and characterization gaps
3. **Michael T. Nygard** (Reliability, red team) -- failure mode and resilience coverage
4. **Martin Kleppmann** (Correctness, green team) -- data integrity and invariant coverage
5. **Nancy Leveson** (System Safety, beige team) -- interaction safety and STAMP analysis

### Output per expert:

**[Expert Name] -- [Domain]**

Strengths:
- [Specific strength with file/test references]

Weaknesses:
- [Specific weakness with file/class references]

Recommendations:
- [Actionable recommendation with category (red/beige/green) and severity]

---

## Phase 6 -- Contract Alignment

For each CIC, check whether its declared guarantees and failure modes are tested.

### Per-CIC checks:

**Section 3 -- Responsibilities and Guarantees:**
- List each guarantee statement
- For each guarantee: find test(s) that verify it, or mark as untested
- Assess test strength: does the test actually verify the guarantee, or just touch the method?

**Section 6 -- Failure Modes and Loudness:**
- List each documented failure mode
- For each failure mode: find test(s) that trigger it, or mark as untested
- Check that fail-loud behavior is verified (assert on exception type, not just "doesn't crash")

**Section 10 -- Test Alignment:**
- Read the CIC's own test alignment section
- Check if referenced test files still exist
- Check if the CIC's assessment of coverage is still accurate
- Flag discrepancies between what the CIC claims and what actually exists

**Section 12 -- Known Deviations (if present):**
- Are any deviations testable? If so, are they tested?
- Have any previously-documented deviations been resolved (tests added)?

### Output per CIC:

| CIC | Guarantee | Tested? | Test File | Strength | Category |
|-----|-----------|---------|-----------|----------|----------|

| CIC | Failure Mode | Tested? | Test File | Strength | Category |
|-----|-------------|---------|-----------|----------|----------|

---

## Phase 7 -- Report

Compile all findings into the Required Output Structure from SKILL.md (7 sections).

### 1. Test Suite Baseline
From Phase 2. Pass/fail/error/skip counts, failing tests listed, coverage if available.

### 2. Coverage Map
From Phase 3. Include both class-level and module-level tables.

### 3. Category Distribution
From Phase 4. Include per-module breakdown and overall balance assessment.

### 4. Expert Reviews
From Phase 5. Present all 5 perspectives independently. Each should have strengths, weaknesses, and recommendations with specific file references.

### 5. Contract Alignment
From Phase 6. Per-CIC guarantee and failure mode coverage tables.

### 6. Gap Analysis
Synthesize across all phases. Prioritized list:

| Priority | Severity | Category | Class/Module | Gap Description | Recommended Test |
|----------|----------|----------|-------------|-----------------|-----------------|
| 1 | Critical | Red | ... | ... | ... |
| 2 | Critical | Green | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

Order by: severity (Critical > High > Medium > Low), then by category (Red > Beige > Green for equal severity -- failure coverage is harder to add later).

### 7. Test Health Summary

Provide an overall assessment:
- Total tests audited
- Category distribution (red/beige/green percentages)
- Contract coverage (% of CIC guarantees tested)
- Failure mode coverage (% of CIC failure modes tested)
- Overall health rating: **robust** / **adequate** / **gaps present** / **significant gaps** / **critical gaps**
- Top 3 recommended actions (specific, actionable, with category labels)
- Which expert perspective revealed the most gaps (indicates systemic blind spot)
