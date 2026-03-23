# Falsification Audit: Detailed Phase Instructions

## Phase 1 -- Parse Claim

Extract a precise, falsifiable hypothesis from the user's claim.

A good hypothesis is:
- **Scoped:** Names specific modules, functions, or capabilities
- **Measurable:** States what the system produces, guarantees, or prevents
- **Falsifiable:** You can construct a concrete test that would disprove it

Reformulation process:
1. Take the user's natural-language claim
2. Identify the subject (what module/component), the predicate (what it does/guarantees), and the consumer (who relies on it)
3. Rewrite as: "[Subject] provides [capability/guarantee] ready for [consumer] to [use case]"

**Good reformulations:**
- "datafactory_grid.build() returns a GeoDataFrame with one row per PRIO-GRID cell per year for the configured temporal range, with columns matching the schema defined in CIC-004 section 3."
- "The authentication middleware rejects expired tokens with HTTP 401 and a JSON error body containing an `error` field."
- "The pipeline produces deterministic output: running it twice with identical input and configuration yields byte-identical output files."

**Bad reformulations (stop and ask user to reformulate):**
- "The code works." -- No scope, no criteria. What code? Works how?
- "The module is good." -- Not falsifiable. Good by what measure?
- "Everything is tested." -- Too broad. Which behavior? Which guarantees?

If the claim cannot be made falsifiable after one reformulation attempt, **STOP** and tell the user: "This claim is not specific enough to audit. What specific behavior or guarantee should I try to disprove?"

---

## Phase 2 -- Scan Context

Locate governance documents, test suites, and source code relevant to the claim.

**Search order for governance docs:**

1. `docs/CICs/` or `CICs/`
2. `docs/ADRs/` or `ADRs/`
3. `ARCHITECTURE.md` or `docs/ARCHITECTURE.md`
4. `docs/standards/`
5. Any `.md` files in the module directory that describe behavior

For each document found, extract:
- Claims about behavior (CIC section 3)
- Declared failure modes (CIC section 6)
- Architectural invariants (ARCHITECTURE.md)
- ADR rules that apply to this module

**Graceful degradation:** If no governance docs exist, note: "No governance documentation found. Probes will be derived from code analysis, docstrings, and standard categories." Do not stop the skill.

**Identifying the code surface area:**

1. From the parsed claim, identify the primary module(s) or package(s)
2. Read the module's `__init__.py` or equivalent to identify the public API
3. Read docstrings of public functions/classes
4. Identify the test directory for this module
5. Run the existing test suite to confirm a green baseline

If existing tests fail: **STOP**. Report: "Cannot run a falsification audit on a red baseline. Fix failing tests first." The audit starts from a state where all known tests pass.

---

## Phase 3 -- Derive Probes

Generate probes from governance docs and standard categories. Consult `references/probes.md` for category definitions, examples, and the selection heuristic.

**Auto-derivation from governance docs (if present):**

From CICs:
- Section 3 (Responsibilities and Guarantees): One Category B probe per guarantee
- Section 4 (Inputs and Assumptions): One Category C probe per stated assumption
- Section 6 (Failure Modes): One Category C or F probe per declared failure mode
- "Does NOT own" statements: One Category B probe verifying the class does not perform the excluded action

From ARCHITECTURE.md:
- Each invariant claim: One Category E probe checking code matches the claim
- Each "provides" or "exposes" statement: One Category D probe simulating consumer usage

From ADRs:
- ADR-008 (if present): Automatic Category B probe -- log-before-raise compliance scan
- ADR-003 (if present): Automatic Category B probe -- fail-loud on semantic ambiguity
- ADR-009 (if present): Automatic Category B probe -- boundary contract validation at entry

**Auto-derivation from code (always):**
- Docstring claims: One Category B probe per behavioral claim in docstrings
- Type hints: One Category C probe for inputs that accept Optional types -- what happens with None?
- Default values: One Category E probe -- is the default consistent everywhere it appears?

**Applying the selection heuristic:**

Determine the situation (migrated code, greenfield, writes data, etc.) and select probe categories accordingly. See the selection heuristic table in `references/probes.md`.

