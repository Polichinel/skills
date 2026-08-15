# ADR-001: The Technical Risk Register is a First-Class Governance Artifact

| Field | Value |
|-------|-------|
| Status | Active |
| Date | 2026-08-15 |
| Deciders | Polichinl (simmaa@prio.org) |
| Supersedes | — |
| Superseded by | — |

## Context

This repository holds 24 Claude Code skills — Markdown instruction files with YAML frontmatter — that impose phase-structured protocols on software governance, strategic writing, research methodology, and cross-repo deliberation. Several of those skills are audit skills: `repo-assimilation`, `expert-code-review`, `test-review`, `falsify`, `review-diff`, and `tech-debt-cleanup` all produce findings that may warrant tracking beyond the conversation in which they were found.

Before this decision there was nowhere for such findings to go. A `repo-assimilation` run of this repository on 2026-08-15 produced nine structural risks, three of which describe invariants that are *already violated* and that survived nine commits undetected — a broken external template path, three references to skills that do not exist, and the complete absence of validation infrastructure. Findings of that kind decay quickly: the conversation ends, the analysis is lost, and the same defect is rediscovered later at full cost.

The repository is also the source of the `register-risk` and `review-rr` skills, which define the register format that other projects are expected to adopt. Operating those skills against every project *except* this one leaves the format untested by its own author and the repository's own risks untracked.

## Decision

The technical risk register at `reports/technical_risk_register.md` is a first-class governance artifact of this repository, on the same footing as the skills themselves.

1. **Single intake path.** All risks enter the register through `/register-risk`. Audit skills emit register-compatible findings and hand off; they do not append directly. This preserves the deduplication check, tier validation, and trigger-quality gate that `register-risk` exists to enforce.
2. **Permanent IDs.** `C-xx` for concerns, `D-xx` for disagreements, sequential within each prefix, never reused. Gaps are expected and informative — they mark merges and resolutions.
3. **Four tiers.** Tier 1 (silent corruption or output incorrectness, no error signal), Tier 2 (structural fragility with a concrete trigger), Tier 3 (maintainability and coupling, multi-developer scope), Tier 4 (localized quality observations). Tier 1 and Tier 2 require explicit justification in the narrative.
4. **Every concern carries an actionable trigger.** A trigger names a specific future developer action and what to check when it happens. Perpetual conditions ("any change to this module"), vague conditions, and consequences stated as triggers are rejected at intake.
5. **Every concern is grounded.** Narratives cite specific files and line numbers. A finding that cannot be located in the repository does not get registered.
6. **The register is version-controlled.** `reports/` is not gitignored in this repository, so ordinary staging applies; no `git add -f` is required here.
7. **Curation is a separate activity.** `/review-rr` owns triage, causal clustering, re-tiering, and prioritization. `register-risk` is intake only and does not re-analyze.

## Consequences

**Positive.** Audit findings survive the conversation that produced them. Tier assignments accumulate a comparison set, so consistency becomes checkable rather than aspirational. Cross-references make causal structure explicit — the initial nine entries already show one root cause (C-03, no validation infrastructure) generating three symptoms (C-01, C-04, C-05), which is actionable in a way nine flat findings would not be. The repository now exercises its own `register-risk`/`review-rr` format, which is the only way format defects surface before other projects inherit them.

**Negative.** Header counts are maintained by hand and will drift if an entry is added without updating them. The register is prose in a Markdown file with no schema validation — the same gap C-03 records for the repository at large, now applying to this artifact too. Nothing yet enforces that a resolved concern is actually moved to the Resolved section.

**Neutral.** This ADR takes number 001 because the repository had no prior ADRs and no `docs/` tree. The `base_docs` convention that `init-base-docs` implements reserves 001–009 for constitutional ADRs; that convention is not installed here, and cannot currently be applied because the template path it depends on is broken (registered as C-01). If `base_docs` governance is later adopted for this repository, this ADR should be renumbered to fit that scheme.

## Compliance

- New risks: invoke `/register-risk`; do not hand-edit the register.
- Review cadence: `/review-rr triage` after any bulk registration, `/review-rr strategic` when tier calibration is in question, `/review-rr prioritize` before planning work.
- Resolution: move the entry to "Resolved Concerns" with a date and a one-to-two sentence summary of what was done, and update the header counts.
