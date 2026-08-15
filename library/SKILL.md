---
name: library
description: Claim-centric research library for managing papers, extracting claims, verifying citations, and semantic search. Use when user says "/library" followed by a command (status, cite, search, find, rebuild, audit, verify, add).
trigger: /library
---

# Library

## Important

Follow these rules strictly.

- Never modify claim files, metadata files, or index databases directly. All mutations go through `src/library.py` functions.
- Never skip HITL review steps. When extracting claims (`/library add`) or verifying (`/library verify`), always present results and wait for user confirmation before finalizing.
- Always run commands from the `library_system` directory: `cd /home/simon/brain/9_library/library_system`
- Always use `.venv/bin/python` to run Python commands.
- When presenting results, put the most important information first. Evidence and metadata come after.

## Working Directory

All Python commands must run from:
```
/home/simon/brain/9_library/library_system
```

The library root (where papers live) is:
```
/home/simon/brain/9_library
```

## Activation

When the user invokes `/library` without a command, load context and present status:

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import context_block, get_config
config = get_config()
print(context_block(config))
"
```

Present the output and list available commands.

## Commands

### `/library status`

Show library statistics.

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import status, get_config
config = get_config()
result = status(config)
print(json.dumps(result, indent=2))
"
```

Present as a clean summary:
- Paper count, claim count, relation count
- Extraction coverage percentage
- Whether the search index exists
- Recent additions (last 10)

### `/library cite <paper_id>`

Generate a BibTeX citation.

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
from src.library import cite, get_config
config = get_config()
print(cite('PAPER_ID', config))
"
```

Output the BibTeX entry in a code block.

### `/library search <query>`

Semantic search across all indexed content.

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import library_search, get_config
config = get_config()
results = library_search('QUERY', config, k=K)
print(json.dumps(results, indent=2))
"
```

Default k=20. Present results as a ranked list with:
- Score and retrieval method
- Text snippet
- Source paper
- Provenance level

Note: First search in a session loads the embedding model (~30-60 seconds).

### `/library find <claim_text>`

Find supporting or contradicting claims for a specific assertion.

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import find, get_config
config = get_config()
results = find('CLAIM_TEXT', config, k=K)
print(json.dumps(results, indent=2))
"
```

Like search but restricted to claims with graph expansion. Present results emphasizing:
- Whether claims support or contradict the query
- Provenance level and source paper
- Relation paths if any

### `/library rebuild`

Rebuild the search index from all metadata and claims.

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import library_rebuild, get_config
config = get_config()
result = library_rebuild(config)
print(json.dumps(result, indent=2))
"
```

This loads the embedding model and processes all papers. Report:
- Papers, claims, relations, and chunks indexed
- Embeddings generated
- Duration
- Any errors

### `/library audit <paper_id>`

Deep audit of a single paper's claims and references.

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import audit, get_config
config = get_config()
result = audit('PAPER_ID', config)
print(json.dumps(result, indent=2))
"
```

Present:
- Paper metadata
- All extracted claims with provenance
- Incoming references from other papers' claims

### `/library verify <claim_text> [--paper <paper_id>]`

Verify a claim against its cited source. Two modes:

**Targeted mode** (paper_id provided): Verify against a specific paper.

**Scan mode** (no paper_id): Search for relevant papers and verify against top candidates.

#### Targeted Verification

This is a multi-step process. Claude acts as the LLM for verification.

**Step 1: Prepare evidence**

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import verify_prepare, get_config
config = get_config()
result = verify_prepare('CLAIM_TEXT', 'PAPER_ID', config)
print(json.dumps({
    'path_used': result['path_used'],
    'evidence_summary': result['evidence_summary'],
    'paper_title': result['paper_title'],
    'system_prompt': result['system_prompt'],
    'user_prompt': result['user_prompt'],
}, indent=2))
"
```

**Step 2: Read the system prompt and user prompt from the output. Produce a verification verdict.**

Read the evidence carefully. Use the `verification_result` tool schema to structure your verdict:

- `verdict`: one of `supported`, `partially_supported`, `not_supported`, `contradicted`, `insufficient_evidence`
- `evidence`: list of evidence passages with location, provenance_level, and relevance
- `drift_type` (optional): if the claim drifts from the source, classify as `scope_narrowing`, `qualification_dropping`, `conclusion_strengthening`, `context_shifting`, or `misattribution`
- `drift_explanation` (optional): explain the drift

