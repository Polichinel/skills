---
name: review-base-docs
description: Audits existing architectural governance documentation (ADRs, CICs, protocols, standards) against the current codebase to detect drift, staleness, and gaps. Use when user says "review the docs", "audit documentation", "check ADR compliance", "are the docs up to date", "pre-PR documentation check", or "review base docs". Do NOT use for creating new documentation (use init-base-docs or adopt-base-docs), for code review (use expert-code-review), or for code refactoring (use tech-debt-cleanup).
---

# Review Base Documentation

## Important

Follow these rules strictly.

- Do not modify any documentation files. This skill audits and reports only.
- Do not modify any code files. Document drift, do not fix it.
- Ground every finding in specific file references (ADR file, CIC file, code file, line numbers where possible).
- Distinguish between critical issues (broken contracts, missing classes) and minor issues (stale dates, cosmetic inconsistencies).
- If validate_docs.sh exists in the docs directory, run it first.
- Propose specific remediation for each finding (what to update, add, or supersede).
- Audit all document types: ADRs, CICs, contributor protocols, and standards.

## Critical Constraint

This skill is read-only. It produces a report. It does not create, modify, or delete any files. All proposed changes are recommendations for the user to act on.

## Purpose

Audit existing governance documentation against the current codebase to detect documentation drift, contract violations, stale reviews, undocumented APIs, and governance gaps. Surface these systematically so the user can address them before a PR or checkpoint.

## Procedure

Execute these 6 phases sequentially. For detailed instructions, consult `references/phases.md`.

1. **Locate Documentation** -- Find and validate the existing docs directory
2. **Automated Checks** -- Run validate_docs.sh and extended integrity checks
3. **ADR Audit** -- Check each ADR's claims against current code
4. **CIC Audit** -- Check each CIC against its actual class implementation
5. **Gap Analysis** -- Identify undocumented classes, missing ADRs, governance holes
6. **Report** -- Structured output with findings and proposed remediations

## Required Output Structure

1. Automated Check Results (validate_docs.sh output + extended checks)
2. ADR Audit Findings (per-ADR: status, drift detected, proposed action)
3. CIC Audit Findings (per-CIC: status, drift detected, undocumented methods, proposed action)
4. Protocol and Standards Audit (per-document: still accurate? tooling/patterns changed?)
5. Gap Analysis (undocumented classes, missing 010+ ADRs, governance holes)
6. Proposed Remediations (prioritized action list: critical to minor)
7. Documentation Health Summary (overall assessment, trends, recommendations)

## Severity Levels

- **Critical:** Broken contracts (CIC references deleted class), dangling cross-references, Active docs for removed code
- **High:** Significant drift (new public methods not in CIC, ADR pattern no longer followed in code)
- **Medium:** Stale reviews (CIC not updated after significant code changes), missing CICs for non-trivial classes
- **Low:** Cosmetic issues (unfilled optional fields, formatting inconsistencies, date staleness)

## Performance Notes

- Run validate_docs.sh first -- it catches mechanical issues quickly.
- Focus CIC audit on public API surface (methods, signatures, documented behaviors).
- For ADR audit, check the Decision and Implementation Notes sections against actual code.
- Do not attempt to audit every line of code. Focus on what the docs claim.
- If the docs directory is large, prioritize: CICs first (most likely to drift), then constitutional ADRs, then project-specific ADRs, then protocols and standards.
