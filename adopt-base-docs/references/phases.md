# Adopt Base Docs: Detailed Phase Instructions

## Phase 1 -- Locate Base Docs

Check `~/brain/8_system/templates/base_docs` for the template directory.

If not found, ask the user for the path. Do not guess.

Validate the directory contains:
- `ADRs/` with `README.md`, `adr_template.md`, and constitutional ADRs (000-009)
- `CICs/` with `README.md` and `cic_template.md`
- `contributor_protocols/` with `carbon_based_agents.md`, `silicon_based_agents.md`, `hardened_protocol_template.md`
- `standards/` with `logging_and_observability_standard.md`, `physical_architecture_standard.md`
- `INSTANTIATION_CHECKLIST.md`
- `validate_docs.sh`

If validation fails, report what is missing and stop.

---

## Phase 2 -- Consume Assimilation

This phase requires prior repo-assimilation output. If no assimilation has been run in this session or a previous session, **STOP** and tell the user:

> "This skill requires repo-assimilation output as a prerequisite. Please run 'assimilate this repo' first, then re-invoke adopt-base-docs."

If assimilation output is available (from earlier in the conversation or provided by the user), extract:

1. **Repository Structure Overview** -- directories, modules, entrypoints
2. **Core Data Structures and Concepts** -- central classes and their roles
3. **Dependency Graph** -- coupling and dependency patterns
4. **Execution Flow** -- pipeline stages and orchestration
5. **System Invariants** -- implicit rules and assumptions
6. **Test Coverage** -- what is tested and where test files live
7. **Technical Risks** -- structural issues and fragilities

These map directly to ADR adaptation:
- Structure + Data Structures → ADR-001 ontological categories
- Dependencies → ADR-002 topology rules
- Invariants → ADR-003 authority, ADR-009 boundary contracts
- Test Coverage → ADR-005 testing doctrine
- Technical Risks → ADR-004 evolution considerations

---

## Phase 3 -- Gather Project Identity

Much of this comes from the assimilation output. Collect or confirm:

**From assimilation (confirm with user):**
- Project name
- One-sentence purpose
- Domain vocabulary and naming patterns found in code

**From user:**
- Domain metaphor family (or confirm the naming patterns extracted from code)
- Docs directory name (default: `docs/`)
- Organization style: flat or lifecycle folders (default: flat)
- Deciders field value (default: "Project maintainers")
- Numbering scheme: preserve 000-009 or custom (default: preserve)

Do not re-ask information that is clearly available from assimilation output.

---

## Phase 4 -- Map Ontology

This is the critical creative phase. Map actual code entities to ontological categories.

Using the assimilation output's "Core Data Structures and Concepts" and "Repository Structure":

