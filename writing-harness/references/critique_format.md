# Critique Format Reference

Persona critiques are written in the persona's natural voice. The body is a professional letter-style critique organized by section or by finding. At the end, a machine-parseable Findings Summary table extracts actionable items for transfer to FINDINGS.md.

## File Naming

```
critiques/<lens>_<NN>.md
```

Where `<lens>` is the persona's failure-mode sensitivity (e.g., `craft`, `substance`, `utility`, or document-specific like `fao_counterpart`, `peer_reviewer`). `<NN>` is a zero-padded round number starting at 00.

## Header Format

```markdown
# [Persona Name] Critique: "[Document Title]"

**[Persona name]**, [role description]
**Date:** [YYYY-MM-DD]
**Round:** [NN]
**Lens:** [craft / substance / utility / other]
**Failure modes watched:** [list of FM-XX from catalog, if applicable]
```

## Body

The critique body follows the persona's natural voice. Organize by section or by finding type, whichever reads more naturally for the persona. The critique should be a readable document, not a checklist.

## Findings Summary (required, at the end)

```markdown
## Findings Summary

| # | Section | Finding | Severity | FM-XX | FINDINGS.md |
|---|---------|---------|----------|-------|-------------|
| 1 | §2      | [short description] | Substantive | FM-16 | F-XX or "pending extraction" |
| 2 | §3      | [short description] | Editorial | -- | pending extraction |
```

**Column definitions:**
- **#**: Sequential within this critique
- **Section**: Where in the document
- **Finding**: One-line description (the full finding is in the critique body)
- **Severity**: Critical / Substantive / Editorial
- **FM-XX**: If this maps to a known failure mode, tag it. This connects scouts (personas) to sentries (catalog). If the same FM-XX appears across multiple critiques, it's evidence for graduation.
- **FINDINGS.md**: The F-XX entry once extracted, or "pending extraction" if not yet transferred

## Persona Design Notes

Three guaranteed coverage zones, each sensitive to a different failure class:
- **Craft**: register contamination, structural overlap, weak transitions, rhythm
- **Substance**: claims outrunning evidence, analogies concealing disanalogies, intellectual overreach
- **Utility**: no ask, no deliverables, wrong institutional language, credibility gaps, missing reader context

The persona most unlike the AI's default voice (typically the institutional counterpart) tends to produce the most consequential findings. Deploy personas in parallel as separate agents, not sequentially in one context.

Personas should either find problems or say nothing. Never validate. (See FM-23.)
