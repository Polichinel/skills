---
name: expert-code-review
description: Provides multi-perspective engineering review of a codebase from 8 canonical expert viewpoints (Martin, GoF, Feathers, Nygard, Kleppmann, Ousterhout, Hickey, Beck) plus a Maintainer seat that judges sufficiency and removes findings not worth acting on, with failure mode analysis and long-term regret test. Use when user says "review this code", "critique the architecture", "evaluate this system", "assess code quality", "engineering review", or "what would Uncle Bob think". Do NOT use for repository mapping (use repo-assimilation), tech debt cleanup, bug fixes, or scaffolding.
---

# Multi-Expert Engineering Review

## Important

Follow these rules strictly.

- Do not merge expert perspectives. Evaluate each expert independently.
- Always follow the required output structure exactly.
- Ground every observation in specific files, modules, or code patterns. Do not give generic advice.
- Use specific observations tied to the system under review.
- Do not give high-level platitudes. Prefer concrete engineering consequences.
- When information is missing, explicitly state assumptions.
- If working from a repo-assimilation output, use it as starting context rather than re-reading the codebase from scratch.

## Purpose

Provide a critical multi-perspective engineering review of a software system.

The goal is insight and tension between perspectives, not consensus.

## Procedure

When given a system description or codebase:

1. Produce a short neutral system summary (3-5 sentences)
2. Evaluate the system from each of 8 expert perspectives separately -- consult `references/experts.md` for evaluation criteria per expert
3. For each expert: identify 2-4 strengths, 2-4 weaknesses/risks, and 1-3 concrete improvements (all with file/module references)
4. Complete all 8 expert reviews, then the Maintainer seat (`references/experts.md`), which speaks last and issues a sufficiency verdict, before proceeding
5. Identify key disagreements between expert perspectives
6. Perform failure mode analysis and long-term regret test -- consult `references/failure-modes.md` for categories and output format
7. Produce a balanced engineering recommendation

## Required Output Structure

1. System Summary
2. Expert Reviews
   - Robert C. Martin Perspective
   - Gang of Four Perspective
   - Michael Feathers Perspective
   - Michael T. Nygard Perspective
   - Martin Kleppmann Perspective
   - John Ousterhout Perspective
   - Rich Hickey Perspective
   - Kent Beck Perspective
   - The Maintainer Perspective (sufficiency verdict; findings judged not worth acting on)
3. Key Disagreements Between Experts
4. Failure Mode Analysis
5. Long-Term Regret Test
6. Engineering Recommendation

## Risk Register Integration

Format failure modes as concern entries (C-xx) and cross-expert disagreements as disagreement entries (D-xx) in register-compatible format (ID, tier, trigger, source, location, narrative). Do not append directly to the register — output the findings and let the user invoke `register-risk` to handle deduplication, tier validation, and registration.

## Principles

- Provide specific observations, not generic advice
- Identify trade-offs between perspectives
- Avoid vague language
- Prefer concrete engineering consequences

## Performance Notes

- Take your time. This is a thorough review.
- Quality is more important than speed
- Do not skip any expert perspective or combine them
- Every strength, weakness, and improvement must reference specific code
