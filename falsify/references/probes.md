# Falsification Probes: Categories and Selection

Seven probe categories target different dimensions of a claim. Each category attacks a distinct failure mode that other categories miss.

---

## Category A -- Parity Probes

**Definition:** Compare the system's output against a known-good reference to detect divergence.

**Use when:** Migrating code from another repository, reimplementing existing functionality, or replacing a dependency. Not applicable for greenfield code (no reference exists).

**How to probe:**
1. Identify the reference implementation or golden values
2. Run both the new and reference code with identical inputs
3. Compare outputs element-by-element or structurally
4. Any divergence is a potential falsification

**Example:**
- Claim: "The new grid generator produces identical output to the legacy version."
- Probe: Generate the default grid with both codebases. Compare all 259,200 pgids element-by-element.
- Falsification criterion: Any pgid produces different lat/lon coordinates.

**Example:**
- Claim: "The refactored parser handles all existing input formats."
- Probe: Run the parser against the full regression test corpus from the legacy system. Compare output field-by-field.
- Falsification criterion: Any input produces a different parse result.

---

## Category B -- Contract Probes

**Definition:** Check every claim in CICs, ARCHITECTURE.md, ADRs, and docstrings against actual code behavior.

**Use when:** Code has governance documentation (CICs, ADRs), docstrings with behavioral claims, or an ARCHITECTURE.md with stated invariants. This is where documentation lies are caught.

**How to probe:**
1. For each CIC guarantee (section 3): construct an input that would violate it if the guarantee is not enforced
2. For each CIC failure mode (section 6): trigger the failure condition and verify the declared behavior occurs
3. For each ADR rule: trace every code path and check compliance
4. For each docstring claim: write a minimal test of that claim

**Auto-derivation from CICs:**
- Section 3 (Responsibilities and Guarantees) -> one contract probe per guarantee
- Section 6 (Failure Modes and Loudness) -> one boundary probe per declared failure mode
- Section 4 (Inputs and Assumptions) -> one probe per stated assumption
- "Does NOT own" statements -> verify the class truly does not perform that action

**Standard ADR probes:**
- ADR-008 compliance: For every `raise` in the module, does `logger.error` precede it?
- ADR-003 compliance: When semantic ambiguity occurs, does the system fail loud or guess silently?

**Example:**
- Claim: "The harvester validates all events before storage."
- Probe: CIC says validate_events raises ValueError on missing required fields. Pass an event with field `id` set to None.
- Falsification criterion: No ValueError raised; event silently accepted.

**Example:**
- Claim: "ADR-008 is enforced: all structural failures are logged before raising."
- Probe: Trace every `raise` statement in the package. Check that `logger.error(...)` appears on a preceding line in the same block.
- Falsification criterion: Any `raise` without a preceding `logger.error` call.

---

## Category C -- Boundary Probes

**Definition:** Feed the system inputs that are technically accepted but semantically questionable -- just outside valid range, exactly on boundaries, zero-length, negative, None, empty.

**Use when:** The system processes numeric ranges, indexed data, collections, date ranges, or any input with defined boundaries. Especially important for code that writes data.

**How to probe:**
1. Identify every input parameter with a valid range or type constraint
2. Test: exactly at the lower boundary, one below, exactly at the upper boundary, one above
3. Test: zero, negative, None, empty string, empty collection
4. The question is not "does it crash?" but "does it produce the RIGHT answer or the right error?"

**Example:**
- Claim: "pgid_to_latlon correctly converts PRIO-GRID cell IDs to coordinates."
- Probe: pgid_to_latlon(0) -- pgid is 1-indexed. What happens with 0?
- Expected: ValueError ("pgid must be in [1, n_cells]")
- Falsification criterion: Returns coordinates without error (silent garbage).

**Example:**
- Claim: "The truncation function handles all valid lengths."
- Probe: truncate(text, length=-1). What happens with negative length?
- Falsification criterion: Returns garbage string instead of raising ValueError.

