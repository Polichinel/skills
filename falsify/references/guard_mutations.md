# Guard Mode: Mutation Categories and Procedure

Guard mode inverts the skill. Claim mode attacks a claim about behaviour. **Guard mode attacks the
guard**, and the claim it falsifies is always the same one, never stated by the user because nobody
ever states it:

> *This guard would catch the defect it was written for.*

The probe is a mutation: a change to **production** code that should break the guard. A mutation the
guard does not notice is a survivor, and every survivor is a defect the guard is credited with
catching and does not.

---

## The rule that makes this work

**The auditor must not be the author.**

This is the entire mechanism, and it is measured rather than assumed. In views-postprocessing
(2026-08-12) *"five parallel reviewers on #242 found what four rounds of self-review had not,"* and
the adversarial reviewer briefed only to supply mutants the author had not thought of was recorded
as *"the single highest-value input of the arc."* The same incident measured the failure directly:
the author proposed **thirteen** evasion forms and proved all thirteen caught; an independent review
proposed **twenty-nine**. views-frames recorded a check that could pass vacuously in three ways, and
*"every one of them was found by someone other than its author."*

A guard is written from the author's model of how the code fails. So is the author's test of that
guard. Auditing your own guard re-runs the model that already missed the defect.

**Therefore: run guard mode in a subagent with a clean context.** It receives the guard, the
production code, and nothing else — not the conversation that produced them, not the plan, not the
reasoning, not the register entry explaining what the guard is for. If you cannot isolate the
context, say so in the report and mark every verdict `UNVERIFIED (not independent)`. A guard audit
performed by the author is worth approximately nothing and must not be reported as though it were.

---

## Mutation categories

Each category below is derived from a failure recorded in this platform, cited. These are not
hypothetical failure modes. Where a category has an established name in Meszaros's *xUnit Test
Patterns*, it is given as a pointer, not as a substitute for the local evidence.

### M1 — Vacuous by construction

The assertion cannot be false regardless of what the code does.

*Probe:* Read the assertion's operands. Can the asserted condition ever hold given the types and
shapes the code actually produces? Then delete the production fix entirely. If nothing breaks, the
guard is decorative.

*Recorded:* views-faoapi's contract guard, added **for the empty-delivery incident**, asserted
`df.shape[1] == 0` against a frame that always carries nine geography columns — it could never fire.
views-pipeline-core: *"`assert_not_called()` was vacuous, since that mock could not have been called
whatever the code did."*

*xUnit name:* Assertion-Free Test.

### M2 — Tests the stub, not the code

The guard passes because the fixture constructs a shape production never produces.

*Probe:* Compare the fixture's construction against a real value taken from the running system. If
the guard's input cannot arise in production, the guard tests an imaginary program.

*Recorded:* views-faoapi — *"its test stubbed a shape the real code never produces."*

### M3 — Asserts on source text, not behaviour

The guard greps a file, matches an AST node, or inspects a docstring instead of exercising the
property.

*Probe:* Rename a variable, reword a comment, reformat, or switch an equivalent literal form
(set → JSON, single → double quotes). If the guard breaks, it was testing text. Then make the
behaviour wrong while leaving the text intact. If the guard stays green, it never tested behaviour
at all.

*Recorded:* views-faoapi — three tests asserted on source text; one grepped a comment for the words
*"still"* and *"servable"*, and its replacement matched the wrong block. views-models — a check
*"AST-matched a set literal and went vacuous once create_catalogs switched to JSON"*; another's
*"test regex finds zero matches, so the offset check vacuously passes."*

### M4 — Checks conformance to a declaration, never the declaration

The guard verifies the code matches a declared list, dict, or contract — and nothing verifies the
declaration.

*Probe:* Corrupt the **declaration**, not the code. Add a cycle to the declared graph. Remove a real
package from the allow-list. If the suite stays green, the guard enforces whatever it is told, and
the thing it is told is unguarded.

*Recorded:* views-datafactory C-350/C-351 — *"an assertion about conformance standing in for an
assertion about the property"*; the allow-list was checked against the code, and nothing checked the
allow-list. views-crafdapi records the decayed form: *"the assertion may have gone vacuous against
changed source — the suite reports the same thing either way."*

### M5 — The author's enumeration

The guard checks a hand-written list of cases, and the list is the author's imagination.

*Probe:* Do not test the listed cases. Generate cases the author did not list — other spellings,
other encodings, other call sites, other file types — and check whether the guard's coverage claim
survives contact with them.

*Recorded:* views-postprocessing — *"Fifteen of twenty-nine markdown assignment forms escaped the
no-copy scan. The author proposed thirteen forms and proved all thirteen caught."*

### M6 — Correct, and never runs

The assertion is sound. Nothing executes it, or it executes against the wrong target.

