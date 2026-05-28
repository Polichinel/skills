---
name: verify-sources
description: Verifies every citation in a document against local source PDFs. Checks that claims about cited works are accurate, flags missing PDFs, and maintains a citation ledger in the writing harness. Use when user says "verify sources", "check citations", "verify references", or "source check". Operates on documents with an active writing harness.
---

# Verify Sources

## Important

Follow these rules strictly.

- Do not modify the draft. This skill verifies only.
- Every citation must have a local PDF. Flag any `\cite{}` key without a resolvable PDF path as an immediate Critical finding. The only exception is online-only resources (codebooks, datasets) where the user explicitly confirms no PDF exists.
- Do not fabricate source content. If a PDF is unreadable or ambiguous, say so. Never guess what a paper says.
- Ground every verdict in a direct quote or page reference from the source PDF.
- On repeat invocations, check the citation ledger first. Only re-read PDFs for new citations, changed claim text, or when explicitly asked to re-verify.
- Produce FINDINGS.md entries for IMPRECISE and WRONG verdicts. ACCURATE verdicts are recorded in the citation ledger only.

## Purpose

Verify that every citation in a document faithfully represents what the cited source actually says. This is the external accuracy layer — complementary to persona-critique (which checks internal quality) and falsify (which checks internal consistency). It reads source PDFs from the local library and compares them against the claims the document makes about each cited work.

The failure mode this skill catches: mischaracterization of cited work. This is invisible to internal QA because the draft can be internally consistent while misrepresenting external sources. The base rate for this failure mode is high enough to warrant systematic checking.

## Harness Integration

This skill operates on documents with an active writing harness (detected by `_dev_materials/*/DECISIONS.md`). It reads from and writes to a `citations/` directory within the harness:

```
_dev_materials/<document_slug>/
├── citations/              # This skill's working directory
│   ├── CITATION_LEDGER.md  # Master index of all citations with verdicts
│   └── <citation_key>.md   # Per-citation verification record
```

The writing-harness skill creates the `citations/` directory. If it doesn't exist, create it.

## Procedure

### Phase 1: Extract Citation Inventory

1. Locate the document source files (LaTeX, Markdown, etc.)
2. Parse all citation commands (`\cite{}`, `\citep{}`, `\citet{}`, `\autocite{}`, etc.)
3. For each unique citation key, collect every claim the document makes about it — the exact text, the section, and the line number
4. Build a citation inventory table: key, claim count, PDF status

### Phase 2: Library Check

For each citation key:
1. Check the bibliography file (`.bib`) for the entry — extract title, authors, year
2. Search for the PDF in the local library. Standard search paths:
   - `lit/` and subdirectories within the project
   - `~/brain/9_library/papers/` and subdirectories
   - `~/brain/9_library/new_temp/`
   - `~/Downloads/` (last resort)
3. If no PDF is found: **immediate Critical finding.** Report to user. Do not proceed with verification for that citation unless the user provides a path or confirms it's an online-only resource.

### Phase 3: Check Citation Ledger

If `citations/CITATION_LEDGER.md` exists:
1. Load all existing citation records
2. For each citation in the current inventory:
   - If the citation key exists in the ledger AND the claim text hasn't changed: skip (already verified)
   - If the citation key exists but claims have changed: mark for re-verification
   - If the citation key is new: mark for first verification
3. Report: "X citations cached, Y new, Z changed — verifying Y+Z"

If no ledger exists, all citations are marked for first verification.

### Phase 4: Triage

Classify each citation to be verified into tiers (following the pattern from the source verification audit):

- **TIER 1 — Substantive technical claims**: Papers where the document describes what they propose, prove, or find. Wrong claim = reviewer rejection.
- **TIER 2 — General claims**: Papers cited for broad characterization. Spot-check suffices.
- **TIER 3 — Attribution-only**: Papers cited as foundational or contextual references with no substantive claim beyond "this exists." Skip unless user requests.

