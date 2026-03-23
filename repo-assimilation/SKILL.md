---
name: repo-assimilation
description: Builds a structured mental model of a repository through 8 sequential phases covering structure, dependencies, execution flow, data structures, invariants, tests, and risks. Use when user says "assimilate this repo", "understand this codebase", "map this project", "analyze repo structure", "onboard me to this codebase", or "walk me through this repo". Do NOT use for code review, refactoring, bug fixes, or cleanup tasks.
---

# Repository Assimilation Protocol

## Important

Follow these rules strictly.

- Do not propose fixes, refactors, or design improvements during this protocol.
- Do not jump to conclusions about behavior before tracing the code.
- Do not assume architecture without locating supporting evidence in files or modules.
- Ground all statements in specific files, modules, or directories.
- If evidence is insufficient, explicitly state: "insufficient evidence."
- Complete all phases before proposing or implementing any changes.

## Purpose

Construct a structured understanding of how a repository works before performing analysis, refactoring, or remediation.

## Procedure

Execute these 8 phases sequentially. Before proceeding to the next phase, confirm the current phase output is complete.

For detailed instructions on each phase, consult `references/phases.md`.

1. **Repository Structure** -- Map directories, classify roles, identify entrypoints
2. **Dependency Graph** -- Map imports, external libraries, coupling patterns
3. **Execution Flow** -- Trace from entrypoints through processing stages
4. **Core Data Structures** -- Identify central objects, their lifecycle, and data flow
5. **Invariants and Assumptions** -- Surface implicit rules and where they may silently fail
6. **Tests and Validation** -- Assess coverage, quality, and gaps
7. **Technical Risks** -- Document structural risks (do not propose fixes)
8. **System Summary** -- Produce a concise overview for a senior engineer

If the repository is too large to fully trace, focus on the 3 most important entrypoints and note what was excluded.

## Required Output Structure

Produce output with exactly these 8 sections:

1. Repository Structure Overview
2. Dependency Graph Description
3. Execution Flow Description
4. Core Data Structures and Concepts
5. System Invariants and Assumptions
6. Test Coverage Analysis
7. Technical Risk Inventory
8. System Summary

## Performance Notes

- Take your time to do this thoroughly
- Quality is more important than speed
- Do not skip phases or combine them
- Do not skip validation steps
