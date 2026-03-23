# Init Base Docs: Detailed Phase Instructions

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

## Phase 2 -- Gather Project Identity

Collect the following information. If the user provided any of these in their invocation, do not re-ask.

**Required:**
- Project name (used in ADR titles and references)
- One-sentence purpose (used to ground Context sections)
- Which constitutional ADRs to include (gathered in Phase 3)

**Optional (with defaults):**
- Domain vocabulary or metaphor family (default: neutral/generic, marked provisional in ADR-001)
- Intended architectural layers or entity categories (default: left as provisional in ADR-001)
- Docs directory name (default: `docs/`)
- Organization style: flat or lifecycle folders (default: flat)
- Deciders field value (default: "Project maintainers")
- Numbering scheme: preserve 000-009 or custom (default: preserve)

If the target repo has existing code, do a lightweight scan (`ls` of top-level and `src/`) to inform the ontology conversation. Do not run a full repo-assimilation.

---

## Phase 3 -- Select Constitutional ADRs

Present the following table and ask which to include. Default is all.

| ADR | Title | Role |
|-----|-------|------|
| 000 | Use of ADRs | Meta-governance (always recommended) |
| 001 | Ontology of the Repository | Defines what exists (always recommended) |
| 002 | Topology and Dependency Rules | Defines structural direction |
| 003 | Authority of Declarations Over Inference | Defines semantic authority |
| 004 | Rules for Evolution and Stability | Deferred placeholder |
| 005 | Testing as Mandatory Critical Infrastructure | Testing doctrine (red/beige/green) |
| 006 | Intent Contracts for Non-Trivial Classes | CIC governance |
| 007 | Silicon-Based Agents as Untrusted Contributors | AI contributor governance |
| 008 | Observability and Explicit Failure | Fail-loud + logging requirements |
| 009 | Boundary Contracts and Configuration Validation | Interface contracts |

If the user excludes ADR-000 or ADR-001, warn that these are foundational and ask to confirm.

If the user excludes ADR-006, note that CIC infrastructure will still be created but governance will reference a non-existent ADR -- ask whether to skip CIC setup entirely.

---

## Phase 4 -- Adapt ADRs

For each selected ADR, read the template from base_docs and apply these transformations:

### Metadata
- Status: `--template--` → `Accepted`
- Date: set to today
- Deciders: from Phase 2

### Title
Include the project name where natural. Examples:
- "Ontology of the Repository" → "Ontology of [ProjectName]"
- "Topology and Dependency Rules" → keep as-is if project name adds nothing

### Context section
Replace the generic motivation with project-domain-specific motivation. Keep the same philosophical thrust but ground it in why THIS project needs this rule. Reference the project's purpose from Phase 2.

### Core sections
Populate template placeholders with project-specific content:
- ADR-001 "Core Ontological Categories": draft categories based on the user's stated architectural layers and domain vocabulary. Present as a table (Category / Purpose / Authority / Stability) to the user for confirmation before proceeding.
- ADR-003: replace generic forbidden-inference examples with domain-relevant ones
- ADR-005: adjust test taxonomy examples to the project's likely concerns
- ADR-009: ground boundary examples in the project's intended architecture

### Cross-references
Ensure all ADR-to-ADR references point to ADRs that are included. If a referenced ADR was excluded, note the exclusion explicitly (e.g., "See ADR-006 [not included in this repository]").

### ADR-004
Keep Status as `Deferred`. Do not adapt content. This is intentional -- evolution and stability rules are premature for greenfield.

### Preservation rules
- Never drop a section from the template
- Never add sections that don't exist in the template
- Preserve the philosophical language and tone
- Keep Consequences sections honest (positive AND negative)

---

## Phase 5 -- Set Up CIC Infrastructure

### cic_template.md
Copy verbatim from base_docs. Do not modify the template.

### CICs/README.md
Adapt from base_docs:
- Update ADR cross-references to match actual ADR numbers included
- Replace the "Active Contracts" example entries with:
  ```
  ## Active Contracts

  No contracts yet. Create intent contracts as non-trivial classes emerge.
  ```
- If the user provided intended entity categories in Phase 2, optionally add a note suggesting which categories will likely need CICs first

---

## Phase 6 -- Set Up Contributor Protocols

