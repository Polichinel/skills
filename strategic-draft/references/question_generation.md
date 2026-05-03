# Three-Question Mechanism

Every paragraph drafted during Phase 5 receives three questions — one per dimension — before the session moves on. The questions surface real content, not procedural compliance.

## The Three Dimensions

### 1. Ground Truth

Does this paragraph say something true, or something that sounds true?

Example questions (adapt to the paragraph — never use these verbatim):
- "What evidence supports [specific claim in the paragraph]?"
- "If [specific claim] were wrong, how would you know?"
- "What would someone who disagrees with [specific claim] point to?"
- "Is this [specific number/stat/comparison] sourced, or are we asserting it?"
- "You wrote [specific formulation] — is that actually the case, or is it what we want to be the case?"

Ground truth questions target the factual backbone. If the paragraph contains no claims (pure framing, transition), this dimension may yield a weaker question — that's fine, but consider whether a paragraph with no claims is doing real work.

### 2. Strategy

Does this paragraph serve the destination?

Example questions:
- "How does this paragraph advance the Reader's Takeaway?"
- "If we deleted this paragraph, what would the document lose?"
- "Does this support the primary argument or is it defensive hedging?"
- "Is this paragraph here because the reader needs it, or because we feel we should include it?"
- "Does this create a commitment we can't sustain later in the document?"

Strategy questions check alignment with MANIFESTO.md. A paragraph that "feels right" but doesn't serve the Reader's Takeaway is a dilution vector. A paragraph that creates an implicit promise the document won't fulfill is a credibility risk.

### 3. Reader Impact

Will the target reader receive what this paragraph intends to deliver?

Example questions:
- "Will [audience] understand [specific term/concept] without your context?"
- "What will [audience] do with this information? Can they act on it?"
- "Does this match the institutional language [audience] expects?"
- "Is this the level of detail [audience] needs, or are we over/under-explaining?"
- "If [audience] reads only this paragraph, what impression do they form?"

Reader impact questions check the gap between writer's intent and reader's reception. The most common failure mode here is the curse of knowledge — the writer knows the context, the reader doesn't.

## Rules for Question Generation

**Specificity is mandatory.** Every question must reference specific content from the paragraph. "Is this true?" is useless. "Is the claim that FAO's mandate covers X actually supported by [specific document]?" is useful. If you cannot make the question specific, the paragraph may be too vague to question — which is itself a finding.

**One question must be uncomfortable.** At least one of the three questions should be the one the writer would rather not answer. This is the question that, if answered honestly, might require rewriting the paragraph. If all three questions are easy, the paragraph may be too safe — it's not doing real argumentative work.

**Questions are offered, not imposed.** Present all three questions after the paragraph is drafted. The writer can:
- Answer one or more (the skill incorporates the answers)
- Say "move on" (the skill proceeds without answers — no penalty, no nagging)
- Say "good point, let me revise" (the skill waits for the revised paragraph, then asks three new questions on the revision)

**No generic fallbacks.** If you truly cannot generate a specific question for a dimension, skip that dimension for this paragraph. Two specific questions beat three generic ones. But if you routinely skip a dimension, that's a signal: ground truth skips suggest the paragraph is all framing with no claims; strategy skips suggest the paragraph's purpose isn't clear; reader impact skips suggest you don't know enough about the audience.

**Track which questions produce revisions.** When a question leads the writer to revise, note which dimension it came from. Over a session, patterns emerge:
- Many ground truth revisions → the writer is asserting without evidence (FM-07 risk)
- Many strategy revisions → the document structure needs work before more paragraphs are drafted
- Many reader impact revisions → the audience model may need updating (revisit MANIFESTO.md)

## Interaction with Anchors

When a question reveals that a paragraph dilutes a sharp formulation that was previously captured as an anchor (A-NNNN), flag this explicitly:

> "This paragraph softens the formulation in A-0003. The anchor says [exact quote]. The paragraph says [what it says now]. Is the softening intentional?"

This is the dilution defense mechanism in action. The anchor is the reference; the paragraph is being checked against it. If the writer confirms the softening is intentional, update or supersede the anchor. If not, the paragraph should be tightened.

## When to Skip Questions

- **Transitional paragraphs** (1-2 sentences connecting sections): Ask one strategy question ("does this transition serve the flow?"), skip the other two.
- **Direct quotes or cited material**: Skip ground truth (the source owns the claim), ask strategy and reader impact.
- **Writer explicitly says "rapid draft, questions later"**: Defer all questions. Record which paragraphs were drafted without questions, and present them as a batch when the writer is ready. Never silently drop deferred questions.

## Failure Modes to Watch

- **FM-01 (Comfort Smoothing)**: If answers to ground truth questions consistently appeal to "it's generally accepted" or "most people agree," the paragraph may be comfort-smoothed. Push for specific evidence.
- **FM-07 (False Grounding)**: If the writer cites a source but the question reveals the source doesn't actually say what the paragraph claims, flag immediately.
- **FM-14 (Register Contamination)**: If reader impact questions reveal that the paragraph's language doesn't match the audience's register, this is a contamination signal. Check MANIFESTO.md for the expected register.
