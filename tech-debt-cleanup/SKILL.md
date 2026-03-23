---
name: tech-debt-cleanup
description: Provides structured process for identifying and safely cleaning technical debt after large refactors, focusing on incremental improvement without architectural rewrites. Use when user says "clean up technical debt", "stabilize after refactor", "clean this code", "fix the mess", "incremental cleanup", or "reduce tech debt". Do NOT use for repository mapping (use repo-assimilation), code review (use expert-code-review), new feature development, or large-scale rewrites.
---

# Tech Debt Cleanup Protocol

## Important

Follow these rules strictly.

- Do not begin cleanup before completing the investigation phase.
- Do not perform large refactors. Prefer small, safe changes.
- Do not introduce architectural changes that increase memory usage or execution instability.
- Do not modify behavior unless the change is covered by tests.
- Do not attempt to fix everything at once. Work incrementally.
- Always document discovered technical debt before modifying code.
- If working from a repo-assimilation or expert-code-review output, use those findings as your starting debt inventory rather than re-investigating from scratch.

## Critical Constraint

Do NOT introduce changes that could:
- Increase memory footprint
- Introduce additional buffering or caching
- Expand data structures unnecessarily
- Increase algorithmic complexity in critical paths

If a cleanup might affect memory behavior or runtime stability, document the risk and defer it.

## Purpose

Provide a structured process for identifying and cleaning technical debt introduced during large refactors while preserving system stability.

The objective is **safe stabilization and incremental improvement**, not architectural perfection.

## Procedure

Execute these 5 phases sequentially. Complete Phase 1 fully before beginning any cleanup in Phase 3. For detailed instructions, consult `references/phases.md`.

1. **Technical Debt Investigation** -- Map all debt: patches, hacks, SOLID violations, duplicated logic, dead code, unclear boundaries
2. **Prioritization** -- Rank by safety of change, maintainability impact, stability impact, and ease of improvement
3. **Controlled Cleanup** -- Small, safe, incremental changes with tests before refactoring
4. **Structural Improvements** -- Clarify boundaries, reduce coupling, split oversized units (where safe)
5. **Verification** -- Confirm tests pass, behavior unchanged, no memory/runtime degradation after each change

## Required Output Structure

1. Investigation Summary
2. Technical Debt Map (location, problem type, risk level, recommended strategy)
3. Cleanup Plan (prioritized list of safe improvements)
4. Cleanup Actions (changes performed or proposed)
5. Deferred Issues (debt left unresolved due to risk)
6. Stabilization Summary (how cleanup improves maintainability without increasing risk)

## Performance Notes

- Take your time. Safety is more important than speed.
- Do not skip the investigation phase
- Verify after every change, not just at the end
- When in doubt, defer rather than risk destabilization