**Minimum coverage:** Produce at least 3 probes from at least 3 different categories. Aim for 5-7 probes for a thorough audit.

---

## Phase 4 -- Present Probes

Present the complete probe list to the user in this exact format:

```
## Proposed Probes

| # | Cat | Probe Description | Risky Prediction |
|---|-----|-------------------|------------------|
| 1 | B   | [description]     | [what should happen if claim is true] |
| 2 | C   | [description]     | [what should happen if claim is true] |
| ...

**Claim:** [the parsed hypothesis from Phase 1]
**Coverage:** [N] probes across [M] categories ([list categories])
**Situation:** [migrated/greenfield/writes data/etc.]

Confirm these probes, modify, or add your own?
```

**STOP.** Do not proceed until the user confirms.

When handling user modifications:
- If the user adds probes: incorporate them with appropriate category tags
- If the user removes probes: remove them, but warn if coverage drops below 3 categories
- If the user modifies a probe: update it, confirm the risky prediction still makes sense
- If the user says "go" or "confirmed" or similar: proceed to Phase 5

---

## Phase 5 -- Predict Outcomes

For each confirmed probe, record the expected outcome as a risky prediction.

Format for each probe:

```
Probe #N ([category]): [description]
If the claim is true: [expected outcome]
Falsifying observation: [what outcome would disprove the claim]
```

**Why this step cannot be skipped:**

The risky prediction is the epistemological core of the audit. Without it:
- You cannot distinguish between "I found a bug" and "I found what I was looking for"
- You cannot distinguish between genuine falsification and post-hoc rationalization
- The audit degenerates into exploratory testing, which has its place but is not falsification

A risky prediction is one where you genuinely do not know whether the system will pass. If you are confident it will pass, the probe is not risky enough -- consider replacing it.

---

## Phase 6 -- Execute Probes

Run each probe. Capture exact results. Do not modify any existing code during this phase.

**Three execution modes:**

1. **Static analysis** (always allowed):
   - Reading source code, tracing call paths, checking imports
   - Comparing documentation against code
   - Counting functions, checking type signatures, verifying naming
   - Searching for patterns (e.g., every `raise` without a preceding `logger.error`)

2. **Dynamic analysis** (allowed when test infrastructure exists):
   - Running existing tests with different parameters or inputs
   - Calling public API functions with probe inputs from a Python shell or temporary script
   - Querying a database or API that the test environment provides

3. **Script execution** (allowed with constraints):
   - Writing and running a small verification script to test a specific probe
   - The script must be temporary -- delete it after capture, or run via stdin
   - The script must not modify any source files, configuration, or persistent state
   - The script must not install packages or change dependencies

