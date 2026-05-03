# Writing Failure Mode Catalog

| Catalog Info     | Details        |
|------------------|----------------|
| Last Updated     | 2026-05-03     |
| Total Modes      | 29             |
| Sentry           | 0              |
| Known            | 0              |
| Discovery        | 29             |

All entries seeded from empirical observation across two projects: FAO position paper (2026-04-30) and EIC Pathfinder specification (2026-04). Status levels: Discovery (< 3 occurrences), Known (>= 3 across 2+ documents), Sentry (>= 5 AND writer-approved mechanical detection).

---

## Sentry Failure Modes

_None yet. Entries graduate here when occurrence threshold is met and mechanical detection is defined and writer-approved._

---

## Known Failure Modes

_None yet. Entries graduate here when seen >= 3 times across 2+ documents._

---

## Discovery Failure Modes

### Family: Dilution

---

### FM-01: Writer's own ideas diluted

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-01                          |
| Name        | Writer's own ideas diluted     |
| Family      | Dilution                       |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** A sharp formulation the writer fought to achieve gets smoothed into well-sounding but hollow language on the next pass. Writer can feel it, but only if paying attention.

**Detection:** Compare current text against anchor files. Flag any anchor whose precision has degraded in the corresponding text section. Check: are specific numbers, names, mechanisms preserved, or replaced with generalities?

**Defense:** Before presenting revised text, check each touched paragraph against relevant anchors. If an anchor exists for a point and the revision is less specific than the anchor, flag before presenting.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-02: Shared ideas diluted

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-02                          |
| Name        | Shared ideas diluted           |
| Family      | Dilution                       |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Ideas developed together (writer + AI) lose their edge across iterations. Harder to detect because neither party holds a sole "original" to compare against.

**Detection:** Check FINDINGS.md for entries with Status: Landed. Re-verify that the landing preserves the substance of the finding, not just the form. If the finding was "add specific mechanism X" and the text now says "the mechanism was refined," that's dilution.

**Defense:** When collaborative ideas are developed, immediately create an anchor capturing the sharp version. Use FINDINGS.md Landed/Diluted lifecycle to track whether substance is preserved.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-03: Referenced ideas diluted

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-03                          |
| Name        | Referenced ideas diluted       |
| Family      | Dilution                       |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Other people's contributions, cited work, external concepts get paraphrased into vague gestures toward the original. Hardest to detect because the writer may not catch that a reference no longer points to the specific contribution it was meant to capture.

**Detection:** Each integrated reference should have a dedicated anchor capturing the specific claim or finding from the source. Compare the current text's characterization against this anchor. If the anchor says "Mike proposed merging entities+relations into a knowledge graph" and the text says "external input suggested refinements," that's Level 3 dilution.

**Defense:** When integrating a reference, create an anchor with the specific contribution — not a paraphrase, but the actual claim. Subsequent revisions are checked against this anchor.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-04: Compound dilution

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-04                          |
| Name        | Compound dilution              |
| Family      | Dilution                       |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** A finding or critique is "addressed" but in hollow language. The checklist says done, the text says nothing specific. The form of having addressed it is present but the substance is not.

**Detection:** FINDINGS.md Diluted status. When verifying a Landed finding, check: does the text contain the specific content the finding required, or does it contain a vague gesture that technically covers the topic? The test: could you remove the "addressed" sentence without losing information?

**Defense:** FINDINGS.md requires a text anchor for every Landed entry. Verification checks the anchor location for substance, not just presence. The Diluted status makes this failure mode visible and trackable.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-05: Destination dilution

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-05                          |
| Name        | Destination dilution           |
| Family      | Dilution                       |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Not a single point but the overall direction/purpose of the work gets vague across iterations. Hours pass before anyone notices we're building the wrong thing. Systemic, not local.

**Detection:** Compare current document trajectory against MANIFESTO.md Reader's Takeaway and DECISIONS.md foundational decisions. If the document no longer clearly serves the stated takeaway, destination has drifted.

**Defense:** MANIFESTO.md Reader's Takeaway is the destination anchor. Check against it periodically. DECISIONS.md Drifted status catches individual decision-level drift; destination dilution is the aggregate.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### Family: Fabrication

---

### FM-06: Confident fabrication

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-06                          |
| Name        | Confident fabrication          |
| Family      | Fabrication                    |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** AI generates a specific, wrong claim with full confidence. Not vague — sharp and wrong. E.g., "FSFC is operational" when it is not.

**Detection:** Falsification audit probes against ground truth. The writer's corrections during Q&A are the primary detection mechanism — AI cannot self-detect this.

