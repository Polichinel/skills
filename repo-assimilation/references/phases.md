# Repository Assimilation: Detailed Phase Instructions

## Phase 1 -- Repository Structure

Build a structural map of the repository.

Identify:
- Top-level directories
- Core modules or packages
- Infrastructure code
- Test directories
- Configuration files
- Scripts and utilities
- Documentation

Produce a hierarchical overview of the repository.

For each major directory, classify its role:
- Application logic
- Infrastructure or orchestration
- Data processing
- Configuration
- Testing
- Tooling

Then identify likely entrypoints:
- CLI interfaces
- Main scripts
- Orchestration pipelines
- APIs
- Training scripts
- Scheduled jobs

**Output format:** Hierarchical tree with role annotations. Entrypoints listed separately with file path and type.

Do not infer behavior yet. Only map structure.

---

## Phase 2 -- Dependency Graph

Construct a dependency map of the system.

For each core module identify:
- What it imports
- What imports it
- External libraries used
- Configuration dependencies
- Environment variables or global state

Highlight:
- Circular dependencies
- Tightly coupled modules
- Modules with many inbound dependencies (high fan-in)
- Modules with many outbound dependencies (high fan-out)
- Modules that appear unused

**Output format:** For each module, list: module name, imports, imported-by, external deps, flags (circular/tight-coupling/unused).

---

## Phase 3 -- Execution Flow

Determine how the system executes in practice.

Start from entrypoints identified in Phase 1 and trace execution paths through the system.

Identify major processing stages such as:
- Data loading
- Preprocessing
- Feature generation
- Model training
- Inference
- Evaluation
- Persistence or output

Describe the order in which components interact.

**Output format:** For each entrypoint, produce a numbered sequence of steps: component called, what it does, what it passes to the next component.

---

## Phase 4 -- Core Data Structures

Identify central objects and data structures used across the system.

Examples may include:
- Data frames
- Tensors
- Domain-specific objects
- Configuration containers
- Dataset objects
- Prediction containers

For each important data structure determine:
- Where it is created
- Where it is transformed
- Where it is consumed
- Where it exits the system

**Output format:** For each data structure: name, type, created-in, transformed-in, consumed-in, exits-via.

---

## Phase 5 -- Invariants and Assumptions

Identify the implicit rules the system relies on.

Examples include:
- Required data schemas
- Ordering assumptions
- Deterministic seeds
- Expected shapes or types
- Required configuration keys
- Expected value ranges

Determine:
- Where these rules are enforced (explicit checks, assertions, type hints)
- Where they are only implicitly assumed (no enforcement)

**Output format:** For each invariant: rule description, where enforced, where assumed-only, risk-if-violated.

Highlight areas where silent failure could occur.

---

## Phase 6 -- Tests and Validation

Analyze the test suite.

Determine:
- Which modules are covered by tests
- Which behavior is validated
- Where test coverage appears weak
- Whether tests verify real functionality or only mocked behavior

**Output format:** Table with columns: module, test-file, coverage-level (good/partial/none), notes.

Highlight important parts of the system that appear untested or under-tested.

---

## Phase 7 -- Technical Risks

Based on the previous phases, identify structural risks:
- Hidden coupling between modules
- Unclear module boundaries
- Duplicated logic
- Configuration drift
- Fragile execution paths
- Reliance on global state
- Difficult-to-test components

**Output format:** For each risk: description, location, severity (low/medium/high), evidence from earlier phases.

Do not propose fixes yet. Only document the risks.

---

## Phase 8 -- System Summary

Produce a concise summary containing:
- The repository's overall purpose (1-2 sentences)
- The main architectural components (bulleted list)
- The execution pipeline (brief description)
- The core data structures (names and roles)
- The most important system invariants (top 3-5)
- The most significant architectural risks (top 3-5)

The summary should allow a senior engineer to quickly understand how the system works and where the bodies are buried.