**Step 3: Finalize with calibrated confidence**

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import verify_finalize, get_config
config = get_config()
raw_verdict = RAW_VERDICT_JSON
result = verify_finalize('CLAIM_TEXT', 'PAPER_ID', raw_verdict, 'PATH_USED', config)
print(json.dumps(result, indent=2))
"
```

Present the final result:
- Verdict with calibrated confidence
- Evidence passages
- Drift analysis if detected

#### Scan Mode

When no paper_id is provided:

1. Run `/library find` with the claim text
2. Identify the top 1-3 candidate source papers
3. Run targeted verification for each
4. Present comparative results

**Token cost estimate:** ~7-13K tokens per targeted verification. Scan mode multiplies by number of papers checked.

### `/library add <pdf_path>`

Add a new paper to the library. This is a multi-phase HITL workflow.

**Token cost estimate:** ~20-60K tokens depending on paper length.

#### Phase 1: Prepare

**Step 1a: Copy and rename the PDF.** Before calling `add_prepare`, the PDF must be in `papers/` with a convention-compliant name per ADR-019: `<FirstAuthorSurname><Year>_<ShortTitle>.pdf`. If the PDF is elsewhere (e.g., `incoming/`), copy it to `papers/` with the correct name first. Read the first page of the PDF to determine the correct author/year/title if needed.

Naming rules:
- `FirstAuthorSurname`: last name of first author, no accents, capitalized
- `Year`: four-digit publication year
- `ShortTitle`: 2-5 word descriptive title, CamelCase

Examples: `Gneiting2007_StrictlyProperScoringRules.pdf`, `Giacomini2006_TestsConditionalPredictiveAbility.pdf`

**Step 1b: Run add_prepare** with the correctly-named PDF in `papers/`.

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import add_prepare, get_config
config = get_config()
result = add_prepare('PDF_PATH', config)
print(json.dumps(result, indent=2))
"
```

Present to the user:
- Paper ID and metadata (title, authors, year)
- Whether metadata was found or generated
- Text length and estimated token cost

**Token warning gate:** If `estimated_tokens` > 30000, warn the user:
> "This paper is ~{estimated_tokens} tokens. Extraction will use a significant portion of conversation context. Proceed?"

Wait for user confirmation before continuing.

If metadata was generated (not from existing sidecar), ask the user to confirm or correct the title, authors, and year before proceeding. If the paper_id needs correcting (wrong name, typo), use `add_confirm_metadata` with `new_paper_id` to rename all files atomically:

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
from src.library import add_confirm_metadata, get_config
config = get_config()
result = add_confirm_metadata('OLD_PAPER_ID', 'TITLE', ['AUTHOR1', 'AUTHOR2'], YEAR, new_paper_id='NEW_PAPER_ID', config=config)
print(result)
"
```

This renames the meta sidecar, extracted text, and PDF. Claims and corrections files must be renamed separately if they already exist.

#### Phase 2: Build extraction prompt

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import add_build_prompt, get_config
config = get_config()
result = add_build_prompt('PAPER_ID', config)
print(json.dumps({k: v for k, v in result.items() if k != 'tools'}, indent=2, default=str))
"
```

**Check the result's `chunked` field.** If `false`, this is a standard single-pass extraction. If `true`, follow the chunked workflow below.

**Standard (single-pass) extraction:**

Read the system prompt and user prompt. Follow the extraction guidelines. Extract claims using the `extract_claims` tool schema:

- `claims`: list of claims, each with `text`, `type` (question/claim/evidence), `confidence` (proven/argued/empirical/conjectured), `provenance_level` (quote/passage/paper), and optional `provenance_detail`
- `relations`: list of relations between claims, each with `source_claim_index`, `target_claim_ref`, `relation_type` (supports/contradicts/extends/contextualizes), and `confidence`

Extract 3-8 claims per paper. Stay close to the paper's language. Propose cross-paper relations when existing claims are provided.

**Chunked extraction (large documents >400K chars):**