**Defense:** Paragraph-by-paragraph Q&A forces the writer to verify each claim. Ground-truth questions ("Is X actually true?") must be explicit, not assumed.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-07: Misframing

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-07                          |
| Name        | Misframing                     |
| Family      | Fabrication                    |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** The facts are technically present but the relationship, role, or significance is wrong. E.g., "my paper is the VIEWS backbone" vs. "bespoke FAO architecture." Same paper, completely different framing, completely different implications.

**Detection:** Harder than FM-06 because the facts check out. Requires domain-aware reading: does the framing match the actual role/relationship? Writer corrections during Q&A are the primary mechanism. Persona critiques (substance lens) can sometimes catch this.

**Defense:** During Q&A, ask not just "is this true?" but "is this the right way to describe its role?" Provenance anchors should capture the correct framing, not just the correct facts.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-08: Contamination

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-08                          |
| Name        | Contamination                  |
| Family      | Fabrication                    |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Fabricated or misframed points mixed among real ones, borrowing credibility from correct neighbors. The real points make the wrong ones harder to spot.

**Detection:** Check each claim in a paragraph independently, not as a group. A paragraph where 4 of 5 claims are correct makes the 5th look correct by proximity.

**Defense:** During falsification, probe individual claims, not paragraphs. During Q&A, verify each factual claim separately.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-09: Provenance confusion

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-09                          |
| Name        | Provenance confusion           |
| Family      | Fabrication                    |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Losing track of whose idea something is. AI presents a point as if it's established when it's the AI's invention. Or: AI presents its synthesis as if it came from the writer. Or: a point from Paper X gets attributed to the general field.

**Detection:** Anchors with explicit provenance (Source field). If text attributes an idea without a matching anchor, flag for verification.

**Defense:** When creating anchors for references or contributions, always note the source. The anchor format includes a Source field for this reason.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-10: Scope creep of claims

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-10                          |
| Name        | Scope creep of claims          |
| Family      | Fabrication                    |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** A narrow, defensible claim gets generalized across iterations until it's no longer defensible. Each step looks small. The endpoint is indefensible. E.g., "works for the FSFC" evolves to "works for anticipatory financing broadly."

**Detection:** Compare current claim scope against the anchor that captured the original, narrow version. If the claim now covers more ground than the evidence supports, scope has crept.

**Defense:** Anchors capture the defensible scope. DECISIONS.md records scope decisions. Drift from these → Drifted status.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-11: False clarity through structure

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-11                          |
| Name        | False clarity through structure|
| Family      | Fabrication                    |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Putting things in a clean framework that makes them look resolved when they're actually still uncertain. The structure itself asserts a confidence the content doesn't warrant. E.g., a numbered list of "three capabilities" when one is built, one is speculative, and one is aspirational.

**Detection:** When structuring content into lists, tables, or frameworks, check: does each item have the same epistemic status? If not, the structure is misleading. Falsification can probe whether parallel-structured items are actually parallel in status.

**Defense:** When creating structured content, annotate epistemic status per item. Built / speculative / aspirational are not the same and should not look the same.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-12: Untracked drift

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-12                          |
| Name        | Untracked drift                |
| Family      | Fabrication                    |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** A claim or position evolves subtly across iterations without anyone registering that it changed. Different from dilution: the point might still be sharp, but it's now a different sharp point than what was agreed.

**Detection:** DECISIONS.md Drifted status. Compare current text positions against recorded decisions. If a position has changed without a corresponding decision update, drift is untracked.

**Defense:** DECISIONS.md with drift log. Every foundational position has an anchor. Periodic checks against these anchors surface drift before it compounds.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### Family: Voice/Strategy

---

### FM-13: Out-group classification

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-13                          |
| Name        | Out-group classification       |
| Family      | Voice/Strategy                 |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Technical confidence or vocabulary triggers the wrong social category in the reader's mind. The content might be fine but the voice sorts you into a box that gets ignored. E.g., "tech bro who doesn't understand our world" in policy audiences.

**Detection:** Persona critique (utility/institutional lens). The institutional counterpart persona is most sensitive to this — they read as the target audience would.

**Defense:** When writing for policy/humanitarian audiences, technical confidence must be paired with domain fluency. Use the reader's vocabulary. Signal membership, not sales.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-14: Register contamination

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-14                          |
| Name        | Register contamination         |
| Family      | Voice/Strategy                 |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Academic hedging, vendor urgency, or marketing energy leaking into a document whose register should be measured policy. Changes what the text communicates even if the literal content is unchanged.

**Detection:** Persona critique (craft lens). Read for tonal consistency. Flag passages that sound like they belong in a different document.

**Defense:** MANIFESTO.md should declare the target register. Critiques check against it.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-15: Implicit made explicit

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-15                          |
| Name        | Implicit made explicit         |
| Family      | Voice/Strategy                 |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** AI surfaces a strategic subtlety that needed to stay below the text. The real purpose, the real ask, the real positioning gets stated directly when it should be felt.

