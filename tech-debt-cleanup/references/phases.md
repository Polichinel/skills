# Tech Debt Cleanup: Detailed Phase Instructions

## Phase 1 -- Technical Debt Investigation

Before making any modifications, map the current technical debt.

Identify and document:
- Patches and temporary fixes
- Hacks or workarounds
- Violations of SOLID principles
- Unclear ownership or responsibility boundaries
- Overly complex or hard-to-understand code paths
- Duplicated logic
- Unused or dead code
- Modules with multiple responsibilities
- Areas where abstractions leak internal complexity
- Code paths likely to create memory pressure or execution instability

Also identify:
- Modules with high cognitive complexity
- Fragile or missing tests
- Unclear data flow between components

**Output format:** Table with columns: Location (file/module), Problem Type (duplication/coupling/abstraction leak/dead code/etc.), Risk Level (low/medium/high to modify), Recommended Strategy (refactor/simplify/isolate/test-first/defer).

Do not perform cleanup yet. The goal is to **understand the mess before touching it**.

---

## Phase 2 -- Prioritization

From the investigation results, prioritize issues using these criteria (in order):

1. **Safety of change** -- How likely is this change to break something?
2. **Impact on maintainability** -- How much does fixing this improve the codebase?
3. **Impact on system stability** -- Does fixing this reduce runtime risk?
4. **Ease of improvement** -- How much effort is required?

Prefer improvements that:
- Simplify code without changing behavior
- Remove duplication
- Clarify module responsibilities
- Improve testability

Avoid improvements that require major structural rewrites.

**Output format:** Ordered list with columns: Priority (#), Issue (from debt map), Safety (safe/moderate/risky), Impact (low/medium/high), Effort (small/medium/large), Decision (fix now/fix later/defer).

---

## Phase 3 -- Controlled Cleanup

Begin incremental cleanup. Apply these principles:

- Prefer small changes over large changes
- Improve readability and structure where risk is low
- Remove duplication when behavior can be verified
- Isolate complex logic behind clear abstractions
- Improve naming and clarity where intent is unclear

When modifying code:
- Add tests before refactoring if tests are missing
- Ensure existing tests continue to pass
- Verify behavior remains unchanged

**Critical:** Do not introduce changes that could:
- Increase memory footprint
- Introduce additional buffering or caching
- Expand data structures unnecessarily
- Increase algorithmic complexity in critical paths

If a cleanup might affect memory behavior, document the risk and defer it.

**Output format:** For each change: what was changed, why, files modified, tests added/verified, risk assessment.

---

## Phase 4 -- Structural Improvements

Where safe, apply limited structural improvements:
- Clarify module boundaries
- Reduce cross-module coupling
- Split overly large functions or classes
- Remove shallow abstractions that obscure behavior

Do not introduce new frameworks or architectural layers during cleanup.

**Output format:** For each improvement: what was improved, before/after description, files modified, verification status.

---

## Phase 5 -- Verification

After each cleanup change:
- Confirm all tests pass
- Confirm behavior remains unchanged
- Confirm memory usage or runtime characteristics are not degraded

If uncertainty exists, revert the change and document the issue.

**Output format:** Verification checklist: change description, tests pass (yes/no), behavior unchanged (yes/no), performance impact (none/improved/degraded), status (accepted/reverted).