**Standard boundary inputs by type:**

| Type | Boundary values |
|------|----------------|
| Integer | 0, -1, 1, MAX_INT, MIN_INT |
| String | "", " ", very long string (10k chars), unicode edge cases |
| Collection | [], [single], [duplicate elements], None |
| Date/time | epoch, pre-epoch, far future, DST transition, leap second |
| Float | 0.0, -0.0, NaN, Inf, -Inf, very small positive |
| Index | 0 (if 1-indexed), -1, len+1, len |

---

## Category D -- Consumer Simulation Probes

**Definition:** Mentally walk through a realistic consumer workflow using only the public API. Look for awkward call sequences, surprising defaults, missing conveniences, and footguns.

**Use when:** The claim is about a module or API being "ready" for use by other components or developers. Especially important for greenfield code with no existing consumers yet.

**How to probe:**
1. Identify the intended consumers (from the claim, CICs, or ARCHITECTURE.md)
2. Write a realistic usage scenario from scratch, using only the public API
3. At each step ask: "Would a real consumer know to do this? Would they be surprised by the result?"
4. Check: are required imports obvious? Is the call sequence intuitive? Do return types match what the consumer needs next?

**Example:**
- Claim: "datafactory_grid is ready for the compiler to place events onto the grid."
- Probe: A compiler developer calls `build()`, receives a GeoDataFrame, and needs to look up the cell for coordinates (59.5, 10.7). Walk through: is there a function for this? Is the return type what the compiler expects?
- Falsification criterion: The lookup requires non-obvious steps, undocumented parameters, or returns a type incompatible with the compiler's expected input.

**Example:**
- Claim: "The authentication module is ready for the API layer to use."
- Probe: An API handler imports auth, calls `authenticate(token)`. What does it return? Does the handler need to check for None, catch exceptions, or inspect a status code? Is the contract clear from the function signature and docstring alone?
- Falsification criterion: The authentication function's contract is ambiguous -- the consumer cannot determine correct usage without reading the implementation.

---

## Category E -- Consistency Probes

**Definition:** Check whether every representation of the same fact agrees across all locations in the codebase.

**Use when:** The system has documentation alongside code, configuration defined in multiple places, version strings, default values, or cross-referenced specifications. Code with governance docs (ADRs, CICs) is especially prone.

**How to probe:**
1. Identify facts that are stated in multiple places (config defaults, version strings, schema definitions, capability claims)
2. For each fact, locate every representation
3. Compare them literally
4. Any discrepancy is a consistency violation

**Example:**
- Claim: "The grid module is internally consistent."
- Probe: DEFAULT_GRID_CONFIG is defined in config.py. Is the same object used in generator.py and validation.py? Or are there independent instances with potentially different values?
- Falsification criterion: Two different default config objects exist with divergent values.

**Example:**
- Claim: "The documentation accurately describes the API."
- Probe: ARCHITECTURE.md says the module exposes 5 public functions. Count the actual public functions in __init__.py.
- Falsification criterion: The count differs, or functions are listed in docs that don't exist in code.

**Common consistency targets:**
- Docstring claims vs actual behavior
- CIC guarantees vs test coverage
- ARCHITECTURE.md capability list vs actual exports
- Version strings in pyproject.toml vs __init__.py
- Default values in config vs defaults used in constructors
- Error messages referencing parameter names that have been renamed

---

## Category F -- Adversarial Probes

**Definition:** Test robustness to garbage, malformed, or hostile input. Not about security -- about whether the system fails gracefully or produces silent garbage.

**Use when:** The system processes external input (API responses, user data, file formats), or the claim involves robustness or error handling. Important for greenfield code where input validation patterns haven't been stress-tested.

**How to probe:**
1. Identify every external input boundary
2. For each: what if the input is None? Wrong type? Correct type but nonsensical value?
3. For structured inputs: what if fields are missing, extra, reordered, or wrong type?
4. The question is: does the system fail loudly (good) or produce plausible garbage (bad)?

