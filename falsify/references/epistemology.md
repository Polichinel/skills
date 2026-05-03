# Falsification: Epistemological Framework

This document grounds the falsification audit in Popper's philosophy of science. Consult it when you are tempted to weaken a finding, design a probe you expect to pass, or declare a claim verified.

---

## Why Falsification

Karl Popper's central insight: a theory gains credibility not by accumulating confirmations but by surviving serious attempts to refute it. One black swan refutes "all swans are white" regardless of how many white swans you have observed.

Applied to software: passing tests confirms that the system does what you thought to check. It says nothing about what you did not check. A system with 100% test coverage and all tests green can still produce wrong answers -- if the tests verify the wrong things or miss entire categories of behavior.

The falsification audit fills this gap. It asks: given that everything looks correct, can I construct a specific scenario that proves it is not?

---

## The Confirmation Trap

The default mode in software quality is confirmation: "Does it work? Run the tests. Tests pass. It works."

This is dangerous because:
- Tests verify expected behavior under expected conditions
- They do not verify unexpected behavior under unexpected conditions
- They do not verify that documentation matches code
- They do not verify that governance policies are enforced
- They do not verify that the system produces correct answers for inputs nobody thought to test

The confirmation trap is not a failure of testing. Tests are necessary. The trap is believing that passing tests is sufficient evidence that a claim is true.

---

## Risky Predictions

A prediction is "risky" in Popper's sense when it could genuinely go either way. A probe where you already know the outcome is a ceremony, not a test.

**How to judge riskiness:**
- If you designed the probe after reading the code and seeing it handles this case: **not risky** (you are confirming what you observed, not testing the unknown)
- If you designed the probe from the claim alone, without looking at the implementation: **risky** (you do not know whether the implementation handles this case)
- If the probe targets a gap between what the documentation promises and what you suspect the code does: **risky** (the answer is genuinely uncertain)

The risky prediction step (Phase 5) enforces this discipline. You must state what you expect before looking. This prevents post-hoc rationalization: "I found this bug, and of course I would have predicted it."

---

## Claim Scope and the Omission Blind Spot

### The problem

A narrow claim like "the notation in §3 is correct" generates probes that examine §3's notation. Every probe is derived from the artifact's content. This is effective for finding errors in what is stated, but it is structurally incapable of finding errors of omission — things the artifact should address but does not.

A broader claim like "the argument is adequate for a stat.AP reviewer" generates probes that require knowledge of what stat.AP reviewers expect. Some of these probes will target content the artifact does not contain. This is the only way to detect omissions.

This is not a subjective preference for broad over narrow. It is a structural property of how hypotheses constrain probe generation. Narrow hypotheses constrain probes to the artifact's content. Broad hypotheses allow probes to be generated from the artifact's context — its field, its comparables, its audience's expectations.

### Lakatos on internal vs external adequacy

Imre Lakatos distinguished between a theory's internal consistency and its engagement with the research programme it claims to contribute to. A theory that is internally consistent but ignores established problems in its field is what Lakatos called "degenerating" — it is not engaging with the hardest challenges the programme faces. The most important criticism of a scientific theory is often not that it gets something wrong, but that it fails to address what its field requires.

Applied to auditing: an artifact that passes all internal-coherence probes but fails to address a known field requirement is analogous to a degenerating programme. The finding is not "you got X wrong" but "you did not address Y, and Y is required." This is a falsifying observation — the claim "this artifact is adequate for its field" is disproven by the absence of Y.

### When to push back on narrow claims

The auditor should accept narrow claims for rounds focused on internal correctness (notation, figures, code-doc alignment). But the auditor should also ensure that at least one round per audit campaign tests the artifact's relationship to its field. Specifically:

