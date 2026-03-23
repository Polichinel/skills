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