*Probe:* Trace the guard to a scheduler. Is it in CI? Is it skipped, marked, gated behind a flag,
excluded by a path filter, or pointed at a route the defect is not on? Delete the guard's file
entirely and re-run CI. A green build means the guard was never load-bearing.

*Recorded:* views-faoapi — *"`smoke.py check_coverage` — the assertion was correct — but runs only
when a human deploys, and points at `/subset`"*, while the defect was on `/latest`. The skills
repository's own C-15 is the same shape: the only check that catches C-01 is skipped in CI.

### M7 — Fires, and reports wrongly

The guard detects correctly and then does damage or misleads in its reporting path.

*Probe:* Force the guard to fail. Read what it emits. Does it leak the value it protects, name the
wrong file, point in the wrong direction, or emit a message that would send a reader to the wrong
place?

*Recorded:* views-postprocessing — *"The guard against publishing a coordinate value printed it"*, on
the single event it exists for, into a world-readable CI log. Two directional pointers in the same
commit *"both pointed the wrong way."*

---

## Procedure

Guard mode replaces phases 1–8 of claim mode. Phases 9 (Pattern Analysis) and 10 (Report) are
unchanged.

**G1 — Isolate.** Confirm the context is clean and the auditor is not the author. If not, stop, or
proceed with every verdict marked `UNVERIFIED (not independent)`.

**G2 — Resolve scope, then locate the guards.**

The default scope is **the changeset, not a path.** Nobody remembers test filenames, and a tool that
requires one is a tool for a person who reads test files rather than one who commissions them.

| invoked as | scope |
|---|---|
| `/falsify guard` | every guard **added or modified** on this branch versus its base — the same scope `/review-diff` takes |
| `/falsify guard <commit-ish>` | guards touched by that commit or range |
| `/falsify guard <path or glob>` | that path, for when you do know where to look |

Resolve the branch base the way `review-diff` does (`git merge-base HEAD <default-branch>`), diff for
changed test files, and enumerate every assertion inside them. New guards matter more than old ones:
a guard added in this changeset has never been observed to fail, which is the condition M1 exists for.

Report the count and how it was derived. A guard nobody enumerated cannot be audited, and a scope
that silently resolved to zero guards must say so rather than returning a clean sheet.

**G3 — Infer the defect each guard exists to catch.** From the guard alone — its name, its
assertion, its file. **Do not read the register entry, ADR, or commit message that explains it.**
Those carry the author's model, which is the thing under test. If the guard's purpose cannot be
inferred from the guard, that is itself a finding.

**G4 — Design mutations before running anything.** For each guard, select categories from M1–M7 and
write the mutations out. Predict for each: caught or survives. Committing the prediction first is
what separates this from a review, and it is mandatory — the same rule as claim mode's Phase 5.

**G5 — Apply and run.** Each mutation is applied to production code, the guard is executed, and the
result is recorded. **Reasoning about whether a mutation would be caught is not a result.** If a
mutation cannot be run — no environment, no fixture, too costly — record it as `UNRUN`, never as
caught. `UNRUN` is not a passing grade.

**G6 — Revert.** Every mutation is reverted. Confirm the tree is clean before reporting. Guard mode
modifies production code temporarily and must leave nothing behind.

**G7 — Verdict per guard.**

| verdict | meaning |
|---|---|
| **DECORATIVE** | Deleting the fix it protects breaks nothing, or the assertion cannot be false. The guard provides no protection and is counted as coverage. |
| **WEAK** | One or more mutations survived. The guard catches less than it is credited with. List each survivor. |
| **HOLDS** | Every mutation attempted was caught. |
| **UNVERIFIED** | Not independent, or mutations could not be run. |

`HOLDS` carries the same caveat as claim mode's `SURVIVED`: it withstood *these* mutations, chosen by
*this* auditor. It is not proof of sufficiency. Where a guard's coverage claim is enumerative (M5),
say plainly how many cases were tried against how many are believed to exist.

---

## Anti-patterns

- **Auditing your own guard and reporting it as independent.** The failure this mode exists for.
- **Counting `UNRUN` as caught.** Silence is not detection — the same error that let a service return
  `200` with no data for eight weeks.
- **Reporting mutation counts without naming survivors.** *"14 of 15 caught"* is not actionable; the
  one survivor is the whole result.
- **Stopping at the first survivor.** Run the full set. The distribution across M1–M7 is what tells
  you whether this is one bad guard or a systemic habit.
- **Grading generously because the guard was hard to write.** Effort is not protection.
- **Building a mutation framework.** Reverting the fix and re-running the guard is a two-minute
  manual check and it caught four dead guards in views-faoapi. Scope any tooling to the diff, never
  the repository — views-faoapi's Action 11: *"Do not build monitoring larger than the thing it
  monitors."*