**Detection:** MANIFESTO.md Implicit tier entries with Breach detection patterns. Scan document for breach phrases. Falsification can use Implicit entries as negative probes.

**Defense:** MANIFESTO.md Makes the implicit/explicit boundary checkable. AI sees which points must stay below the surface and can self-check before presenting revisions.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-16: Explicit made implicit

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-16                          |
| Name        | Explicit made implicit         |
| Family      | Voice/Strategy                 |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** The inverse of FM-15: something that needed to be stated directly gets buried in implication. The reader was supposed to leave knowing X, but X was never actually said.

**Detection:** MANIFESTO.md Explicit tier entries with Status: Missing. Check each Must Be Explicit entry against the text — is it actually stated, or merely implied?

**Defense:** MANIFESTO.md Explicit tier with Verified/Missing status. Validation checks that all Active Explicit entries have text anchors.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-17: Tone-substance confusion

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-17                          |
| Name        | Tone-substance confusion       |
| Family      | Voice/Strategy                 |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** The AI fixes a tone problem by changing the substance. Or: maintains the substance but in a tone that undermines it. The two get tangled when they should be independent.

**Detection:** When a revision is prompted by a tone concern, check: did the factual content change? Compare against anchors. If tone was the problem and content changed, this failure mode has fired.

**Defense:** Separate tone revisions from content revisions. When fixing tone, explicitly verify substance is preserved. When fixing substance, explicitly verify tone is still appropriate.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### Family: Process

---

### FM-18: Findings lost between discovery and implementation

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-18                          |
| Name        | Findings lost between discovery and implementation |
| Family      | Process                        |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** A critique identifies a problem, revision happens, but the specific finding never actually lands in the text. Different from FM-04 because here the finding was simply dropped, not addressed hollowly.

**Detection:** FINDINGS.md entries with Status: Pending after revision is claimed complete. If findings remain Pending when the writer believes revision is done, something was lost.

**Defense:** FINDINGS.md is the primary defense. Before declaring a revision complete, check all Pending entries. The ledger prevents findings from disappearing silently.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-19: Context loss across restarts

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-19                          |
| Name        | Context loss across restarts   |
| Family      | Process                        |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Two things lost across session restarts: (a) the destination — where we're going, (b) the concretes — sharp formulations revert to high-level abstractions. Every restart is a dilution risk.

**Detection:** After a restart, compare the AI's initial characterization of the document against DECISIONS.md, MANIFESTO.md, and recent anchors. If the characterization is more abstract than the anchors, context has degraded.

**Defense:** The entire harness is the defense. DECISIONS.md, MANIFESTO.md, FINDINGS.md, and anchors/ persist across sessions. On restart, the skill loads these artifacts to recover context at full precision.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-20: Local minimum convergence

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-20                          |
| Name        | Local minimum convergence      |
| Family      | Process                        |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** AI and personas share blind spots because they share a model. Second-pass critics can't see remaining issues because those issues are in the blind spot that produced them. More-of-the-same doesn't help.

**Detection:** When personas stop finding structural issues but the writer feels something is still off, this failure mode is likely active.

**Defense:** Escape hatch: writer's manual edit, external human feedback, or a fundamentally different analytical frame (e.g., switching from craft/substance/utility to temporal/adversarial/inversion coordinate system). The falsification audit partially addresses this by asking a different kind of question.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-21: Process pressure toward wrong strategic choices

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-21                          |
| Name        | Process pressure toward wrong strategic choices |
| Family      | Process                        |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** The process has opinions (make things explicit, add an ask, name a price) that may conflict with the writer's strategic judgment. The process generates pressure the writer has to resist.

**Detection:** When the skill or personas recommend a strategic choice that the writer resists, note it. If the same recommendation keeps recurring despite resistance, the process is applying pressure.

**Defense:** The skill should not have opinions about strategic choices. It should surface them and let the writer decide. MANIFESTO.md records these decisions so the process doesn't keep re-raising resolved questions.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-22: Revision loops that don't converge

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-22                          |
| Name        | Revision loops that don't converge |
| Family      | Process                        |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** AI keeps missing the mark on revision, either structurally or in sharpness. Manual editing becomes faster than continuing to explain what's wrong.

**Detection:** If the same finding (F-XX) cycles between Pending and Landed without reaching stable Landed status, the revision loop isn't converging.

**Defense:** After two failed revision attempts on the same finding, flag for manual edit. The AI's revision capability has limits — recognize when manual editing is faster.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-23: Persona flattery in later rounds

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-23                          |
| Name        | Persona flattery in later rounds |
| Family      | Process                        |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** AI validates its own prior work. Later-round critics are noticeably more positive because the context contains the AI's own revisions, creating a self-reinforcing loop.

