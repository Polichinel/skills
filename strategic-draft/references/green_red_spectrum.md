# Green/Red Spectrum: Behavioral Tracking

The green/red spectrum tracks the oscillation between generative and critical modes during a drafting session. It is descriptive, not prescriptive — a mirror the skill holds up, not a gate it enforces.

## The Spectrum

| Position | Label | Writer behavior | AI behavior |
|----------|-------|-----------------|-------------|
| 0.0–0.2 | Pure green | Ranting, dumping ideas, providing raw material | Structuring, organizing, capturing formulations as anchors |
| 0.2–0.4 | Mostly green | Proposing content, answering questions | Asking clarifying questions, suggesting structure |
| 0.4–0.6 | Middle | Both questioning and proposing | Both questioning and proposing |
| 0.6–0.8 | Mostly red | Pushing back on proposals, challenging claims | Defending or conceding, providing evidence |
| 0.8–1.0 | Pure red | Stress-testing, trying to break AI's proposals | Defending with evidence or conceding honestly |

## How to Classify Each Exchange

Tag each exchange implicitly (never shown to the user) based on these signals:

**Green signals (writer generating, AI structuring):**
- Writer provides new content, ideas, or raw formulations
- Writer answers a question with substance (not just "yes/no")
- Writer directs ("let's talk about X", "the next section should...")
- AI asks questions, organizes material, proposes structure

**Red signals (writer challenging, AI defending):**
- Writer questions a proposal ("why did you...?", "I don't think...")
- Writer provides counter-evidence or counter-arguments
- Writer asks the AI to justify a choice
- AI defends a position with evidence or concedes

**Middle signals (balanced exchange):**
- Writer and AI both asking and answering
- Collaborative refinement where neither is clearly leading
- Back-and-forth on a specific point without clear challenge/defend dynamic

## Tracking Mechanism

Maintain a rolling window of the last 5 exchanges. Each exchange gets a score:
- Green: 0.0–0.3
- Middle: 0.4–0.6
- Red: 0.7–1.0

The session position is the mean of the rolling window.

Do not show the numerical position to the user. Do not announce "we are currently at 0.7 on the spectrum." The tracking is internal; only the trigger prompts are visible.

## Trigger Prompts

These are suggestions, not commands. The writer can ignore them.

**Sustained green (position < 0.2 for 3+ exchanges):**
> "We've been building — want to stress-test what we have so far?"

Only prompt once per sustained green stretch. If the writer declines or ignores, do not prompt again until the position naturally shifts red and back to green.

**Sustained red (position > 0.8 for 3+ exchanges):**
> "We've been challenging — ready to build on what survived?"

Same rule: prompt once, then back off.

**Sustained middle (position 0.4–0.6 for 5+ exchanges):**
No prompt. This is the healthy equilibrium. The skill should operate normally.

**Session-level summary (on handoff only):**
When the session ends (Phase 7), include a one-line note:
- "Session was mostly generative" (mean < 0.35)
- "Session was mostly critical" (mean > 0.65)
- "Session balanced generation and critique" (mean 0.35–0.65)

This goes into the handoff notes so the next session knows where the energy was.

## What the Spectrum Does NOT Do

- It does not block any action. The writer can stay pure green for an entire session if that's productive.
- It does not change the AI's behavior. The AI drafts, questions, and challenges the same way regardless of position.
- It does not judge. Pure green is not "worse" than balanced. Some sessions need pure generation; others need pure critique.
- It does not create transitions. The shift between green and red is organic, driven by the writer's choices, not by the skill's prompts.