**Example:**
- Claim: "The event processor handles API failures gracefully."
- Probe: Pass events where every field is None. Pass a list where id is a list (unhashable type). Pass events with extra unexpected fields.
- Falsification criterion: TypeError or AttributeError propagates unhandled; or worse, silently produces records with None values in required fields.

**Standard adversarial inputs:**

| Input type | Adversarial values |
|-----------|-------------------|
| Dict/object | Missing keys, extra keys, None values, wrong value types |
| List | Empty, None elements, unhashable elements, nested lists |
| File/path | Nonexistent, empty file, wrong format, permission denied |
| String field | None, empty, whitespace-only, extremely long, unicode control chars |
| Numeric field | None, NaN, Inf, string "123", negative when unsigned expected |

---

## Category G -- Temporal Probes

**Definition:** Test whether the system behaves correctly across time -- repeated calls, ordering dependencies, cache staleness, and state accumulation.

**Use when:** The system caches results, maintains state across calls, processes ordered data, or makes idempotency claims. Important for code that writes data or manages provenance.

**How to probe:**
1. Call the same operation twice. Does the second call produce the same result?
2. Call operations in a different order. Does the result change?
3. If caching exists: modify the source, re-call. Does the cache invalidate correctly?
4. If the system accumulates state: does cleanup happen? Can state leak across runs?

**Example:**
- Claim: "The shapefile fetcher correctly caches downloads."
- Probe: Call fetch_shapefile() twice. Does the second call re-download or correctly skip? Modify the source file between calls. Does the cache detect staleness?
- Falsification criterion: Second call re-downloads unnecessarily (waste), or source modification is not detected (stale cache served).

**Example:**
- Claim: "The digest computation is deterministic."
- Probe: Compute digest(content) twice with identical input. Compare results. Then compute with content containing the same data in different insertion order (for dicts/sets).
- Falsification criterion: Same logical content produces different digests, or different content produces the same digest.

---

## Probe Selection Heuristic

Not every audit needs all probe categories. Select based on the situation:

| Situation | Prioritize | Rationale |
|-----------|-----------|-----------|
| Migrated code (from another repo) | A (parity), B (contracts), E (consistency) | Must match reference; docs may describe old behavior |
| Greenfield code (no reference) | C (boundaries), D (consumer), F (adversarial) | No reference to compare; test edges and usability |
| Code that writes data | C (boundaries), G (temporal), B (contracts) | Wrong writes are hard to undo; ordering and edges matter |
| Code with governance docs (ADRs, CICs) | B (contracts), E (consistency) | Docs create testable promises; check if they're kept |
| Code touching provenance/audit | G (temporal), B (contracts), E (consistency) | Provenance must be deterministic, complete, and honest |
| Code with external dependencies | F (adversarial), B (contracts), D (consumer) | External inputs are unreliable; test failure handling |

When the situation is mixed, select the union of prioritized categories. If in doubt, include Category B (contracts) -- it applies everywhere.

**Minimum coverage:** 3-5 probes from at least 3 different categories.

---

## Probe Quality Checklist

Before finalizing each probe, verify:

- **Specific:** The probe targets a concrete, identifiable behavior -- not a vague property.
- **Executable:** The probe can be run as analysis, code reading, or a targeted script. If it requires human judgment to evaluate, refine it until the pass/fail criterion is mechanical.
- **Falsifying:** The probe could genuinely fail. If you are confident it will pass, it is not a useful probe -- replace it with one targeting a riskier area.
- **Independent:** The probe's result does not depend on another probe passing first. Each probe stands alone.

**Red flags that a probe is weak:**
- "Check that the function works correctly" -- too vague, not falsifiable
- A probe you designed because you already read the code and know it passes -- this is confirmation, not falsification
- A probe that tests an implementation detail rather than a contract ("line 47 calls logger.error" vs "invalid input produces an ERROR log entry")