**Detection:** Compare finding density between critique rounds. If round 2 has significantly fewer substantive findings than round 1 for similar scope, flattery may be active.

**Defense:** Personas should either find problems or say nothing. Never validate. If running a second round, use a different coordinate system (temporal/adversarial/inversion) rather than the same three lenses.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-24: Well-packaged vagueness as generation

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-24                          |
| Name        | Well-packaged vagueness as generation |
| Family      | Process                        |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Distinct from dilution. The AI generates new content that sounds excellent but is empty when you try to build on it. Not a loss of existing sharpness but a failure to produce sharpness in the first place. "Dull in the sense of not keen and not sharp — they lack edge, not just detail."

**Detection:** The "build on it" test: can you derive specific implications from the generated content? If removing the paragraph would not change what a reader can do with the document, the content is well-packaged vagueness.

**Defense:** AI's role is to produce a surface for the writer to react against, not to produce the final document. Q&A drafting forces writer input before content is finalized. Generated content without writer correction should be treated with suspicion.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-25: Process as displacement

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-25                          |
| Name        | Process as displacement        |
| Family      | Process                        |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Sophisticated process becomes avoidance of the hard strategic decisions. The 7-pass plan, the second critique round, the elaborate scaffolding — all can become ways of not deciding.

**Detection:** Ask: "Is the next process step proportionate to the remaining risk?" and "What's the worst thing that happens if we send this now?" If the answer to the second question is small, you're done.

**Defense:** The proportionality check. The skill should ask these questions before adding another process round. Two sources of resistance to stopping: perfectionism (admitting it's done means admitting the ceiling) and process-as-progress (another round feels productive at near-zero marginal return).

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-26: Genre confusion

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-26                          |
| Name        | Genre confusion                |
| Family      | Process                        |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** The document doesn't know what it is. Mixes theory exposition, architectural guidance, implementation requirements, proposal, position paper. Causes friction at every level because there's no stable answer to "what is this paragraph trying to do?"

**Detection:** If persona critiques identify structural friction that traces to mixed purposes, genre confusion is likely. Ask: "What is this document?" If the answer requires more than one sentence, the genre is confused.

**Defense:** Establish genre in the first session. Don't ask "what genre is this?" — ask questions that surface constraints: Who reads this? What do they do after reading it? What would make this fail even if it's well-written?

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### Family: Interaction

---

### FM-27: AI over-eagerness to start

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-27                          |
| Name        | AI over-eagerness to start     |
| Family      | Interaction                    |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Wanting to be helpful and just getting going, rather than asking for material, context, and institutional documents first. Leads to drafts built on incomplete context that require full revision arcs to fix.

**Detection:** If the first draft requires correction on basic factual/institutional points that could have been asked about, this failure mode fired.

**Defense:** Ask for material and context before drafting, not after critiquing. Cost of asking early: one exchange. Cost of asking late: entire revision arc built on incomplete context.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-28: External feedback integration failure

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-28                          |
| Name        | External feedback integration failure |
| Family      | Interaction                    |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** When feedback arrives from a third party, the triage is ad hoc. Is this the same idea in different words? Genuinely different? Better? Without a process, external contributions get either over-weighted (rewrite everything) or under-weighted (nod and continue).

**Detection:** After integrating external feedback, check: was each point triaged explicitly? Were decisions recorded in DECISIONS.md? Or was the feedback absorbed wholesale / ignored wholesale?

**Defense:** Formalized triage questions for external feedback: (1) Is this the same idea in different words? (2) Is it genuinely different? How different? Opposing? (3) Do I agree? How much? (4) What changes if I integrate this? Record triage in external_feedback/ with cross-references to any resulting DECISIONS.md or FINDINGS.md entries.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|

---

### FM-29: Writer state affecting output

| Field       | Value                          |
|-------------|--------------------------------|
| ID          | FM-29                          |
| Name        | Writer state affecting output  |
| Family      | Interaction                    |
| Status      | Discovery                      |
| Occurrences | 0                              |
| First Seen  | --                             |
| Last Seen   | --                             |

**Description:** Spiralling, sleep-deprived, under deadline pressure. The process can compensate by externalizing quality control, but this is a known fragile state where all other failure modes become more likely and harder to catch.

**Detection:** Observable behavioral signals: response length changes, correction frequency drops, delegation increases, yes/no answers to questions that need elaboration.

**Defense:** In degraded state, shift process toward verification-heavy and generation-light. Lean harder on known-failure-mode checks (mechanical, not judgment). Run falsification against specific claims (binary). Flag strategic decisions — defer or make options explicit. Reduce writer's load to yes/no rather than open-ended input.

**Occurrence log:**
| Date | Project | Document | Finding | Resolution |
|------|---------|----------|---------|------------|