- If the user provides only narrow, artifact-internal claims across multiple rounds, the auditor should say: "These claims test internal correctness. They cannot detect omissions — topics the artifact should address but does not. I recommend adding a round with a broader claim like '[artifact] makes an adequate argument for [field/venue/audience]' to probe for gaps."
- If the user provides a readiness claim ("ready for publication," "ready for production," "ready for the next team to consume"), the auditor must treat this as requiring Category H (Adequacy) probes. Readiness claims are inherently about external expectations, not just internal correctness.
- If the user provides a claim that is so narrow it can only generate trivial probes (e.g., "line 47 is correct"), the auditor should suggest broadening to the function or module level.

### The two-pass discipline

For audit campaigns (multiple rounds on the same artifact), use two passes:

**Pass 1 — Internal coherence.** Narrow claims targeting the artifact's stated content. "Is the notation correct?" "Do the figures match the data?" "Does the code match the documentation?" These use Categories A–G.

**Pass 2 — External adequacy.** At least one broad claim targeting the artifact's relationship to its field. "Is the argument adequate for a [field] reviewer?" "Does the system address what comparable systems address?" This uses Category H.

Pass 2 should not be deferred to "after we finish Pass 1." Run at least one adequacy round early in the campaign — ideally round 2 or 3, not the final round. If Pass 2 reveals a major omission, it may reprioritise all remaining Pass 1 work.

---

## Anti-Patterns

### 1. "Tests pass, therefore done"

This is the confirmation trap applied as a decision criterion. Tests are a necessary condition for doneness, not a sufficient one. The falsification audit runs after tests pass precisely because it targets what tests miss.

### 2. Goodharting the probes

If you design probes that you already know will pass, you are optimizing for a clean report rather than for knowledge. A clean report from weak probes is worthless -- it provides false confidence.

Signs you are Goodharting:
- Every probe passes on the first try
- You chose to probe the parts of the system you are most confident about
- You avoided probing the parts that make you nervous

The cure: probe what makes you nervous. The best probe is one where you genuinely do not know the outcome.

### 3. Ad hoc rescue

When a probe falsifies the claim, the temptation is to save the claim by narrowing its scope: "That's an edge case," "No one would do that," "That's out of scope."

This is Popper's ad hoc modification -- changing the theory to fit the evidence rather than accepting that the evidence disproves the theory.

If the system does not handle an input correctly, the options are:
- Fix it (change the code)
- Document it (change the claim to exclude this case)
- Accept the falsification (the claim is not true as stated)

The option that does not exist: pretend you did not see it.

### 4. Skipping the re-audit

After fixing a falsification, the natural impulse is to re-test only the fixed probe. This is insufficient because:
- The fix may have broken something else (regression)
- The fix may have exposed a new edge case
- Other probes may now produce different results

Re-run all probes after fixing. This is the re-audit step.

### 5. Probing implementation instead of contract

A probe that checks "does line 47 call logger.error?" is testing implementation. A probe that checks "when I pass invalid input, does the log contain an ERROR entry?" is testing the contract.

Implementation probes are brittle -- they break when code is refactored even if behavior is preserved. Contract probes are durable -- they test what the system promises, not how it delivers.

Always probe the contract. The contract is what matters to consumers.

---

## The Survived/Falsified Distinction

The skill uses "SURVIVED" rather than "VERIFIED" or "PROVEN" for a claim that passes all probes. This word choice is deliberate.

"Survived" means: the claim withstood this specific set of attacks. A different set of attacks, or a more creative attacker, might still falsify it. The claim's credibility is proportional to the severity and diversity of the probes it survived.

"Verified" or "proven" would imply that the claim is established as true. No finite set of probes can establish this. There is always another edge case, another input, another interaction pattern.

This is not pedantry. It shapes how the audit results are interpreted:
- SURVIVED with 3 weak probes: low confidence
- SURVIVED with 7 diverse, risky probes: high confidence
- SURVIVED does not mean "stop looking": it means "this set of attacks failed to find a problem"

The goal of repeated audits is not to prove the claim true. It is to build sufficient confidence by failing to prove it false despite trying hard.
