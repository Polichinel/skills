# Strategic Draft: Detailed Phase Instructions

## Phase 1 — Locate Harness

Find or create the writing harness before any drafting begins.

**Discovery logic:**

1. Search for `_dev_materials/*/DECISIONS.md` in the current working directory
2. If exactly one harness is found, load it
3. If multiple harnesses are found, list them and ask: "Which document are we working on?" Wait for answer.
4. If no harness is found, proceed to auto-bootstrap

**Auto-bootstrap procedure:**

When no harness exists, create a minimal one. Ask only three questions:

1. "What's the working title?" (determines the slug and directory name)
2. "Who reads this, and what do they do after reading it?" (fills Audience and seeds Reader's Takeaway)
3. "What would make this document fail even if it's well-written?" (seeds the first MANIFESTO.md implicit-tier entry and the first DECISIONS.md entry)

From the answers, create:

```
_dev_materials/<slug>/
├── DECISIONS.md     (from writing-harness/references/decisions_template.md)
├── FINDINGS.md      (from writing-harness/references/findings_template.md)
├── MANIFESTO.md     (from writing-harness/references/manifesto_template.md)
└── anchors/         (empty directory)
```

Fill in the templates:
- DECISIONS.md: Document name, dates, D-01 with Status: Open for the scope boundary question
- FINDINGS.md: Document name, dates
- MANIFESTO.md: Document name, Audience, Reader's Takeaway (drafted from the "who reads this" answer), at least one M-01 entry in the appropriate tier

Do not create `critiques/`, `falsification/`, or `external_feedback/` directories — those are created by the skills that need them. The minimal harness is intentionally minimal.

After bootstrap, confirm what was created and proceed to Phase 2.

---

## Phase 2 — Gather Context

Load the current state of the document and its harness.

**Resuming an existing session (harness has content):**

Read, in this order:
1. MANIFESTO.md — Reader's Takeaway first, then all three tiers
2. DECISIONS.md — focus on Open and Drifted entries
3. FINDINGS.md — focus on Pending entries
4. Most recent anchors (by date or numbering)
5. The document itself (if it exists)

Summarize the current state in 3–5 sentences. Include:
- What the document is and who it's for (from MANIFESTO.md)
- What's been decided and what's still open (from DECISIONS.md)
- What findings are pending (from FINDINGS.md)
- What was drafted last session (from the document or the previous handoff notes)

End with: "Where do you want to pick up?"

**Starting fresh (just bootstrapped or empty harness):**

Ask the four harness questions if not already answered during bootstrap:
1. What is the document? (working title, purpose)
2. Who reads this? What do they do after reading it?
3. What would make this fail even if it's well-written?
4. What institutional documents, reference materials, or prior correspondence exists that the audience would recognize as their language?

Question 4 is especially important. The answer identifies the register — not the skill's idea of what the register should be, but the actual language the audience uses. If the writer provides reference materials, create anchors capturing specific formulations from those sources.

---

## Phase 3 — Assess Scale and Plan

Estimate the document's complexity and choose the appropriate drafting rhythm.

**Scale is not page count.** A 2-page document with three competing audiences is more complex than a 10-page document with one. Assess on these dimensions:

| Dimension | Low complexity | High complexity |
|-----------|---------------|-----------------|
| Audiences | Single reader or homogeneous group | Multiple readers with different needs |
| Claims | Few claims, well-evidenced | Many claims, some contested |
| Political sensitivity | Internal use, low stakes | External review, career/funding implications |
| Structural choices | Obvious structure (e.g., standard report) | Structure itself is a strategic decision |
| Novelty | Well-trodden territory | New argument, new framing, or new method |

**Three scale bands:**

**Short (low complexity, 1–3 pages):** Skip formal section planning. Go straight to Phase 4 to resolve foundations, then Phase 5 to draft. The overhead of a section outline isn't justified. Ask: "What's the first thing the reader needs to know?" and start there.

**Medium (moderate complexity, 3–15 pages):** Propose a section outline. Each section gets a one-sentence purpose: what does this section do for the reader? Present the outline and get confirmation before drafting. Create a D-XX entry for the structural choice ("Document follows [structure] because [reason]").

**Long (high complexity, 15+ pages):** Require an explicit section plan before any prose is written. Each section gets: purpose, key claims, audience segment it serves, dependencies on other sections. Create D-XX entries for each major structural decision. The plan itself becomes a document worth reviewing before proceeding.

If the writer pushes to "just start writing" on a high-complexity document, note the risk but comply: "Starting without a section plan. We can restructure later, but it gets harder as more prose accumulates. I'll flag when I think we need to step back."

---

## Phase 4 — Resolve Foundations

Surface and resolve the decisions that must be made before prose is written.

**Three minimum foundations:**

1. **Scope boundary:** What is in and what is out. This prevents scope creep mid-document and gives the writer a defense against "but you didn't cover X." Create D-XX with Status: Open, present options, record resolution.

2. **Primary claim or argument:** What is the one sentence the reader should take away? This is not the Reader's Takeaway (which is about the reader's state after reading). This is the document's thesis — its single strongest statement. If the writer can't state it in one sentence, the document isn't ready to draft.

