---
name: persona-critique
description: Multi-persona critique of a draft document from domain expert and writing craft perspectives. Produces grounded findings in the writing-harness critique format. Two layers — domain panels (ML/DL, Bayesian statistics, conflict studies, configurable) and craft personas (Strategist, Reader, Editor, fixed) plus a bespoke Scout. Use when user says "critique this draft", "review the writing", "persona critique", "what would the experts say", "run the personas", or "critique section N". Do NOT use for harness sync (use review-harness), drafting (use strategic-draft), or code review (use expert-code-review).
---

# Persona Critique

## Important

Follow these rules strictly.

- Do not draft or revise prose. This skill critiques only.
- Do not write to FINDINGS.md. Produce critique files with Findings Summary tables. The user runs review-harness sync or manually extracts findings.
- Personas should either find problems or say nothing. Never validate. Never praise. (See FM-23: Persona flattery.)
- Do not merge persona perspectives. Each persona writes independently. Tension between personas is a feature.
- Ground every finding in specific sections, paragraphs, or sentences of the draft. No vague observations.
- When a finding maps to a cataloged failure mode, tag it (FM-XX). This connects critiques to sentries.

## Purpose

Deploy parallel expert personas to critique a draft document for substantive accuracy, methodological rigor, and writing craft. Produces structured critique files in `critiques/` that feed the writing-harness finding pipeline.

The goal is to surface what's wrong, weak, missing, or misleading — not to confirm that the draft is good.

## Persona Architecture

Two layers plus a scout. Domain personas are selectable per document. Craft personas always run.

### Domain Panels (select which panels to activate)

Consult `references/domain_panels.md` for the full persona definitions.

- **ML/DL Panel** — channels Goodfellow, Hinton, LeCun, Bengio, Karpathy, Sutskever, Welling, Kingma
- **Bayesian Statistics Panel** — channels Gelman, McElreath, Vehtari, Rasmussen, Jordan, Carpenter, Ghahramani, Blei
- **Conflict Studies Panel** — channels Hegre, Cederman, Buhaug, Gleditsch (N.P. & K.S.), Weidmann, Gates, Müller, Colaresi, Tollefsen

Each panel is a single composite persona — one voice channeling the collective standards of the named authorities.

### Craft Personas (always active)

Consult `references/craft_personas.md` for the full persona definitions.

- **The Strategist** — argument architecture, claim-evidence chains, does the paper deliver on its promise
- **The Reader** — cognitive load, clarity, assumed knowledge, "I got lost here"
- **The Editor** — economy, precision, rhythm, "this paragraph earns its space"

### The Scout (always active)

A bespoke persona generated fresh for each critique invocation. Briefed from:
- The document's MANIFESTO.md (reader's takeaway, implicit/explicit tiers)
- The document type and target audience
- The specific section under review

The scout looks for the domain-specific vulnerability that no fixed persona would catch. It names itself based on what it decides to watch for.

## Library Integration

Domain personas may access the research library at `~/brain/9_library/` for grounded references. The library contains ~300 papers with two access layers:

1. **`papers/THEMATIC_INDEX.md`** — Human-curated index of papers by methodological tradition (22 traditions) with 13 cross-tradition bridges. Start here. Token-efficient and organized by domain.
2. **`papers/graphify-out/graph.json`** — Knowledge graph (480 nodes, 676 edges). For connection discovery beyond the thematic index.

Consult `references/library_protocol.md` for the full progressive disclosure protocol.

**Token discipline**: Each domain persona gets a total library interaction budget of 2000 tokens. The thematic index is the primary tool (cheap, structured). Graph queries are a fallback. Craft personas and the scout do not access the library.

## Procedure

### Phase 1: Load Context

1. Locate the document and its harness: find `_dev_materials/*/DECISIONS.md`
2. Read the draft (or the section specified by the user)
3. Read MANIFESTO.md (for scout briefing and implicit/explicit awareness)
4. Read DECISIONS.md (for resolved constraints the draft must respect)
5. Determine the critique round number: count existing files in `critiques/` to assign the next `<NN>`
6. If library graph exists at `~/brain/9_library/graphify-out/graph.json`, note it as available for domain personas

### Phase 2: Select Domain Panels

If the user specified panels, use those. Otherwise, infer from the document content:
- Contains ML/DL methodology → activate ML/DL panel
- Contains Bayesian inference or probabilistic modeling → activate Bayesian panel
- Contains conflict data, peace research, or political violence → activate Conflict Studies panel