The result contains `"chunked": true` and a `"chunks"` list. Each chunk has its own `system_prompt`, `user_prompt`, and `tools`. Process each chunk sequentially:

1. For each chunk (in order), read its `system_prompt` and `user_prompt`. Extract claims from that chunk only - do not re-extract claims from the abstract unless the chunk materially extends it.
2. Collect raw extraction outputs from all chunks.
3. After all chunks are processed, run deduplication:

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.extraction import deduplicate_proposals
from src.schema import ClaimProposal
claims = [ClaimProposal(**c) for c in ALL_CLAIMS_JSON]
unique, duplicate_pairs = deduplicate_proposals(claims, threshold=0.85)
print(json.dumps({
    'unique_claims': [c.model_dump() for c in unique],
    'duplicate_pairs': duplicate_pairs,
}, indent=2))
"
```

4. If duplicate pairs are found, present them side by side for the user to resolve (keep one, merge, or discard).
5. Proceed to Phase 3 with the deduplicated claims as a single combined extraction.

#### Phase 3: Validate extraction

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import add_validate, get_config
config = get_config()
raw_output = RAW_EXTRACTION_JSON
result = add_validate('PAPER_ID', raw_output, config)
print(json.dumps(result, indent=2))
"
```

**Pre-submission self-check (run before presenting to user):**

1. **Relations — "extends" gate:** For each relation typed "extends," state what mathematical or conceptual apparatus the source paper adds beyond the target. If you cannot, change to "contextualizes."
2. **Confidence — provenance gate:** For each claim with confidence "proven," confirm the proof appears in this paper, not cited from another. If cited, change to "argued."
3. **Completeness — boundary check:** For each theorem or positive construction captured, check whether the paper states an impossibility or failure condition. If yes, consider whether it warrants a separate claim or passage.
4. **Formulas — OCR verification:** Any formula extracted from OCR text must be spot-checked (plug in a small case, check dimensions, verify coefficients). OCR reliably drops superscripts, subscript nesting, and fraction structure.
5. **Numbers — source verification:** Any specific count or number stated in a claim must appear in THIS paper. If the paper doesn't state the number, use approximate language ("over 30") rather than a precise count. When a number is flagged for review, verify the correction against this paper's own tables and text only — do not import values from other papers' tables. A confident wrong correction is worse than the original uncertainty.
6. **Relations — rationale verification:** For each cross-paper relation, verify that every technique or vocabulary the rationale attributes to the target paper actually appears in that paper. If the rationale names a method, term, or comparison the target paper doesn't contain, rewrite the rationale to state only what both papers actually say. Prefer contrast ("both constrain σ(W) via independent mechanisms") over derivation ("applies X's technique").

Present validated proposals to the user:
- Each claim with type, confidence, and provenance
- Each relation with source, target, and type
- Any validation warnings

**HITL checkpoint:** Ask the user to review:
- Accept all, reject some, or edit specific claims
- For each edit, track the original proposal and changes

Wait for user response. Do not finalize without explicit approval.

#### Phase 4: Finalize

Collect the user's decisions:
- `accepted_claims`: list of claim dicts (may include user edits)
- `accepted_relations`: list of relation dicts
- `corrections`: list of correction entries (edits, rejections) or null

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from src.library import add_finalize, get_config
config = get_config()
accepted_claims = ACCEPTED_CLAIMS_JSON
accepted_relations = ACCEPTED_RELATIONS_JSON
corrections = CORRECTIONS_JSON_OR_NULL
result = add_finalize('PAPER_ID', accepted_claims, accepted_relations, corrections, config)
print(json.dumps(result, indent=2))
"
```

Report:
- Claims stored (with assigned IDs)
- Relations stored
- Corrections stored
- BibTeX entry
- Citation key: show the auto-generated default key (e.g., `bessac2021`) from the result's `citation_key` field

**Citation key check:** The result includes `citation_key` (the generated default) and `citation_keys` (the full list on the sidecar). Show the default key and ask: "This paper is registered with citation key `<key>`. If you use a different key in your `.bib` files (e.g., `bessac2021forecast`), tell me and I'll add it as an alias." If the user provides aliases, save them:

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
from src.metadata_store import load_metadata, save_metadata
from src.config import load_config
from pathlib import Path
config = load_config(Path('config.yaml'), Path('..'))
meta = load_metadata('PAPER_ID', config.paths.meta_dir)
for key in ['ALIAS1', 'ALIAS2']:
    if key not in meta.citation_keys:
        meta.citation_keys.append(key)
save_metadata('PAPER_ID', meta, config.paths.meta_dir)
print(f'Citation keys: {meta.citation_keys}')
"
```

