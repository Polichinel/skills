# Expert Perspectives: Evaluation Criteria

## Robert C. Martin -- Clean Code / Clean Architecture

Evaluate:
- Readability and naming clarity
- Function cohesion and size
- SOLID principles
- Separation of concerns
- Dependency direction
- Architectural boundaries

Identify:
- Technical debt
- Hidden coupling
- Unclear abstractions
- Code structures that make reasoning difficult

Focus on developer ergonomics and maintainability.

---

## Gang of Four -- Design Patterns

Evaluate structural design.

Assess:
- Object collaboration
- Responsibility distribution
- Pattern usage (correct, incorrect, or unnecessary)
- Coupling and reuse
- Extensibility

Identify:
- Rigid structures
- Excessive coupling
- Incorrect or unnecessary pattern usage

Focus on extensible architecture and clear object structure.

---

## Michael Feathers -- Legacy Code & Safe Change

Evaluate change safety.

Identify:
- Code that is difficult to test
- Areas risky to modify
- Tight coupling
- Missing seams for refactoring

Recommend strategies for incremental improvement without breaking the system.

Focus on safe evolution of existing systems.

---

## Michael T. Nygard -- Production Reliability

Evaluate runtime behavior.

Assess:
- Failure modes
- Cascading failures
- Dependency fragility
- Retry storms
- Resource exhaustion

Check for resilience mechanisms:
- Timeouts
- Circuit breakers
- Load shedding
- Graceful degradation

Focus on system survivability under stress.

---

## Martin Kleppmann -- Data Systems & Correctness

Evaluate system guarantees.

Assess:
- Consistency
- Concurrency handling
- State management
- Ordering assumptions
- Scalability of data flows

Identify hidden assumptions about timing, ordering, or synchronization.

Focus on correctness and reliability of data processing.

---

## John Ousterhout -- Complexity Management

Evaluate complexity control.

Assess:
- Module boundaries
- Abstraction depth
- Complexity containment

Identify modules that leak complexity across the system.

Focus on reducing cognitive load for future engineers.

---

## Rich Hickey -- Simplicity vs Complexity

Evaluate conceptual simplicity.

Identify:
- Unnecessary coupling
- Conflated concepts
- Incidental complexity
- Designs that increase cognitive burden

Distinguish between simple systems and merely familiar ones.

Focus on clear conceptual models.

---

## Kent Beck -- Test-Driven Development

Evaluate development feedback loops.

Assess:
- Testability of components
- Safety of incremental change
- Presence of automated tests
- Brittleness of existing tests

Identify areas where tests are missing, difficult to write, or fragile.

Focus on designs that enable safe iteration.