3. **Audience assumption:** What does the reader already know, and what do they need to learn from this document? This controls the level of explanation and prevents both over-explaining (condescending) and under-explaining (opaque).

**How to present decision options:**

For each foundation, present 2–3 concrete options with tradeoffs. Do not present a "recommended" option — this biases the writer toward the AI's preference. Present the options neutrally and let the writer choose.

Bad: "I recommend option A because..." (FM-26: Anchor Drop)
Good: "Option A gives you X but costs Y. Option B gives you Z but costs W. Which fits your situation?"

Record each resolution as a D-XX entry with Status: Resolved. The rationale must include why the alternatives were rejected, not just why the chosen option was preferred.

**When to push back on "let's just start writing":**

If the writer wants to skip foundations:
- For the scope boundary: comply but warn. "Starting without a scope boundary. I'll flag scope creep when I see it."
- For the primary claim: push back once. "I need to know the single strongest statement in this document to ask useful questions. Can you give me a rough version, even if it's not final?" If they still decline, proceed and try to extract it from the first few paragraphs.
- For the audience assumption: push back once. "I need to know what the reader already knows so I can calibrate the questions. What's their background?" If they decline, default to "intelligent non-specialist" and adjust as signals emerge.

---

## Phase 5 — Draft via Q&A

The core drafting loop. This is where prose is produced.

**The loop:**

1. Writer provides direction (a topic, a claim, a rant, a rough paragraph, or "draft the next section")
2. AI structures, questions, or drafts as appropriate
3. For every paragraph of prose (whether writer-provided or AI-drafted), present three questions (see `references/question_generation.md`)
4. Writer responds, revises, or says "move on"
5. Track green/red position (see `references/green_red_spectrum.md`)
6. Repeat

**When to draft vs. when to question:**

