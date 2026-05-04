# Review Harness: Detailed Phase Instructions

## Sync Mode

### Phase 1 — Locate Harness and Document

Find the harness and the document it tracks.

1. Search for `_dev_materials/*/DECISIONS.md`
2. If multiple harnesses exist, list them and ask which one to sync
3. If no harness exists, stop: "No writing harness found. Run `/writing-harness` or `/strategic-draft` to create one."
4. Read the DECISIONS.md header to identify the document name
5. Find the document file — look for the most likely candidate:
   - A `.md` file in the project root or `docs/` matching the document slug
   - A file referenced in MANIFESTO.md text anchors
   - Ask the writer if ambiguous: "Which file is the current document?"

If the document file doesn't exist yet (harness was created but drafting hasn't produced a file), note this and proceed with artifact-only checks (internal consistency, not document comparison).

---

### Phase 2 — Audit DECISIONS.md

Read every entry. For each, compare its status against the document text.

**Open entries — are they actually still open?**

For each Open decision, search the document for text that resolves the question. Signs of implicit resolution:
- The document consistently uses one option from the decision's alternatives
- A section is structured in a way that presupposes the decision
- The scope boundary described in the decision is reflected in what the document covers

If the text has implicitly resolved an Open decision, propose: "D-XX appears resolved by §N — the text [specific evidence]. Propose Status: Resolved."

**Resolved entries — has the text drifted?**

For each Resolved decision, check whether the document still reflects the decision. Signs of drift:
- Text contradicts the recorded decision
- A later section uses a different framing than the decision specified
- The decision's scope boundary is violated by new content

If drift is found, propose: "D-XX has drifted — decision says [X], but §N now says [Y]. Propose Status: Drifted."

**Drifted entries — has the drift been addressed?**

For each Drifted decision, check whether a subsequent revision has brought the text back into alignment or whether the decision should be superseded.

**Header counts:** After auditing all entries, verify the header table counts (Total, Active, Drifted) match the actual entries.

---

### Phase 3 — Audit FINDINGS.md

Read every entry. For each, compare its status against the document text.

**Pending entries — have they been addressed?**

For each Pending finding, search the document for text that addresses the finding. Two possible outcomes:
- **Substantively addressed:** The document now contains content that directly responds to the finding. Propose Status: Landed, with the text anchor (section, paragraph, specific quote).
- **Superficially addressed:** The document contains text that appears to address the finding but lacks substance — hedging language, vague generalities, or form without content. Propose Status: Diluted, with evidence of what's missing.

**Landed entries — are they still substantive?**

For each Landed finding, re-verify that the text anchor is still accurate and the content is still substantive. Subsequent revisions can erode a landing. If a Landed finding has been diluted, propose Status: Diluted.

**Diluted entries — have they been re-sharpened?**

For each Diluted finding, check whether subsequent revision has restored substance. If so, propose Status: Landed with updated text anchor.

**Header counts:** Verify the header table counts match actual entries.

---

### Phase 4 — Audit MANIFESTO.md

Read every entry across all three tiers. Compare against the document text.

**Explicit tier — have they landed?**

For each Explicit entry:
- If Status is Active or Missing: search the document for text that states this point. If found, propose Status: Verified with text anchor.
- If Status is Verified: re-check the text anchor. Has the text been revised away?

**Flexible tier — is the current choice reflected?**

For each Flexible entry, check whether the document reflects the recorded choice (Explicit or Implicit). If the choice has flipped without updating the manifesto, flag it.

**Implicit tier — have they been breached?**

For each Implicit entry:
- Read the Breach detection field (specific phrases or patterns)
- Search the document for those phrases or patterns
- If found, propose Status: Breached with the location: "M-XX breached in §N — text says [specific phrase] which surfaces what should stay implicit."

This is the most important check for strategic documents. A breached implicit entry can undermine the document's strategy.

**Reader's Takeaway:** Re-read the Reader's Takeaway. Does the document, as currently drafted, deliver this destination? If not, flag: "The document does not yet deliver the Reader's Takeaway. [Specific gap]."

---

### Phase 5 — Report

Produce the Sync Report in the format specified in SKILL.md. Include:
- Every proposed status change with evidence
- Drifted anchors with the old and new formulations
- Updated header counts
- A summary line per artifact type
- The verdict (IN SYNC / STALE / SIGNIFICANTLY STALE)

End with: "Want me to apply these updates?"

---

### Phase 6 — Apply Updates

Only after user confirms. For each approved change:

1. Update the entry's Status field
2. Update or add text anchors
3. Add drift log entries to DECISIONS.md where applicable
4. Add "What happened" to FINDINGS.md Diluted entries
5. Update header counts in all artifact files

Do not create new entries. Do not delete entries. Only update statuses, anchors, counts, and log fields.

---

## Prioritize Mode

### Phase P1 — Load Harness State

Read all harness artifacts and build a summary:

- DECISIONS.md: count by status (Open, Resolved, Drifted, Superseded)
- FINDINGS.md: count by status and severity
- MANIFESTO.md: count by tier and status
- Anchors: total count, any marked Superseded
- Document: which sections exist, rough completion estimate

If the harness has zero entries across all artifacts, stop: "The harness is empty — nothing to prioritize. Either drafting hasn't started, or artifacts weren't being created during drafting. Run `/strategic-draft` to begin."

---

### Phase P2 — Score Open Items

Rank all open items by urgency. The ranking is not mechanical — use judgment about what blocks what — but follow this priority order as a starting framework:

**Tier 1 — Blocking:**
- Open decisions that block drafting of undrafted sections (e.g., "we can't write §3 until we decide the scope of the methodology")
- Drifted decisions in already-drafted sections (text contradicts a recorded decision — this needs resolution before further work makes the drift worse)
- Critical-severity Pending findings

**Tier 2 — Important:**
- Explicit manifesto entries still Missing after their target section is drafted
- Substantive-severity Pending findings
- Diluted findings that need re-sharpening

**Tier 3 — Maintenance:**
- Editorial-severity Pending findings
- Flexible manifesto entries whose current choice needs review
- Stale text anchors

Items in Tier 1 should be addressed before the next drafting session. Items in Tier 2 can be addressed during drafting. Items in Tier 3 can wait for a dedicated cleanup pass.

---

### Phase P3 — Identify Dependencies

Map which open items depend on other open items:

- Does resolving D-XX depend on resolving D-YY first?
- Does a finding's resolution depend on a decision that's still open?
- Does an undrafted section depend on decisions that haven't been made?

Present dependencies as: "D-04 depends on D-02 — resolve D-02 first."

Also identify external dependencies — items that require information the writer needs to get from outside the document (data, feedback from collaborators, institutional approval).

---

### Phase P4 — Report

Produce the Prioritize Report in the format specified in SKILL.md.

The report must be opinionated. Do not present a flat list. The writer needs:
1. **One clear next action** (even if it's "resolve D-XX before anything else")
2. A short list of what to do after that
3. Deferred items with honest rationale for deferral

End with a one-sentence recommendation: "Start the next session by [specific action]."
