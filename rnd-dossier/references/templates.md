# Dossier Templates

Skeletons for `preregister` and `log`. The pre-registration and the log entry are the two ends of the Popperian loop and **must link to each other**. Negatives use the fuller postmortem and are recorded with the same prominence as wins.

---

## 1. Pre-analysis plan (`preregister`) — commit BEFORE running

```markdown
# Pre-Analysis Plan — <experiment name> (<risk/area id>)

**Date:** <YYYY-MM-DD> (pre-registered *before* execution)
**Dossier:** <link> · **Builds on:** <prior results / the design doc / an expert-method-review>

## 1. Hypothesis
H: <one sentence — the mechanism claim being tested>.

## 2. Intervention (the ONE variable)
<exactly what changes vs baseline; everything else held constant; behind which flag>.

## 3. Skepticism ledger
<every reservation we hold, numbered — especially ways this could "work" for the wrong reason,
or be a symptom-mask rather than a fix. Name the things you'd be embarrassed to have ignored.>

## 4. Pre-registered predictions
| Endpoint (primary first) | Prediction | Threshold (pass / fail) |

## 5. Falsifiers (pre-committed — any one fires ⇒ hypothesis rejected, not rescued)
- F1 — <ineffective>: <observation> ⇒ <conclusion>
- F2 — <works-but-degenerate>: <observation> ⇒ <conclusion>
- F3 — <control fails / confound>: <observation> ⇒ <conclusion>

## 6. Method
<model/data/config; controls; readout order (fast probe → full eval); run discipline>.

## 7. Decision rules
<for each falsifier outcome and the accept case: what we do next>.
```

Discipline: a **primary endpoint with a numeric pass/fail threshold**; a **control** that rules out the obvious confound; readout **cheap-before-expensive**.

---

## 2. Experiment-log entry (`log`) — record AFTER

```markdown
### EXP-NN · <short title> · <date> · <SUCCESS|FALSIFIED|INCONCLUSIVE>
- **Plan (pre-reg):** <link to the pre-analysis plan it tests>
- **Variable:** <the one thing changed>
- **Driver / artifact / results:** <script · artifact ts · results/log location>
- **Readout:** <fast-probe result> → <full metrics vs the locked baseline>
- **Verdict vs falsifiers (plan §5):** <which fired / none> ⇒ <SUCCESS / FALSIFIED / INCONCLUSIVE>
- **Decision:** <next step per plan §7>
```

Every entry **links its pre-registration** and states the **verdict against the pre-committed falsifiers** — that linkage is what makes the log a meta-evaluation corpus later. Newest at the bottom; never edit past entries except to add a cross-link.

---

## 3. Postmortem (for a FALSIFIED / negative result) — first-class, not buried

```markdown
# Negative Result — <what we tested> did NOT <claim>

**Status:** Hypothesis **FALSIFIED**. <one-line so-what>.
## 1. What we tested (and pre-registered)  — the §3.1 commitment + the falsifier
## 2. What happened — the data table; the pre-registered acceptance that failed
## 3. Decisive evidence — the cleanest, least-confounded observation and what it points to
## 4. Biases weighed (intellectual-honesty audit) — confirmation bias, confounds NOT ruled out, counter-hypotheses
## 5. What is / isn't established
## 6. Disposition — what stays, what's abandoned, what it redirects toward
```

A falsification is a *result*, not a failure. The postmortem records what the data said, what we'd been wrong to assume, and where it redirects the search — and it must read as honestly as a success would. (Exemplars in `reports/`: `postmortem_locked_dropout_negative_result.md`, `results_*_ablation.md`.)
