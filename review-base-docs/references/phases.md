# Review Base Docs: Detailed Phase Instructions

## Phase 1 -- Locate Documentation

Find the project's documentation directory. Check common locations:
- `docs/`
- `documentation/`
- Ask the user if neither exists.

Validate the directory contains at least:
- `ADRs/` with one or more ADR files
- Optionally: `CICs/`, `contributor_protocols/`, `standards/`

Inventory what exists:
- Count ADR files (constitutional 000-009 and project-specific 010+)
- Count CIC files
- List contributor protocols present
- List standards present
- Check for `validate_docs.sh` and `INSTANTIATION_CHECKLIST.md`

If the directory has no ADRs at all, stop and suggest running init-base-docs or adopt-base-docs first.

---

## Phase 2 -- Automated Checks

### 2a. Run validate_docs.sh (if present)
Execute the script and capture output. Report:
- Pass/fail status
- Any errors found (dangling references, unfilled placeholders, missing CIC files)
- Any warnings

### 2b. Extended integrity checks (beyond what the script covers)

**Cross-reference integrity:**
- For every `ADR-NNN` citation in any markdown file, verify the referenced ADR file exists
- For every CIC listed in `CICs/README.md`, verify the CIC file exists
- For every `contributor_protocols/*.md` reference, verify the file exists
- For every `standards/*.md` reference, verify the file exists

**Status coherence:**
- List all ADRs with their status (Accepted, Proposed, Superseded, Deprecated, Deferred)
- Flag Superseded ADRs that are still cross-referenced from Active/Accepted documents without noting the supersession
- Flag Active CICs whose "Related ADRs" reference Superseded or Deprecated ADRs

**Metadata completeness:**
- Check all ADRs have Status, Date, and Deciders filled (not template placeholders)
- Check all CICs have Status, Owner, Last reviewed, and Related ADRs filled
- Flag any Active/Accepted documents with YYYY-MM-DD dates or <placeholder> values

Report all findings with severity levels.

---

## Phase 3 -- ADR Audit

For each ADR, check its claims against the current codebase.

### Constitutional ADRs (000-009)

For each accepted constitutional ADR:

**ADR-001 (Ontology):** Do the declared ontological categories still match the codebase?
- Are all listed entity categories still represented in code?
- Are there new classes/modules that don't fit any declared category?
- Have any categories been effectively abandoned (no code implements them)?

**ADR-002 (Topology):** Do declared dependency rules still hold?
- Check actual imports against stated allowed/forbidden dependencies
- Flag any circular dependencies the ADR forbids

**ADR-003 (Authority):** Is the fail-loud/no-inference principle honored?
- Grep for patterns that infer semantics (e.g., deriving meaning from naming conventions)
- Check for silent fallbacks where the ADR demands explicit failure

**ADR-005 (Testing):** Does the test structure match the declared doctrine?
- Do red/beige/green test categories exist as described?
- Are there test files not covered by the taxonomy?

**ADR-007 (Silicon Agents):** Is the silicon agent protocol being followed?
- Check if contributor_protocols/silicon_based_agents.md is referenced and up to date

**ADR-008 (Observability):** Are logging/failure patterns followed?
- Check for silent exception swallowing (catch without raise/log)
- Verify logging standard is referenced if present

**ADR-009 (Boundary Contracts):** Are boundary validations in place?
- Check module entry points for validation patterns described in the ADR

### Project-specific ADRs (010+)

For each project-specific ADR:
- Read the Decision and Implementation Notes sections
- Check if the described pattern still exists in code
- Flag if the code has diverged significantly from what the ADR describes
- Suggest Superseded status if the pattern has been replaced

### Output per ADR:

| ADR | Status | Drift? | Severity | Finding | Proposed Action |
|-----|--------|--------|----------|---------|-----------------|

---

## Phase 4 -- CIC Audit

For each CIC file in the CICs directory:

### 4a. Class existence check
- Does the class still exist in the codebase?
- Has it been renamed? (search for similar names)
- If deleted: flag as Critical, propose archiving the CIC

### 4b. Public API drift
- List all public methods in the actual class
- List all methods documented in the CIC (sections 3, 8, 9)
- Flag methods in code but not in CIC as **undocumented** (High severity)
- Flag methods in CIC but not in code as **stale** (Critical severity)

### 4c. Contract accuracy
- **Purpose (section 1):** Still accurate?
- **Non-Goals (section 2):** Any non-goals the class now violates?
- **Inputs and Assumptions (section 4):** Do constructor parameters match?
- **Failure Modes (section 6):** Does the class still fail as documented?
- **Boundaries (section 7):** Does it still interact with only the documented components?

### 4d. Test alignment
- Do the test files referenced in section 10 still exist?
- Are there new test files for this class not mentioned in the CIC?

### 4e. Known Deviations check (if section 12 exists)
- Have any documented deviations been resolved? (update needed)
- Are there new deviations not yet documented?

### 4f. Freshness
- Compare CIC "Last reviewed" date against recent git commits touching the class file
- If the class was significantly modified after the CIC's last review date, flag as Medium severity

### Output per CIC:

| CIC | Class Exists? | Undocumented Methods | Stale Methods | Contract Drift | Severity | Proposed Action |
|-----|--------------|---------------------|---------------|---------------|----------|-----------------|

---

## Phase 5 -- Gap Analysis

### 5a. Undocumented non-trivial classes
Scan the codebase for classes that:
- Are non-trivial (not simple data classes or pure utilities)
- Do NOT have a CIC

A class is non-trivial if it:
- Has more than 3 public methods
- Sits at a module boundary (imports from/exported to multiple modules)
- Orchestrates other components
- Manages state
- Enforces invariants

List undocumented non-trivial classes with their file locations and suggest CIC creation.

### 5b. Missing project-specific ADRs
Identify architectural patterns in the code that are not documented by any ADR:
- Design patterns used consistently (strategy, factory, observer, etc.)
- Data flow patterns (pipeline stages, ETL, pub-sub)
- Configuration management approaches
- Deployment or infrastructure patterns
- Error handling conventions beyond what ADR-008 covers

Suggest 010+ ADR candidates for each.

### 5c. Protocol and standards drift
For each contributor protocol:
- Does it reference tooling/CI that still exists?
- Are the allowed/forbidden operations still relevant?
- Does the silicon agent protocol match actual AI tool usage?

For each standard:
- Does the logging standard match actual logging patterns?
- Does the physical architecture standard match actual directory structure?
- Are there standards that should exist but don't?

### 5d. Governance holes
Check for systemic gaps:
- ADRs that reference CICs but no CICs exist
- CICs that reference ADRs that don't exist
- Contributor protocols that reference outdated tooling
- Missing governance for entire subsystems

---

## Phase 6 -- Report

Compile all findings into the Required Output Structure from SKILL.md (7 sections).

### Prioritized remediation list

Order all findings by severity, then by effort:

| Priority | Severity | Document | Finding | Remediation | Effort |
|----------|----------|----------|---------|-------------|--------|
| 1 | Critical | ... | ... | ... | small/medium/large |
| 2 | High | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

### Documentation Health Summary

Provide an overall assessment:
- Total documents audited (ADRs, CICs, protocols, standards)
- Issues found by severity (critical/high/medium/low counts)
- Overall health rating (healthy / needs attention / significant drift / critical issues)
- Top 3 recommended actions
- Trend assessment (if this is a repeat review: improving, stable, or degrading)