### Always include:
- **carbon_based_agents.md** -- Copy from base_docs. Adapt team/role references to match the project's context. If the project has no team yet (solo greenfield), keep the protocol but note it applies when contributors join.
- **silicon_based_agents.md** -- Copy from base_docs. Adapt tooling references to match the project's AI tools (e.g., Claude Code, GitHub Copilot). Verify that ADR-007 cross-references are correct.

### Ask about:
- **hardened_protocol_template.md** -- This is domain-specific (ML/reproducibility-critical systems). Present it to the user and ask: "Does this project involve ML, numerical computation, or reproducibility-critical workloads?" If yes, include and adapt. If no, skip.

---

## Phase 7 -- Set Up Standards

### Always include:
- **logging_and_observability_standard.md** -- Copy from base_docs. Adapt scope expectations to the project's domain. Verify ADR-008 cross-references are correct.

### Ask about:
- **physical_architecture_standard.md** -- This enforces the 1-class-1-file rule and a specific directory ontology. Present it to the user and ask: "Does this project follow a 1-class-1-file convention?" If yes, include and adapt directory ontology. If no, skip.

---

## Phase 8 -- Write Files

Create the full directory structure under the docs directory name from Phase 2.

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
│   ├── README.md           (adapted)
│   └── cic_template.md     (verbatim from base_docs)
├── contributor_protocols/
│   ├── carbon_based_agents.md  (adapted)
│   ├── silicon_based_agents.md (adapted)
│   └── hardened_protocol_template.md (if selected)
├── standards/
│   ├── logging_and_observability_standard.md (adapted)
│   └── physical_architecture_standard.md    (if selected)
├── INSTANTIATION_CHECKLIST.md  (adapted, completed items checked)
└── validate_docs.sh            (verbatim from base_docs)
```

### Lifecycle organization (if requested):
```
<docs-dir>/
├── ADRs/
│   ├── active/             (adapted constitutional ADRs go here)
│   ├── proposed/           (empty)
│   ├── archive/            (empty)
│   ├── templates/          (adr_template.md from base_docs)
│   └── README.md           (adapted navigation)
├── CICs/
│   ├── README.md           (adapted)
│   └── cic_template.md     (verbatim from base_docs)
├── contributor_protocols/
│   ├── carbon_based_agents.md  (adapted)
│   ├── silicon_based_agents.md (adapted)
│   └── hardened_protocol_template.md (if selected)
├── standards/
│   ├── logging_and_observability_standard.md (adapted)
│   └── physical_architecture_standard.md    (if selected)
├── INSTANTIATION_CHECKLIST.md  (adapted, completed items checked)
└── validate_docs.sh            (verbatim from base_docs)
```

### ADRs/README.md adaptation
- List only the ADRs that were actually created
- Update one-line descriptions to reflect adapted titles
- Keep the Governance Structure section, removing references to excluded ADRs
- Update the Project-Specific ADRs section to say: "No project-specific ADRs yet. Create ADRs numbered 010+ as architectural decisions arise."

### INSTANTIATION_CHECKLIST.md
Copy from base_docs. Check off items that the skill has completed. Leave unchecked items that were skipped or deferred.

### validate_docs.sh
Copy verbatim from base_docs. Do not modify.

---

## Phase 9 -- Verify Coherence

Run through the quality checklist from SKILL.md. For each item:

1. All selected ADRs have Status `Accepted` (except ADR-004 which is `Deferred`)
2. All ADRs have today's date and the deciders value
3. ADR-001 ontology categories match what the user confirmed
4. Every ADR cross-reference (e.g., "see ADR-003") points to an ADR that exists in the directory
5. CIC README references only ADRs that exist
6. ADR README navigation lists exactly the files that were created
7. ADR-004 is deferred (not accidentally adapted)
8. `adr_template.md` and `cic_template.md` are unmodified copies of the originals
9. contributor_protocols/ contains the selected protocol files
10. standards/ contains the selected standard files
11. INSTANTIATION_CHECKLIST.md is present with completed items checked
12. Run `bash validate_docs.sh` in the docs directory -- it must pass (exit 0)
13. Protocol file cross-references resolve (e.g., ADR-007 → silicon_based_agents.md)

If any check fails, fix the issue before reporting completion.

Report the results using the Required Output Structure from SKILL.md.