1. Identify all non-trivial classes and their roles
2. Group them into ontological categories (e.g., "Data Handlers", "Orchestrators", "Validators", "Configurations")
3. For each category, determine:
   - **Category name** (using the project's domain vocabulary where possible)
   - **Purpose** (what this category of entity does)
   - **Authority level** (authoritative vs derived)
   - **Stability** (stable, evolving, experimental)
   - **Representative classes** (actual class names that belong here)
   - **File locations** (where these classes live)

Present the ontology mapping to the user as a table:

| Category | Purpose | Classes | Files | Stability |
|----------|---------|---------|-------|-----------|

**STOP and wait for user confirmation** before proceeding.

Also during this phase, identify non-trivial classes that will need CICs. A class is non-trivial if it:
- Is a core domain class
- Sits at an architectural boundary
- Orchestrates other components
- Owns state
- Enforces invariants
- Modifies semantics or transformation

Present the CIC candidate list to the user. **STOP and wait for confirmation** of which classes to write CICs for.

---

## Phase 5 -- Select Constitutional ADRs

Present the constitutional ADR table (same as init-base-docs):

| ADR | Title | Role |
|-----|-------|------|
| 000 | Use of ADRs | Meta-governance (always recommended) |
| 001 | Ontology of the Repository | Defines what exists (always recommended) |
| 002 | Topology and Dependency Rules | Defines structural direction |
| 003 | Authority of Declarations Over Inference | Defines semantic authority |
| 004 | Rules for Evolution and Stability | Deferred by default -- ask user |
| 005 | Testing as Mandatory Critical Infrastructure | Testing doctrine (red/beige/green) |
| 006 | Intent Contracts for Non-Trivial Classes | CIC governance |
| 007 | Silicon-Based Agents as Untrusted Contributors | AI contributor governance |
| 008 | Observability and Explicit Failure | Fail-loud + logging requirements |
| 009 | Boundary Contracts and Configuration Validation | Interface contracts |

For ADR-004 specifically: present context from the assimilation's Technical Risk Inventory. Ask the user whether evolution and stability rules should be activated or remain deferred.

If the user excludes ADR-000 or ADR-001, warn that these are foundational.

If the user excludes ADR-006 but CICs are being written, warn about governance gap.

---

## Phase 6 -- Adapt ADRs

For each selected ADR, read the template from base_docs and apply these transformations:

### Metadata
- Status: `--template--` → `Accepted`
- Date: set to today
- Deciders: from Phase 3

### Title
Include the project name where natural.

### Context section
Ground in the actual codebase. Reference real architectural patterns discovered in Phase 2. Explain why this governance rule matters for THIS project's actual structure.

### Core sections
Populate with code-grounded content:

- **ADR-001 (Ontology):** Use the confirmed ontology mapping from Phase 4. Each category must reference actual class names and file paths. The "Core Ontological Categories" section should list categories with their representative classes.

- **ADR-002 (Topology):** Ground dependency rules in the actual dependency graph from assimilation. Reference real module relationships.

- **ADR-003 (Authority):** Reference actual places where inference vs declaration matters in this codebase. Use examples from the code.

- **ADR-004 (Evolution):** If activated, ground in actual technical risks from assimilation. If deferred, keep the template's deferred status.

- **ADR-005 (Testing):** Reference actual test files and coverage from assimilation. Map red/beige/green categories to the project's actual test structure.

- **ADR-006 (Intent Contracts):** Reference the CICs being created in Phase 7. List which classes have contracts.

- **ADR-007 (Silicon Agents):** Ground in the project's actual use of AI tools. Reference existing patterns.

- **ADR-008 (Observability):** Reference actual logging/error handling patterns found in the code.

- **ADR-009 (Boundary Contracts):** Reference actual module boundaries and interface patterns from the dependency graph.

### Cross-references
Ensure all ADR-to-ADR references point to included ADRs. Note exclusions where applicable.

### Consequences
Include project-specific consequences. The "Negative" subsection should honestly note constraints this governance imposes on the existing codebase.

---

## Phase 7 -- Write CICs

For each confirmed non-trivial class from Phase 4:

1. Read the `cic_template.md` from base_docs
2. Read the actual class source code
3. Fill each CIC section grounded in the actual implementation:

### Section-by-section guidance:

- **Purpose:** What does this class actually do? One or two sentences.
- **Non-Goals:** What does it NOT do that might be tempting to assume? Look for responsibilities that are handled elsewhere.
- **Responsibilities and Guarantees:** Observable behavior based on actual method signatures. Use "guarantees that" language.
- **Inputs and Assumptions:** Actual constructor parameters, configuration requirements, preconditions.
- **Outputs and Side Effects:** What it actually produces. Include state changes, logging, file I/O.
- **Failure Modes and Loudness:** How does it actually fail? Does it raise exceptions, return None, log silently? Be honest.
- **Boundaries and Interactions:** Which other classes does it actually interact with? Reference the dependency graph.
- **Examples of Correct Usage:** Real usage patterns from the codebase or tests.
- **Examples of Incorrect Usage:** Anti-patterns specific to this class.
- **Test Alignment:** Reference actual test files. Note coverage gaps.
- **Evolution Notes:** Based on technical risks from assimilation. What is likely to change?

### Known Deviations section (added after section 11):

Add a `## 12. Known Deviations` section for each CIC that documents:
- Places where the class behavior doesn't match what the contract would ideally specify
- Technical debt that affects this class
- Implicit assumptions that should be made explicit
- Missing tests or coverage gaps

This section is mandatory for brownfield CICs. Honest documentation of deviations is the whole point of brownfield adoption.

### CIC metadata:
- Status: `Active`
- Owner: from Deciders in Phase 3
- Last reviewed: today's date
- Related ADRs: list actual ADR numbers that govern this class

---

## Phase 8 -- Set Up Contributor Protocols

### Always include:
- **carbon_based_agents.md** -- Copy from base_docs. Adapt team/role references to match the project's actual team structure (from assimilation output and user input).
- **silicon_based_agents.md** -- Copy from base_docs. Adapt tooling references to match the project's actual AI tools. Use assimilation output to identify how AI tools are currently used in the project. Verify ADR-007 cross-references are correct.

### Ask about:
- **hardened_protocol_template.md** -- This is domain-specific (ML/reproducibility-critical systems). Present it to the user and ask: "Does this project involve ML, numerical computation, or reproducibility-critical workloads?" If yes, include and adapt with actual operational constraints from the codebase. If no, skip.

---

## Phase 9 -- Set Up Standards

### Always include:
- **logging_and_observability_standard.md** -- Copy from base_docs. Ground in the project's actual logging patterns (from assimilation output). Reference actual logging calls, error handling patterns, and monitoring infrastructure found in the code. Verify ADR-008 cross-references are correct.

### Ask about:
- **physical_architecture_standard.md** -- This enforces the 1-class-1-file rule and a specific directory ontology. Present it to the user and ask: "Does this project follow a 1-class-1-file convention?" If the assimilation output shows the project already uses this pattern, recommend including it. If the codebase has multi-class files, note the deviation and let the user decide.

---

## Phase 10 -- Write Files

Create the full directory structure under the docs directory name from Phase 3.

### Flat organization (default):
```
<docs-dir>/
├── ADRs/
│   ├── README.md           (adapted navigation)
│   ├── adr_template.md     (verbatim from base_docs)
│   ├── 000_use_of_adrs.md  (adapted)
│   ├── 001_ontology_of_the_repository.md (adapted)
│   ├── ... (other selected ADRs)
├── CICs/
│   ├── README.md           (adapted, listing all created CICs)
│   ├── cic_template.md     (verbatim from base_docs)
│   ├── ClassName.md        (one per confirmed class)
│   └── ...
├── contributor_protocols/
│   ├── carbon_based_agents.md  (adapted)
│   ├── silicon_based_agents.md (adapted, grounded in project tooling)
│   └── hardened_protocol_template.md (if selected)
├── standards/
│   ├── logging_and_observability_standard.md (adapted, grounded in project patterns)
│   └── physical_architecture_standard.md    (if selected)
├── INSTANTIATION_CHECKLIST.md  (adapted, completed items checked)
└── validate_docs.sh            (verbatim from base_docs)
```

### CIC file naming:
Use PascalCase matching the class name: `ClassName.md`

### ADRs/README.md adaptation:
- List only the ADRs that were actually created
- Update descriptions to reflect adapted titles
- Keep the Governance Structure section, removing references to excluded ADRs
- Update the Project-Specific ADRs section with suggested 010+ candidates from Phase 6

### CICs/README.md adaptation:
- List all created CICs in the "Active Contracts" section
- Update governance cross-references to match actual ADR numbers
- Add a note about which classes still need CICs (if any were deferred)

### INSTANTIATION_CHECKLIST.md
Copy from base_docs. Check off items that the skill has completed. Leave unchecked items that were skipped or deferred.

### validate_docs.sh
Copy verbatim from base_docs. Do not modify.

---

## Phase 11 -- Verify Coherence

Extended verification for brownfield. Check everything from init-base-docs plus code-grounding:

1. All ADRs have Status `Accepted` (except ADR-004 if deferred)
2. All ADRs have today's date and the deciders value
3. ADR-001 ontology categories reference actual classes that exist in the codebase
4. ADR-002 dependency rules reflect actual module relationships
5. Every ADR cross-reference points to an ADR that exists
6. Every CIC references a class that exists in the codebase
7. CIC method names match actual method signatures
8. CIC test file references point to files that exist
9. CIC "Known Deviations" sections are present and non-empty where applicable
10. CIC README lists all created CICs
11. ADR README navigation matches actual files
12. Templates are unmodified copies of originals
13. contributor_protocols/ contains the selected protocol files, grounded in project context
14. standards/ contains the selected standard files, grounded in project patterns
15. INSTANTIATION_CHECKLIST.md is present with completed items checked
16. Run `bash validate_docs.sh` in the docs directory -- it must pass (exit 0)
17. Protocol file cross-references resolve (e.g., ADR-007 → silicon_based_agents.md)

If any check fails, fix the issue before reporting completion.

Report results using the Required Output Structure from SKILL.md (7 sections).