After finalization, suggest running `/library rebuild` to update the search index.

#### Phase 5: Key Passages

After claims are finalized, identify the paper's key quotable passages. Key passages are complementary to claims: claims capture what the paper asserts (epistemic), key passages capture how the paper formulates important concepts (definitional, methodological, characterizing).

**Selection heuristics (follow in order):**

1. **Contributions first.** Identify 3-5 things you would cite this paper for that you couldn't cite from a textbook. Start from the results/methods/discussion sections, not the introduction.
2. **Title check.** If the paper is called "Decomposition of X" and no passage mentions the decomposition, you are missing the paper's central contribution.
3. **Quote over paraphrase.** Default to verbatim text from the paper with exact location (section, equation, page). When the original is too notation-heavy to stand alone, paraphrase minimally and flag it. Never introduce terminology the paper does not use.
4. **Definitions are secondary.** Include definitional passages only when this paper gives the canonical or most-cited formulation. If the definition appears in every textbook on the topic, it is not a key passage for this paper.

**Procedure:**

1. Present proposed key passages to the user as a table: label, passage text, location.
2. Wait for user review. The user may accept, edit, reject, or add passages.
3. After approval, save to the metadata sidecar:

```bash
cd /home/simon/brain/9_library/library_system && .venv/bin/python -c "
import json
from pathlib import Path
from src.metadata_store import load_metadata, save_metadata
from src.schema import KeyPassage

meta_dir = Path('../papers/_meta')
meta = load_metadata('PAPER_ID', meta_dir)
meta.key_passages = [
    KeyPassage(text='PASSAGE_TEXT', location='LOCATION', label='LABEL'),
]
save_metadata('PAPER_ID', meta, meta_dir)
print('Key passages saved.')
"
```

Report the number of key passages stored. Then suggest running `/library rebuild` to update the search index.

#### Phase 6: Update Extraction Quality Register

After the user's audit feedback has been addressed for both claims and key passages, update `reports/extraction_quality_register.md`:

1. **Per-paper audit log** (Section 5): Append an entry with paper ID, archetype, finding count, error types, surprises, verdict, and protocol used.
2. **Cumulative statistics** (Section 1): Update the totals table.
3. **Active patterns** (Section 2): For each audit finding, check whether it matches an existing pattern. If yes, increment the count and update "last observed." If a finding represents a genuinely new pattern, add a new P-entry.
4. **What's working** (Section 3): If any probe categories passed cleanly or the user confirmed quality without changes, note what worked and why.
5. **Surprises** (Section 4): If anything unexpected happened — a new error type, an intervention that failed or succeeded unexpectedly, an unusual result — add an S-entry.
6. **Active experiments** (Section 6): If the paper is part of an active experiment (e.g., two-pass trial), update the experiment metrics.
7. **Workflow update history** (Section 7): If the audit led to a process change, log it.

Do this automatically after every audit cycle. Do not ask the user whether to update — just do it and report what changed.

## Error Handling

| Error | Cause | Response |
|-------|-------|----------|
| `FileNotFoundError: PDF not found` | Bad path | Ask user for correct path |
| `FileNotFoundError` on paper_id | Paper not in library | List available papers with `/library status` |
| `FileNotFoundError: Index needs rebuild` | No search index | Tell user to run `/library rebuild` |
| `ValueError: No claims or extracted text` | Paper has no evidence | Suggest adding claims or extracted text first |
| `RuntimeError: All PDF extraction methods failed` | PDF parsing failed | Ask user to provide a `.md` sidecar with extracted text |

## Output Format

1. Results first (verdict, claims, search hits)
2. Evidence next (passages, provenance, confidence)
3. Metadata last (model used, path, warnings)

Keep output concise. Use tables for lists of claims. Use code blocks for BibTeX. Use bullet points for search results.