- Writer provides raw content (a rant, bullet points, a rough formulation) → Structure it into prose, then question. Do not question the raw input — question the structured version.
- Writer says "draft the next section/paragraph" → Draft it, then question. The draft should follow from the last anchored decision and the section plan (if one exists).
- Writer asks a question → Answer it. This is a green exchange — the writer is seeking information, not challenging.
- Writer challenges something → Defend or concede honestly. This is a red exchange. If the challenge is valid, concede immediately and revise. Do not defend a position you know is wrong (FM-25: Sycophantic Collapse in reverse — don't resist valid criticism just to seem consistent).

**Handling silence:**

If the writer goes quiet after a question, wait. Do not fill the silence with more prose, more questions, or "shall I continue?" The writer may be thinking. If the conversation has a gap (they come back in a new session), Phase 2's context-loading handles re-entry.

**Creating artifacts during drafting:**

**Anchors** (immediate — do not batch): When the writer provides a sharp formulation, mathematical definition, precise claim, or specific example that will be referenced later, create an anchor file immediately. Tell the writer: "Anchored as A-NNNN." The anchor preserves the formulation at its sharpest; if subsequent drafting softens it, the question mechanism will catch the drift.

**Decisions** (at the moment of choice): When a foundational choice is made — even mid-paragraph — create a D-XX entry. Scope changes, framing choices, methodology decisions, structural pivots. The writer doesn't need to see the entry being created every time; mention it briefly: "Recorded as D-XX."

**Manifesto entries** (when strategic intent surfaces): When the writer reveals something that "must be felt but never stated," or when a new explicit requirement emerges, add an M-XX entry to the appropriate tier. For implicit-tier entries, always ask: "Should this stay below the surface?" before recording.

**Findings** (mandatory check after each Q&A exchange): After every three-question exchange, ask yourself: "Did any question reveal a gap, unsupported claim, audience mismatch, or strategic misalignment?" If yes, create an F-XX entry with Status: Pending immediately — even if the writer revised the paragraph in response. The finding exists as a record that the issue was surfaced. If the revision addressed it, the finding can be marked Landed during Phase 6. An empty FINDINGS.md after extensive Q&A is a sign this step is being skipped.

**Paragraph-level workflow:**

```
Writer input
  ↓
Structure/Draft (if needed)
  ↓
Three questions (ground truth, strategy, reader impact)
  ↓
Writer responds → Revision loop (0-N rounds)
  ↓
Log any findings from the Q&A (mandatory check)
  ↓
Anchor any sharp formulations
  ↓
Record any decisions made
  ↓
Next paragraph
```

**Sentry checks during drafting:**

Load `writing-harness/references/failure_mode_catalog.md`. For any failure mode with Status: Sentry, run its detection mechanism against the paragraph. If triggered, flag it:

> "Sentry alert: [FM-XX name]. [What was detected]. [One-line description of the issue]."

Sentry checks are silent when they pass. Only flag when triggered.

---

## Phase 6 — Consolidate Artifacts

Synchronize the harness artifacts with the current state of the document. This phase has mandatory triggers — do not skip or defer it.

**Mandatory triggers (run Phase 6 when ANY of these occur):**
1. **A section is complete.** After the last paragraph in a section has been drafted and questioned, run Phase 6 before starting the next section. This is not optional.
2. **The writer says "let's stop here" or "save progress."**
3. **The writer shifts to a different section** out of sequence.
4. **10 paragraphs have been drafted** since the last Phase 6 run, regardless of section boundaries.

Do not wait for the writer to ask for a sync. The whole point of Phase 6 is that it catches drift the writer and AI are too close to notice.

**Synchronization checklist:**

1. **DECISIONS.md**: Update counts in the header table. Check for any Resolved decisions that the drafted text contradicts — if found, mark as Drifted and flag to the writer.

2. **FINDINGS.md**: Update counts. Check if any Pending findings have been addressed by the paragraphs drafted in this session — if so, verify the landing is substantive (not just form) and update to Landed with the text anchor. If the landing is hollow, mark as Diluted.

3. **MANIFESTO.md**: Check each Explicit-tier entry: has it landed in the text? If yes, update Status to Verified and add the text anchor. If an Explicit entry remains Missing after substantial drafting in its target section, flag: "M-XX hasn't landed yet. Is it still required?"

4. **Anchors**: List all anchors created during this stretch. Verify each one still matches the current paragraph text. If a paragraph was revised after its anchor was created, check for drift.

Present the synchronization as a brief report:
```
## Artifact sync

- Decisions: X active, Y open, Z drifted [flag any new drifts]
- Findings: X pending, Y landed this session [flag any dilutions]
- Manifesto: X explicit items verified, Y still missing
- Anchors: N new anchors created [list IDs]
```

---

## Phase 7 — Handoff

When the drafting session ends, produce a handoff note that serves as the re-entry point for the next session.

**Handoff format:**

```
## Session Handoff — [date]

**Drafted:** [What sections/paragraphs were drafted. Be specific: "§2 complete, §3 paragraphs 1-3"]

**Decisions made:** [List D-XX entries created or resolved this session]

**Open questions:** [List D-XX entries still Open, plus any questions raised but not yet formalized as decisions]

**Pending findings:** [List F-XX entries still Pending, especially any discovered this session]

**Anchors created:** [List A-NNNN entries with one-line descriptions]

**Session energy:** [One line from green/red spectrum: "mostly generative" / "mostly critical" / "balanced"]

**Next session should:** [Concrete suggestion for where to start. E.g., "Resolve D-04 (scope of methodology section) before drafting §4" or "Continue §3 from paragraph 4 — the claim about X needs evidence"]
```

The handoff note is not stored as a file. It is the last output of the session. Phase 2 of the next session will reconstruct context from the harness artifacts directly — the handoff note is for the writer's benefit between sessions.

If the writer asks to "save" or "checkpoint" mid-session, run Phase 6 (consolidate) and Phase 7 (handoff) but note "mid-session checkpoint, not a full handoff" so they know they can continue in the same session.
