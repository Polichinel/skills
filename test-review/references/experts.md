# Test Review: Expert Perspectives

## Kent Beck -- Test-Driven Development (Cross-cutting)

Kent Beck evaluates whether tests serve as a reliable safety net for incremental change. His perspective cuts across all three categories.

### Evaluation Criteria

**Testability assessment:**
- Can each class be instantiated in isolation for testing?
- Are dependencies injectable or hard-wired?
- Do classes have clear seams for test doubles where needed?

**Test design quality:**
- Do tests verify behavior (what the class promises) or implementation (how it does it)?
- Are tests independent -- can any test run alone without relying on other tests' side effects?
- Are tests fast enough to run frequently during development?
- Do tests follow Arrange-Act-Assert structure with clear intent?

**Feedback loop:**
- How quickly does the full test suite run?
- Are there tests that are consistently slow, flaky, or skipped?
- Do test failures point directly to the problem or require debugging?

**Brittleness indicators:**
- Tests that break when internal refactoring occurs (coupled to implementation)
- Tests that use excessive mocking (testing the mock, not the code)
- Tests that assert on incidental details (exact log messages, internal state)

### Output Format

For each finding, state:
- What the test does well or poorly (specific file + test name)
- Whether it tests behavior or implementation
- Recommended change (if any)

---

## Michael Feathers -- Legacy Code & Safe Change (Cross-cutting)

Michael Feathers evaluates whether the test suite makes the codebase safe to change. His focus is on identifying code that is risky to modify because it lacks adequate test coverage.

### Evaluation Criteria

**Change safety assessment:**
- Which classes can be safely refactored today (adequate test coverage)?
- Which classes are risky to touch (no tests, or tests that don't cover key paths)?
- Are there "edit and pray" zones -- code regularly modified but never tested?

**Seam analysis:**
- Does the code have natural seams (interfaces, dependency injection) that enable testing?
- Where are the pinch points -- places where many paths converge that would be high-value test targets?
- Are there classes with hidden dependencies (global state, singletons, file system access) that make testing hard?

**Characterization test gaps:**
- Is existing behavior documented by tests (even if the behavior is imperfect)?
- Are there classes where the only specification is the code itself -- no tests describe what it does?
- Would a developer modifying this class know from the tests what behavior to preserve?

**Test infrastructure:**
- Are test fixtures and helpers available for common setup patterns?
- Is there a clear pattern for testing each architectural layer?
- Are integration boundaries (database, filesystem, network) properly isolated in tests?

### Output Format

For each class/module, state:
- Safety rating: Safe to change / Risky / Dangerous
- What tests exist (if any) and what they cover
- What characterization tests are missing
- Recommended seams to exploit for testing

---

## Michael T. Nygard -- Production Reliability (Red Team Alignment)

Nygard evaluates whether the test suite verifies that the system fails safely under adverse conditions. His perspective maps directly to red team tests.

### Evaluation Criteria

**Failure mode coverage:**
- For each CIC section 6 (Failure Modes): is there at least one test that triggers each documented failure?
- Are exceptions tested for correct type, message, and propagation?
- Is fail-loud behavior verified (system raises rather than silently continuing)?

**Resilience mechanism testing:**
- Timeouts: are timeout behaviors tested with both fast and slow scenarios?
- Retry logic: are retry limits, backoff, and exhaustion tested?
- Circuit breakers: are open/closed/half-open states tested?
- Graceful degradation: when a dependency fails, does the test verify degraded behavior?

**Cascading failure scenarios:**
- What happens when a downstream dependency is unavailable?
- What happens when a dependency returns corrupt or unexpected data?
- Are there tests for partial failure (some records succeed, some fail)?

**Resource exhaustion:**
- Are there tests for behavior under memory pressure, full disks, or connection pool exhaustion?
- Are there tests for behavior with empty inputs, maximum-size inputs, or malformed inputs?
- Are cleanup/teardown paths tested (do resources get released on failure)?

**Dependency failure testing:**
- Does the test suite include scenarios where external services return errors?
- Are network partition scenarios represented (even if simulated)?
- Are there tests for stale cache, expired tokens, or revoked credentials?

### Output Format

For each finding, state:
- The failure scenario (grounded in CIC failure modes)
- Whether it is tested, partially tested, or untested
- Red team category: boundary abuse / dependency failure / resource exhaustion / cascading failure
- Severity based on production impact

---

## Martin Kleppmann -- Data Correctness (Green Team Alignment)

Kleppmann evaluates whether the test suite verifies that data flows correctly through the system and that correctness invariants hold. His perspective maps to green team tests.

### Evaluation Criteria

**Correctness verification:**
- For each CIC section 3 (Guarantees): is there a test that verifies the guarantee holds?
- Are invariants tested at boundaries (before/after transformation, at module interfaces)?
- Are edge cases covered (empty collections, null/None values, boundary values)?

**State management:**
- Are state transitions tested for correctness?
- Are there tests that verify state consistency after sequences of operations?
- Are concurrent access patterns tested where applicable?

**Data flow integrity:**
- Is data transformation tested end-to-end (input → processing → output)?
- Are intermediate representations validated?
- Are there tests for data that passes through multiple components?

**Schema and contract boundaries:**
- Are input validation rules tested at system boundaries?
- Are there tests for schema evolution (new fields, removed fields, type changes)?
- Are serialization/deserialization round-trips tested?

**Ordering and timing:**
- Are tests sensitive to processing order where order matters?
- Are there tests for idempotency where the CIC claims idempotent behavior?
- Are there tests for determinism where the CIC claims deterministic output?

### Output Format

For each finding, state:
- The correctness property being tested (or missing)
- Which CIC guarantee it relates to
- Green team category: invariant / transformation / boundary / state management
- Whether the test is sufficient or needs strengthening

---

## Nancy Leveson -- System Safety (Beige Team Alignment)

Leveson evaluates whether the test suite addresses system-level safety concerns -- accidents that arise from normal component interactions rather than individual component failures. Her STAMP/STPA framework maps to beige team tests.

### Evaluation Criteria

**Unsafe control actions:**
- Are there tests for actions performed at the wrong time (too early, too late)?
- Are there tests for actions performed in the wrong sequence?
- Are there tests for actions performed with incorrect parameters that are technically valid?
- Are there tests for required actions that are NOT performed (omission)?

**Component interaction failures:**
- Are there tests where individually-correct components produce incorrect system behavior?
- Are there tests for assumption mismatches between interacting components?
- Are there tests for feedback loops that could amplify errors?

**Inadequate feedback and monitoring:**
- Are there tests that verify monitoring/logging captures the information needed to detect problems?
- Are there tests for scenarios where metrics look healthy but the system is in a degraded state?
- Are there tests for alert conditions and threshold behaviors?

**Decision-support safety:**
- If the system provides information for human decisions: are there tests for misleading outputs?
- Are there tests for over-trust scenarios (system appears confident but is wrong)?
- Are there tests for under-trust scenarios (system gives correct output but in an ambiguous way)?

**Human factors in operation:**
- Are there tests for configuration errors that a human operator might plausibly make?
- Are there tests for recovery procedures (can the system be restarted/reset safely)?
- Are there tests for the system's behavior when operated outside its design envelope?

### Output Format

For each finding, state:
- The safety scenario (grounded in actual system interactions)
- STAMP category: unsafe control action / interaction failure / inadequate feedback / decision-support risk
- Whether the scenario is tested, partially tested, or untested
- Potential consequence if the scenario occurs in production
