# Reflection: Writing "Making Conflict Risk Actionable"

**Process date:** 2026-04-30
**Document:** 2-page position paper for FAO Chief Economist
**Purpose:** Scaffolding for building strategic writing skills for Claude Code

---

## Process Summary

A 2-page position paper was written in one session through 10 phases:
1. Admin crisis triage (precondition)
2. Paragraph-by-paragraph Q&A drafting (AI prints, explains purpose, asks 3 questions, Simon corrects)
3. Referencing (search + Simon's corrections on citation framing)
4. Three-persona critique round 1 (editor/peer/FAO counterpart, deployed as parallel agents)
5. Revision plan + implementation
6. Falsification audit round 1 (claim: "all material criticisms resolved")
7. Falsification audit round 2 (meta-claim: "no question could improve this further")
8. Reference material integration (FSFC documents revealed institutional context)
9. Three-persona critique round 2
10. Final targeted fixes + title change

---

## 1. What Worked

### Paragraph-by-paragraph Q&A (highest-value move)
- AI prints paragraph, explains what it's meant to do, asks writer 3 questions
- Extracted strategic context no amount of drafting would produce:
  - FSFC isn't operational yet (overstatement prevented)
  - Episode identification is writer's original contribution (funding strategy)
  - Writer's paper is bespoke FAO architecture, not the public system (framing corrected)
  - Real purpose: make the reader protect the writer's funding line
- Every paragraph was written against wrong assumptions until the writer corrected it
- **The Q&A was not polish. It was load-bearing.**

### Three-persona critique (genuine diagnostic value)
- Three orthogonal failure modes: craft (editor), intellectual honesty (peer), institutional utility (FAO counterpart)
- Round 1 findings had zero overlap in primary findings
- Most consequential finding ("there is no ask") came from the persona most unlike the AI's default voice
- The personas are well-written caricatures, not realistic people. That's fine. The value is in forcing attention to different failure modes.

### Falsification audits (found different things than critiques)
- Critiques identify what is weak. Falsification audits identify what is wrong.
- Found: specific phrases surviving despite being flagged; claims overstating ground truth; improvements blocked by practical constraints
- Work because they test convergence claims ("everything is fixed"), not quality
- Different epistemic operation, complementary to critique

### Admin triage before writing
- A spiralling writer produces bad prose. Resolving the crisis first was a precondition, not a detour.
- Generalizes: assess writer's state before starting strategic work.

---

## 2. What Was Wasteful

### 7-pass revision plan (process theater)
- Seven named passes for 2 pages. Actual revisions were interleaved, not sequential.
- The plan gave the illusion of systematic coverage but real improvements came from specific persona findings.
- **Lesson:** Plan passes by finding, not by section or technique.

### Second persona critique round (diminishing returns)
- Largely confirmatory ("this is better," "would sign off")
- Actionable findings were editorial, not structural
- One round of persona critique + falsification audit covers the same ground in half the time
- **Lesson:** Second persona round only justified if revision was structural.

### Reference search (formality)
- Bibliography ended up with references the writer already knew
- The one real contribution (FSFC footnote) came from writer's own reference materials
- **Lesson:** Ask what the writer already knows before searching.

---

## 3. Generalizable Insights for Skill Design

### The writer's corrections are the primary source of value
- AI produces competent prose. Writer's corrections change truth content.
- Without corrections, document would have been fluent, well-structured, and wrong in ways that damage credibility with the actual reader.
- **AI's role: produce a surface for the writer to react against, not produce the document.**

### Strategic documents require adversarial reading before delivery
- Gap between "reads well" and "survives the reader's actual context" is large
- The persona critique identified flaws invisible from inside the writing process
- Forced the writer to make implicit choices explicit

### Falsification and critique are complementary, not redundant
- Critiques evaluate quality holistically
- Falsification audits check specific claims against ground truth
- Audits can elicit ground truth the writer hasn't volunteered ("Is X actually true?")

### The efficient process configuration
```
Draft (paragraph Q&A) -> 1 round of 3 personas -> falsification audit -> targeted fixes
```
Not:
```
Draft -> critique -> plan -> revise -> falsify -> critique again -> falsify again -> fix
```

---

## 4. The Writer's Most Consequential Corrections (Pattern)

Ranked by trajectory change:
1. **Factual correction** ("FSFC isn't operational yet") — prevented credibility damage
2. **Attribution correction** ("episode identification is MY contribution") — shifted strategic framing
3. **Provenance correction** ("my paper is bespoke, not backbone") — prevented misrepresentation
4. **Strategic correction** ("no explicit ask") — resisted process pressure toward the wrong format

Pattern: corrections 1-3 are about ground truth the AI cannot access. Correction 4 is a strategic judgment the AI's process kept trying to override. Both categories are essential. The skill must create space for both.

---

## 5. Orthogonality of Persona Lenses (Design Notes)

### What makes personas useful
- Each persona must have a **different failure mode** they're sensitive to, not just a different style
- Editor: craft failures (register contamination, structural overlap, weak transitions)
- Peer: intellectual overreach (claims outrunning evidence, analogies concealing disanalogies)
- Institutional counterpart: utility failures (no ask, no deliverables, wrong language, credibility gaps)

### What to watch for
- Round 2 personas were noticeably more positive — partly genuine, partly AI validating its own prior work
- The personas that matter most are the ones most unlike the AI's default voice (institutional counterpart > peer > editor)
- Personas should be deployed in parallel as separate agents, not sequentially in one context

---

## 6. Process Risks to Design Against

### Fluency masking falsehood (critical)
- AI produces confident prose about things it does not understand
- Document can pass editorial review while failing domain review
- **Design implication:** The skill must force ground-truth checks with the writer, not just ask "does this sound right?"

### Process as displacement
- Sophisticated process can become avoidance of the hard strategic decisions
- The process kept generating pressure toward an explicit ask; the writer had to resist his own process
- **Design implication:** The skill should not have opinions about strategic choices. It should surface them and let the writer decide.

### Persona flattery in later rounds
- Later-round personas validate the AI's own prior work
- **Design implication:** If running multiple rounds, the later round should be harder, not softer. Or: don't run multiple rounds.

### Sleep deprivation / writer state
- The process compensated for impaired judgment by externalizing quality control
- That worked once. It is not a repeatable strategy.
- **Design implication:** The skill should assess writer state and adjust process weight accordingly.

---

## 7. Candidate Skills to Build

Based on the above, the process breaks into separable capabilities:

### Skill: `strategic-draft` (paragraph-by-paragraph Q&A drafting)
- AI explains what each paragraph is meant to do
- Asks writer 3 targeted questions per paragraph
- Implements based on answers
- Key: must force ground-truth extraction, not just style input

### Skill: `persona-critique` (three-persona adversarial review)
- Deploys 3 parallel agents with orthogonal failure-mode sensitivity
- Each writes structured critique to `[persona]_critique_NN.md`
- One round default. Second round only on structural revision.
- Personas defined per document type (position paper, proposal, technical report, presentation)

### Skill: `falsify` (already exists)
- Works well as-is for document review
- Key insight: apply to convergence claims ("all criticisms addressed") not quality claims

### Skill: `strategic-revise` (critique-driven targeted revision)
- Takes critique findings as input, not a numbered pass list
- Groups findings by type: factual corrections, framing changes, sentence-level craft
- Asks writer for decisions on strategic questions before implementing
- Does NOT plan 7 passes. Plans by finding.

### Possible meta-skill: `write-for-impact` (orchestrator)
- Chains: assess writer state -> strategic-draft -> persona-critique -> falsify -> strategic-revise
- Knows when to stop (one critique round + one falsification is usually enough)
- Tracks which corrections came from the writer vs. the process

---

## Source Artifacts

All in `/home/simon/brain/2_projects/fao02/_dev_materials/one_pager_aa_ml/`:
- `main.tex` — final document
- `editor_critique_00.md`, `editor_critique_01.md`
- `peer_critique_00.md`, `peer_critique_01.md`
- `fao_critique_00.md`, `fao_critique_01.md`
- `falsification_findings_00.md`, `falsification_findings_01.md`