Confirm panel selection with the user before proceeding if inferred rather than specified.

### Phase 3: Brief the Scout

Read MANIFESTO.md and the draft section. Generate the scout's identity:
- What specific vulnerability is this document most exposed to, given its domain, audience, and strategic intent?
- Name the scout after its focus (e.g., "The Methodological Skeptic", "The Policy Reader", "The Data Auditor")
- The scout watches for failure modes that the fixed personas' mandates don't cover

### Phase 4: Dispatch Personas

Launch all active personas as parallel subagents. Each persona receives:
- The draft text (or section)
- Its persona definition (from references/)
- The critique format template (header, body in persona voice, Findings Summary table)
- The failure mode catalog excerpt relevant to its lens
- The round number

Domain personas additionally receive:
- Library graph access instructions (progressive disclosure protocol)
- Any relevant anchors from `anchors/`

Each persona writes its critique to a temporary working file. The body follows the persona's natural voice — a professional letter-style critique, not a checklist.

### Phase 5: Collect and File Critiques

1. Collect all persona outputs
2. Write each to `critiques/<lens>_<NN>.md` following the naming convention:
   - Domain panels: `ml_dl_<NN>.md`, `bayesian_<NN>.md`, `conflict_studies_<NN>.md`
   - Craft personas: `strategist_<NN>.md`, `reader_<NN>.md`, `editor_<NN>.md`
   - Scout: `scout_<NN>.md`
3. Each file must end with a Findings Summary table (see format below)

### Phase 6: Cross-Persona Tensions

After all critiques are filed, identify findings where personas disagree or where fixing one finding would create another. Report these tensions — do not resolve them. The writer resolves tensions.

### Phase 7: Summary Report

Present to the user:
- Total findings by severity (Critical / Substantive / Editorial) across all personas
- Cross-persona tensions
- Any failure mode patterns (same FM-XX appearing across multiple personas = evidence for graduation)
- If the draft contains `\cite{}` commands and no `citations/CITATION_LEDGER.md` exists in the harness: note "Source verification has not been run. Consider `/verify-sources`."
- Verdict (see below)

## Required Critique Format

Each persona's output file follows the writing-harness critique format:

```markdown
# [Persona Name] Critique: "[Document Title]"

**[Persona name]**, [role description]
**Date:** [YYYY-MM-DD]
**Round:** [NN]
**Lens:** [domain panel name / craft / scout]
**Failure modes watched:** [FM-XX list]

[Body: professional letter-style critique in the persona's voice, organized by section or by finding type. Readable, not a checklist.]

## Findings Summary

| # | Section | Finding | Severity | FM-XX | FINDINGS.md |
|---|---------|---------|----------|-------|-------------|
| 1 | §2      | [short description] | Substantive | FM-16 | pending extraction |
```

## Verdict

- **CLEAN**: Fewer than 3 findings total, none Critical. Unusual — note if this feels like FM-23 (flattery).
- **NEEDS WORK**: Findings present but no structural problems. Addressable in revision.
- **STRUCTURAL ISSUES**: Critical findings or cross-persona tensions that require rethinking a section or argument.
- **RETHINK**: Multiple Critical findings across personas pointing at the same root cause. The section's approach may need to change, not just its text.

## Invocation

```
/persona-critique                          # critique current draft, infer panels
/persona-critique §3                       # critique section 3 only
/persona-critique --panels ml,bayesian     # specify domain panels
/persona-critique --panels conflict,ml §2  # panels + section
/persona-critique --full                   # full document, all panels
/persona-critique --no-library             # skip library graph queries
```

## Performance Notes

- Quality over speed. Each persona should take its time.
- The scout is often the most valuable persona. Invest in its briefing.
- If the library graph is stale (check `graphify-out/cost.json` dates), warn the user. Stale references are worse than no references.
- Craft personas do not need domain expertise to find problems. Unclear writing is unclear regardless of field.
- On a single section: 4-7 findings per persona is normal. More than 10 suggests the persona is nitpicking. Fewer than 2 suggests FM-23 or an overly narrow mandate.
- On a full document: expect 20-40 total findings across all personas. Prioritize by severity.
- Do not run more than 7 personas per invocation. If all 3 domain panels + 3 craft + scout = 7, that's the maximum.
