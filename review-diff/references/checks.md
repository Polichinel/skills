# Review Diff: Detailed Check Criteria

## Category A -- Naming and Clarity

### What to check

**Misleading names:**
- Function name implies read-only but function mutates state (e.g., `get_user` that also updates last_login)
- Name suggests one type but returns another (e.g., `count` that returns a boolean)
- Name implies single item but returns collection, or vice versa

**Ambiguous or generic names:**
- Variables named `data`, `result`, `tmp`, `val`, `info`, `obj` without qualification
- Functions named `process`, `handle`, `do`, `run` without specifying what
- Single-letter variables outside of trivial loops or lambdas

**Naming inconsistency:**
- Different convention than the surrounding file (camelCase in a snake_case file)
- Different verb for the same concept (`get_` vs `fetch_` vs `retrieve_` for the same operation pattern)
- Different noun for the same entity than what the rest of the module uses

**Unclear booleans:**
- Boolean variables or parameters where `True`/`False` meaning is ambiguous (e.g., `flag`, `status`, `check`)
- Boolean parameters without clear positive-case naming (prefer `is_valid`, `has_items`, `should_retry`)

**Comment quality:**
- Comments that restate the code ("increment counter by 1")
- Missing comments on non-obvious logic (complex conditionals, bitwise operations, domain-specific formulas)
- Stale comments that describe code that has been changed

### How to check

Read each changed name in context. Compare against the 5-10 nearest names in the same scope. Flag inconsistencies.

---

## Category B -- Complexity and Structure

### What to check

**Multi-responsibility functions:**
- Function contains distinct logical blocks separated by blank lines or comments (suggests separate responsibilities)
- Function has multiple unrelated side effects (writes to DB AND sends email AND logs metrics)
- Function name requires "and" to describe accurately

**Deep nesting:**
- 3+ levels of nested conditionals or loops
- Can be flattened with guard clauses (early returns) or extraction

**Long functions:**
- New function exceeding the module's typical function length
- Existing function made significantly longer by the change
- Judge relative to the file's baseline, not an absolute number

**Mixed abstraction levels:**
- Same function mixes high-level orchestration ("process the order") with low-level details ("split string on comma, parse int")
- Same function mixes business logic with infrastructure concerns (validation logic interleaved with HTTP response construction)

**God-method growth:**
- An already-large function getting larger
- A function accumulating conditional branches for different cases (suggest strategy/dispatch pattern)

### How to check

For each changed function: count responsibilities, measure nesting depth, compare length to file average. Read the function as a narrative -- does it tell a coherent story at one abstraction level?

---

## Category C -- Error Handling

### What to check

**Swallowed exceptions:**
- `except: pass` or `except Exception: pass`
- Catch block that logs but does not re-raise or return an error indicator
- `try/except` where the except path silently continues normal flow

**Overly broad catches:**
- `except Exception` when specific exceptions are known
- Catching at a level that masks the real error type from callers

**Missing error handling:**
- File I/O without handling FileNotFoundError or PermissionError
- Network calls without timeout or connection error handling
- Parsing/deserialization without handling malformed input
- Dictionary access without handling missing keys (where KeyError is possible)

**Error messages without context:**
- Exception raised with generic message ("An error occurred")
- Error log without the variable values that caused the failure
- Exception that loses the original traceback (raise without `from`)

**Silent fallbacks:**
- Returning a default value instead of raising when the operation fails
- Using `dict.get(key, default)` where the default masks a real problem
- Optional chaining (`?.` or `getattr(x, y, None)`) that hides missing attributes

### How to check

For each changed block: identify operations that can fail. Check if failure is handled, how it is handled, and whether the handling preserves diagnostic information.

---

## Category D -- Duplication and Reuse

### What to check

**Logic duplication:**
- New code that reimplements logic already present elsewhere in the codebase
- Same algorithm expressed differently in two places (search the module first, then the package)

**Copy-paste with variations:**
- Multiple blocks in the diff that differ only in variable names or constants
- Repeated conditional structures with different predicates but same shape

**Magic values:**
- Numeric literals without named constants (especially thresholds, limits, indices)
- String literals used as identifiers or keys (should be constants or enums)
- Repeated literal values that should be a single source of truth

### How to check

For significant new logic (5+ lines), search the codebase for similar patterns. Use grep for key function calls, algorithm-specific operations, or distinctive variable names. Limit initial search to the same package; broaden if the pattern is architectural.

---

## Category E -- Pattern Consistency

### What to check

**Structural patterns:**
- New code uses a different pattern than peer code in the same module (e.g., inheritance where the module uses composition, callbacks where it uses events)
- Different function signature style (positional args where module uses keyword-only, or vice versa)
- Different return type convention (returns None where peers raise, or vice versa)

**Error handling strategy:**
- Different exception types than what the module typically uses
- Different error propagation strategy (catching locally where module lets exceptions bubble, or vice versa)

**Data access patterns:**
- Different way of accessing shared state (direct attribute access where module uses getters, or vice versa)
- Different serialization approach than peer code

**Logging and observability:**
- Different log level conventions than surrounding code
- Missing logging where peer functions log
- Different log message format

**Import patterns:**
- Importing from a different level than peer code (importing internals where module uses public API)
- Circular import risk from new import

### How to check

Read 3-5 peer functions/methods in the same file or module. Identify the dominant patterns. Compare the changed code against them. Flag deviations. Note: deviation is not always wrong -- but it should be conscious, not accidental.

---

## Category F -- Contract Alignment (conditional)

This category is only applied when CICs exist for classes affected by the diff. If no CICs are found, skip entirely without comment.

### What to check

**New public methods:**
- Class has a CIC but the diff adds a public method not listed in CIC section 3 (Responsibilities and Guarantees)
- New method changes the class's API surface without CIC update

**Signature changes:**
- Method signature changed in a way that contradicts CIC section 4 (Inputs and Assumptions)
- Parameter removed or renamed that CIC documents
- Return type changed from what CIC describes

**Guarantee violations:**
- Change introduces behavior that contradicts a CIC guarantee statement
- Change weakens a guarantee (e.g., method documented as raising on invalid input now returns None)

**New failure modes:**
- Change introduces a new way the class can fail that is not in CIC section 6 (Failure Modes)
- Change alters failure behavior (different exception type, silent where CIC says loud)

**Boundary changes:**
- New dependency introduced that is not in CIC section 7 (Boundaries and Interactions)
- Interaction with a component not documented in the CIC

### How to check

For each CIC-governed class in the diff: read the CIC. Compare the diff against sections 3, 4, 6, and 7. Flag discrepancies. Each finding should reference both the CIC section and the diff line.

### Output for contract alerts

For each alert, state:
- Which CIC and which section
- What the CIC says
- What the diff does
- Whether the CIC needs updating or the code needs changing