Present the triage to the user. Proceed after confirmation (or immediately if the user invoked with `--all`).

### Phase 5: Read and Verify

For each citation marked for verification:

1. Read the source PDF — abstract, introduction, and sections relevant to the claims being verified. For TIER 1 citations, read thoroughly. For TIER 2, spot-check.
2. For each claim the document makes about this source:
   - Extract what the source ACTUALLY says (with page number and direct quote)
   - Compare against the document's claim
   - Assign verdict: **ACCURATE** / **IMPRECISE** / **WRONG**
3. If IMPRECISE: explain what's imprecise and what the source actually says
4. If WRONG: explain what's wrong, what the source actually says, and suggest corrected text

Token discipline: for large PDFs, read targeted sections rather than the entire document. Use the table of contents, abstract, and section headings to navigate to relevant content.

### Phase 6: Write Citation Records

For each verified citation, write a record file to `citations/<citation_key>.md`:

```markdown
---
key: <citation_key>
title: "<full title>"
authors: "<author list>"
year: <year>
pdf_path: "<path to local PDF>"
verified: <YYYY-MM-DD>
verdict: <ACCURATE | IMPRECISE | WRONG>
---

## Claims in Document

### Claim 1
- **Location:** §N, line M
- **Our text:** "<exact text from document>"
- **Source says:** "<relevant quote from source, p.XX>"
- **Verdict:** ACCURATE / IMPRECISE / WRONG
- **Note:** [if IMPRECISE/WRONG: explanation]

### Claim 2
[...]
```

Update `citations/CITATION_LEDGER.md` with a summary line per citation.

### Phase 7: Report and Findings

1. **Summary table**: citation key, tier, # claims, verdict, action needed
2. **For each WRONG verdict**: create a FINDINGS.md entry (Critical severity)
3. **For each IMPRECISE verdict**: create a FINDINGS.md entry (Substantive severity)
4. **Library compliance**: list any citations without local PDFs
5. **Bibliography check**: flag any obvious bib entry errors (wrong year, wrong title, wrong author order) discovered during PDF reading

Present the full report to the user.

## Citation Ledger Format

`citations/CITATION_LEDGER.md`:

```markdown
# Citation Ledger

| Key | Title (short) | Tier | Claims | Verdict | Verified | PDF |
|-----|---------------|------|--------|---------|----------|-----|
| bessac2021forecast | Bessac & Naveau (2021) | 1 | 5 | ACCURATE | 2026-05-07 | ~/brain/9_library/new_temp/Bessac2021_... |
| lerch2017forecasters | Lerch et al. (2017) | 1 | 2 | IMPRECISE | 2026-05-07 | lit/scoring_rules/Lerch-... |
```
## Invocation

```
/verify-sources                    # verify all unverified citations
/verify-sources --all              # re-verify everything, ignore cache
/verify-sources --new              # verify only citations not in ledger
/verify-sources <key> <key>        # verify specific citation keys
```

## Integration with Other Skills

- **persona-critique**: If `\cite{}` commands exist in the draft but no `citations/CITATION_LEDGER.md` exists, persona-critique should note in its summary: "Source verification has not been run. Consider `/verify-sources`."
- **writing-harness**: Creates the `citations/` directory during harness initialization.
- **falsify**: Can use citation records as evidence when auditing claims about external sources.

## Performance Notes

- First run on a paper with 15-20 citations is expensive (reading many PDFs). Budget accordingly.
- Subsequent runs are cheap — the ledger cache means only new/changed citations trigger PDF reads.
- TIER 1 verification is thorough and slow. TIER 2 is fast. TIER 3 is skipped. The triage step controls cost.
- When reading PDFs, extract and quote relevant passages generously. Future runs check the cache, not the PDF — the quotes need to be sufficient for re-evaluation.
- The most common failure mode is not "wrong" but "imprecise" — directionally correct claims that overstate, understate, or use slightly wrong terminology. These are worth catching because reviewers who know the cited work will notice.