**For each probe, capture:**
- The exact command, code snippet, or analysis steps performed
- The actual output or observation
- Whether it matches the predicted outcome from Phase 5
- Any unexpected observations (record even if they don't relate to the probe)

**No code modification during this phase.** You are observing, not fixing. If you find a bug, record it. Resist the urge to fix it immediately.

---

## Phase 7 -- Classify Findings

For each probe result that did not match the predicted outcome, classify using this decision tree:

```
Did the system produce a wrong answer silently?
  YES → Hard falsification

Did the system violate a documented contract (CIC, ADR, docstring)?
  YES → Hard falsification

Did the system behave unexpectedly but not dangerously?
  (Missing validation, undocumented edge case, surprising default)
  YES → Soft falsification

Is the behavior technically correct but surprising or poorly documented?
  YES → Observation
```

**Hard falsification examples:**
- Function returns wrong value without error
- Docstring says "raises ValueError" but function returns None
- ADR-008 says log-before-raise but a raise has no preceding log
- CIC guarantee is not enforced in code

**Soft falsification examples:**
- Function accepts None but produces confusing output instead of clear error
- Edge case is handled but the handling is undocumented
- Default value works but is not what a consumer would expect
- Missing input validation -- currently works but fragile

**Observation examples:**
- API is functional but call sequence is unintuitive
- Documentation is accurate but could be clearer
- Test exists but uses a mock where a real call would be better

---

## Phase 8 -- Generate Test Stubs

Create a failing test file for all hard and soft falsifications.

**File naming:**

1. Derive a slug from the claim: lowercase, replace spaces and special chars with underscores, truncate to 40 characters
2. File path: `tests/test_falsification_<slug>.py`
3. If a `tests/` directory doesn't exist, use the project's test directory (from pyproject.toml, setup.cfg, or convention)

**Adapt to the repository's language and test framework.** The examples below use Python/pytest. For other languages, use the equivalent:
- JavaScript: `__tests__/falsification_<slug>.test.js` with Jest
- Go: `falsification_<slug>_test.go` with standard testing
- Rust: inline `#[test]` module or separate test file

**Test stub format (Python/pytest):**

```python
"""
Falsification test stubs for claim: "<claim>"
Generated by /falsify audit on <date>

These tests are in TDD RED state -- they FAIL against the current code.
Fix the code to make them pass, then re-run /falsify to verify and check for regressions.
"""


def test_falsify_<probe_id>_<short_description>():
    """
    Probe <id> (Category <X>): <description>

    Finding: <what was actually observed>
    Severity: <hard/soft>

    Expected: <what should happen when the code is correct>
    """
    # TODO: Replace this stub with a proper test
    # <one-line description of what to test>
    assert False, "<summary of the falsification>"
```

**Rules:**
- One test function per hard or soft falsification
- Test names must be descriptive: `test_falsify_03_pgid_zero_returns_error`
- The docstring records the full probe context for the developer who will fix it
- `assert False` with a message is the stub -- the developer replaces it with a real test
- Observations (non-falsifying) are NOT included as test stubs
- The file header includes the claim and date for traceability

---

## Phase 9 -- Pattern Analysis

After all probes are complete, look across findings for systemic issues.

**Questions to answer:**

1. Did multiple probes in the same category find issues? (e.g., all boundary probes failed -- suggests systematic missing input validation)
2. Did the same root cause appear in multiple probes? (e.g., the same function is the source of multiple failures)
3. Is there a class of issues that the existing test suite structurally cannot catch? (e.g., documentation-code alignment, ADR compliance)
4. Did a specific ADR or CIC violation appear that also appeared in previous audits? (indicates a systemic governance gap)
5. Are the falsifications concentrated in one module or spread across the system?

**Common patterns:**
- "All boundary probes failed" → Missing input validation layer
- "Contract probes failed on the same ADR" → Governance rule not operationalized
- "Consistency probes found doc-code divergence" → Documentation not maintained during refactoring
- "Consumer simulation found API confusion" → Public interface designed inside-out (implementer perspective, not consumer perspective)

**Output:** A brief narrative (3-5 sentences) identifying the most important cross-cutting pattern and what it implies about the system's health.

---

## Phase 10 -- Report

Produce the structured output matching the Required Output Structure in SKILL.md.

**Section-by-section guidance:**

**1. Claim and Hypothesis:**
- Original claim (as the user stated it)
- Reformulated hypothesis (from Phase 1)
- Scope: which modules, functions, or components are covered

**2. Probe Plan:**
- The confirmed probe table from Phase 4 (with any user modifications)

**3. Probe Results:**
For each probe:
```
### Probe #N -- [short title]
**Category:** [A-G]
**Prediction:** [risky prediction from Phase 5]
**Actual:** [what happened]
**Verdict:** [Passed / Hard Falsification / Soft Falsification / Observation]
**Evidence:** [exact command, output, or code reference]
```

**4. Failing Tests:**
- File path of the generated test file
- Count of test stubs (hard + soft)
- Brief listing of test function names

**5. Pattern Analysis:**
- Cross-cutting narrative from Phase 9
- List of systemic issues identified

**6. Verdict:**

Decision logic:
- Any hard falsifications → **FALSIFIED** (N hard, M soft falsifications found)
- No hard, but soft falsifications → **CONTESTED** (M soft falsifications weaken the claim)
- No falsifications → **SURVIVED** (the claim has survived N probes across M categories)

Include the caveat for SURVIVED: "Survived means the claim withstood this specific set of probes. It does not mean the claim is proven true. Stronger claims require more probes."

After the verdict, add: "After fixing falsifications, re-run `/falsify` with the same claim to verify fixes and check for regressions."
