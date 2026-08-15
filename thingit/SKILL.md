---
name: thingit
description: Runs a þing — the cross-repo deliberation protocol in views_platform/þingit/. Any repo session can open a matter, take its turn, or report status without the human authoring prompts or pasting content between sessions. Use when the user says "do a þing", "open a þing", "this needs deliberation and coordination", "take your turn", "þing status", or invokes /thingit. Do NOT use for single-repo decisions (write an ADR), for risk registration (use register-risk), or for code review.
trigger: /thingit
---

# /thingit — run a þing

`þingit` is a deliberation protocol for decisions that span repositories whose agent sessions cannot
talk to each other. The conversation happens through shared files. **The human is a scheduler, not a
translator** — they should never author a prompt or paste content between sessions. If you find
yourself asking them to, you are doing it wrong.

**Root:** `/home/simon/Documents/scripts/views_platform/þingit/`
**Read `<root>/README.md` in full before acting.** It is the protocol (v2) and it overrides anything
here that disagrees with it. This file tells you *which turn to take*; the README tells you *how*.

## Step 0 — orient, always

```bash
ROOT=/home/simon/Documents/scripts/views_platform/þingit
ls -d $ROOT/[0-9][0-9]_*/ 2>/dev/null          # the matters
cat $ROOT/<latest matter>/baton.md              # whose turn, what to do
pwd                                             # which seat you are: the repo you are running in
```

Your **seat** is the repository your session is running in (`basename $(git rev-parse --show-toplevel)`).
If you are running in `þingit/` itself, you are one of the two unstaked seats — the **lögsögumaðr**
(lawspeaker) or the **efasemdarmaðr** (doubter); `baton.md` and `þingmenn.md` say which is wanted.

Then dispatch on what the user asked:

| They said | Verb |
|---|---|
| "this needs a þing", "open a þing", "/thingit open" | **open** |
| "/thingit", "take your turn", or the baton names your seat | **turn** |
| "where is the þing", "/thingit status" | **status** |

---

## Verb: open

The user has told you a piece of work needs cross-repo deliberation, and may have suggested
participants. **You have the context on the matter — they do not. Do not ask them to write it.**
Everything below is yours to draft; you ask them only what they alone can decide.

1. **Read** `<root>/README.md`, then `<root>/_skeleton/þing.toml` and `_skeleton/þingmenn.md`.
   Skim the last matter's `final_decision.md` and `eftirmál_NN.md` §2 so you do not repeat its
   failures.
2. **Scaffold:** `cp -r <root>/_skeleton <root>/NN_<short_matter_slug>` (next free `NN`).
3. **Fill `þing.toml` yourself:** the `title` (one line, from your own context), `stefnandi` (you),
   `opened` (today), and a proposed **`weight`** — `lítill` for ≤3 seats and one reactive round,
   `fullt` for a cross-platform or irreversible matter. Fill `[skil] demand` with the concrete
   artifacts the verdict must produce.
4. **Fill `þingmenn.md` yourself:** one row per seat, from the participants the user suggested plus
   any seat you know has a stake they have not thought of — say so explicitly when you add one. The
   `Stake` column is required. Seat the **efasemdarmaðr** and the **lögsögumaðr** as `þingit` with
   stake `none`; they are sessions opened in `þingit/`, which is what makes them unstaked.
5. **Pin the sources** — this is the anchor that keeps the record re-verifiable:
   ```bash
   for r in <seated repos>; do
       printf '%s = "%s"\n' "$r" "$(git -C <root>/../$r rev-parse --short HEAD)"
   done >> <root>/NN_<matter>/sources.toml
   ```
6. **Write `orð_00.md`** — the summons. TL;DR of ≤5 lines first. The matter, why now, what you see
   **from your own seat** flagged as one view ("correct me"), the desired end state, and a template
   of questions every þingmaðr answers from its seat. Anchor claims about other repos as
   `repo@<short-sha>:path:line` using the shas you just pinned.
7. **Write `baton.md` last** (see "Every turn ends the same way").
8. **Report to the human in three lines:** the matter, the seats, and the single next action —
   *"open a session in `<repo>` and run `/thingit`"*. Nothing to paste.

**Ask the human only:** whether the roster is right, and the weight class if you are genuinely
torn. Propose a default for both. Never ask them to phrase the matter.

---

## Verb: turn

1. `cat <matter>/baton.md`. If `BATON:` names a seat that is not yours, **stop** and tell the user
   which session to open — do not speak out of turn.
2. If `BATON: HUMAN`, tell them which gate (G1–G4) is waiting and what it needs. Do not proceed.
3. Otherwise do the turn the baton describes, under the README's rules. What that means by phase:
   - **blind round** — react to `orð_00` **only**. Do not read your peers' `orð`. If you must name
     one (to take a free number, or to count quorum), do it in your front-matter, in a
     `## Blind-round disclosure` block, or in `## Baton` — nowhere else, and V16 checks this.
   - **reactive round** — read everything prior; answer the `ágreiningr` items assigned to your seat;
     state a position on every open item, because silence is not assent.
   - **synthesis** (lawspeaker only) — `sáttmál` (settled) + `ágreiningr` (open). Do not advocate.
     **Commit the previous version before you overwrite it.**
   - **aðgát** (doubter only) — what is *not* here. Close with "Claims I broke" **and** "Claims I
     tried to break and could not". A list of concerns is unfalsifiable; failed attacks are evidence.
   - **rýni** — the against-interest review, assigned by the lawspeaker to the seat with the most to
     gain from the drafted verdict. Argue against the clauses that favour you.
   - **dómr** (lawspeaker only) — `## What / Why / How` and the **smallest thing** that fixes the
     pain, both before the first `D`-clause.
4. Facts are about **your** seat. Grep your own code and cite `file:line`; flag anything about
   another repo as inference.
5. Respect the weight class's soft cap. Open with a TL;DR of ≤5 lines.

---

## Verb: status

`cat baton.md`, then `bash <root>/scripts/validate_thing.sh`. Report: whose turn, what phase, what
is owed by whom (`ágreiningr`), and any validator ERROR. Two or three sentences. Do not do the turn.

---

## Every turn ends the same way — this is the part that must not be skipped

The finishing agent carries the whole handoff, because it is the one with the context:

1. **Write `baton.md`.** `BATON:` the next seat (or `HUMAN` **plus the gate number**), `PHASE:`, one
   `DO NOW:` line, the **assigned `orð` number** for the next seat, and — since the next session runs
   `/thingit` and reads this file — what that seat owes, specifically. Name the items.
2. **Run `bash <root>/scripts/validate_thing.sh`** and fix every ERROR before you stop. Sixteen
   checks; they encode rules that decayed silently in þing 01.
3. **Commit** your `orð` (one commit per turn — the cadence is a rule, and V12 reports on it).
4. **Tell the human one thing:** which session to open next. Literally *"open a session in `<repo>`
   and run `/thingit`"* — no prompt for them to write, no text for them to paste.

## What the human does, and nothing more

Opens the named session, types `/thingit`, and decides at the four gates: **G1** matter/weight/roster
· **G2** naming an authority the verdict needs · **G3** ratification · **G4** execution hand-off.
Everything else is the assembly's work. If you are about to ask them for anything else, re-read the
README and find the answer yourself.
