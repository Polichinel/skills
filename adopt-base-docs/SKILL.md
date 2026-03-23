---
name: adopt-base-docs
description: Retrofits architectural governance documentation (ADRs + CICs) onto an existing project by consuming repo-assimilation output and adapting constitutional templates from base_docs to match what the code actually does. Use when user says "adopt base docs", "add ADRs to this project", "retrofit documentation", "document this architecture", "add governance docs", or "adopt documentation framework". Do NOT use for new/empty projects (use init-base-docs), for projects that already have ADRs (use review-base-docs), or for code refactoring (use tech-debt-cleanup).
---

# Adopt Base Documentation

## Important

Follow these rules strictly.

- Do not write project-specific ADRs (010+). Only constitutional ADRs (000-009), but suggest 010+ candidates in the output.
- Do not refactor or modify existing code. Document what exists, even if imperfect.
- Do not fabricate architectural details. If something is unclear from the code, state the ambiguity.
- Always preserve all mandatory sections from each ADR template. Never drop sections.
- Present the ontology mapping (code entities to categories) to the user for confirmation before writing.
- Present the CIC candidate list to the user for confirmation before writing.
- Require repo-assimilation output as a prerequisite. If unavailable, stop and tell the user to run repo-assimilation first.
- Include a "Known Deviations" section in CICs where code does not match ideal patterns.
- Write CICs for all confirmed non-trivial classes, not just a subset.

## Critical Constraint

Brownfield documentation must describe what IS, not what should be. ADRs codify existing architectural decisions. CICs describe actual class behavior. Aspirational improvements belong in "Open Questions" or "Evolution Notes" sections, not in the core declarations.

Honesty over elegance. If the architecture is messy, the docs should say so.

## Purpose

Retrofit a documentation governance foundation onto an existing project by consuming its repo-assimilation output and adapting base_docs constitutional ADR templates and CIC templates to accurately describe the codebase as it exists.

## Procedure

Execute these 11 phases sequentially. For detailed instructions, consult `references/phases.md`.

1. **Locate Base Docs** -- Find and validate the base_docs template directory
2. **Consume Assimilation** -- Load and validate prior repo-assimilation output (required)
3. **Gather Project Identity** -- Collect project name, purpose, confirm domain vocabulary
4. **Map Ontology** -- Map actual code entities to ontological categories, present for confirmation
5. **Select Constitutional ADRs** -- Present 000-009 for selection (default: all)
6. **Adapt ADRs** -- Transform templates grounded in actual code structure
7. **Write CICs** -- Create intent contracts for all confirmed non-trivial classes
8. **Set Up Contributor Protocols** -- Copy carbon + silicon protocols (grounded in project tooling); ask about hardened template
9. **Set Up Standards** -- Copy logging standard (grounded in project patterns); ask about physical architecture standard
10. **Write Files** -- Create directory structure, write all documents, include meta-tools
11. **Verify Coherence** -- Check docs match actual code, cross-references valid, run validate_docs.sh

## Required Output Structure

1. Discovery Summary (what was found in the codebase)
2. Ontology Mapping (code entities to categories, confirmed by user)
3. ADR Manifest (numbered list with one-line descriptions)
4. CIC Manifest (classes documented, with status)
5. Adaptation Notes (what was customized, what remains ambiguous)
6. Suggested Project-Specific ADRs (010+ candidates for future)
7. Next Steps (review priority, missing CICs, evolution concerns)

## Quality Checklist

Before reporting success, verify:

- All ADRs reference actual code structure (not generic examples)
- ADR-001 ontology categories map to real classes and modules
- All CICs reference actual method names and test files
- CIC "Known Deviations" sections are honest about current state
- Cross-references between ADRs point to ADRs that exist
- CIC README lists all created CICs
- ADR README navigation matches actual files
- Templates (adr_template.md, cic_template.md) are present and unmodified
- contributor_protocols/ contains carbon + silicon protocols (+ hardened if selected), grounded in project tooling
- standards/ contains logging standard (+ physical architecture if selected), grounded in project patterns
- INSTANTIATION_CHECKLIST.md is present with completed items checked off
- validate_docs.sh is present and passes when run

## Performance Notes

- Phase 2 requires prior repo-assimilation output. Do not proceed without it.
- Phase 4 (Map Ontology) is the highest-value creative work. This is where code becomes governance.
- Write CICs for all confirmed non-trivial classes. Each CIC should reference actual methods, tests, and known deviations.
- Honest incompleteness is better than fabricated completeness.
