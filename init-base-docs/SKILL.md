---
name: init-base-docs
description: Initializes architectural governance documentation (ADRs + CIC infrastructure) for a new greenfield project by adapting constitutional templates from base_docs to the project's domain and intended architecture. Use when user says "initialize docs", "set up ADRs", "bootstrap documentation", "init base docs", "create documentation foundation", or "set up governance docs". Do NOT use for existing projects that already have ADRs (use review-base-docs), for brownfield projects without docs (use adopt-base-docs), for writing project-specific ADRs (010+), or for code scaffolding (use init-repo).
---

# Initialize Base Documentation

## Important

Follow these rules strictly.

- Do not write project-specific ADRs (010+). This skill only handles constitutional ADRs (000-009).
- Do not create CICs for classes. Only set up CIC infrastructure (template + README).
- Do not run repo-assimilation. Greenfield projects have nothing to assimilate.
- Do not invent domain vocabulary the user has not provided or confirmed.
- If the user's intended architecture is vague, say so honestly in ADR-001 rather than fabricating specificity.
- Always preserve all mandatory sections from each ADR template. Never drop sections.
- ADR-004 must remain deferred unless the user explicitly requests otherwise.
- Present the adapted ADR-001 (Ontology) draft to the user for confirmation before writing files.

## Critical Constraint

Constitutional ADRs are philosophical and structural. They define HOW the project governs itself, not WHAT the project builds. When adapting, ground them in the project's domain but do not convert them into implementation specifications. The adaptation is semantic grounding, not specification writing.

## Purpose

Bootstrap a documentation governance foundation for a new project by adapting base_docs constitutional ADR templates and CIC infrastructure to the project's domain, vocabulary, and intended architecture.

For greenfield projects, the documentation is the first architectural declaration. It defines what the system intends to become.

## Procedure

Execute these 9 phases sequentially. For detailed instructions, consult `references/phases.md`.

1. **Locate Base Docs** -- Find and validate the base_docs template directory
2. **Gather Project Identity** -- Collect project name, purpose, domain, intended architecture, preferences
3. **Select Constitutional ADRs** -- Present 000-009 for selection (default: all)
4. **Adapt ADRs** -- Transform each selected template into a project-grounded document
5. **Set Up CIC Infrastructure** -- Create CIC directory with template and adapted README
6. **Set Up Contributor Protocols** -- Copy carbon + silicon protocols; ask about hardened template
7. **Set Up Standards** -- Copy logging standard; ask about physical architecture standard
8. **Write Files** -- Create directory structure, write all documents, include meta-tools
9. **Verify Coherence** -- Check cross-references, completeness, run validate_docs.sh

## Required Output Structure

1. Initialization Summary (what was created, where)
2. ADR Manifest (numbered list with one-line descriptions)
3. Adaptation Notes (what was customized, what remains provisional)
4. Next Steps (review ADR-001, future ADRs to consider, when to create CICs)

## Quality Checklist

Before reporting success, verify:

- All selected ADRs have Status set to Accepted (not --template--)
- All ADRs have dates and deciders filled in
- ADR-001 ontology categories reflect the project's domain
- All cross-references between ADRs point to ADRs that exist
- CIC README governance references match actual ADR numbers
- ADR README navigation matches actual files
- ADR-004 remains explicitly deferred
- Templates (adr_template.md, cic_template.md) are present and unmodified
- contributor_protocols/ contains carbon_based_agents.md and silicon_based_agents.md (+ hardened if selected)
- standards/ contains logging_and_observability_standard.md (+ physical_architecture_standard.md if selected)
- INSTANTIATION_CHECKLIST.md is present with completed items checked off
- validate_docs.sh is present and passes when run

## Performance Notes

- Phase 2 (Gather Project Identity) is the most important. Spend time here.
- ADR-001 adaptation is the highest-value creative work. Get it right.
- If the user provides minimal information, prefer honest vagueness over fabricated detail.
- This is philosophically consistent with ADR-003: declare, do not infer.
