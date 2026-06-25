# Expert Method Review — Persona Casting Pool

Named figures with documented, principled, **opinionated** stances. The panel is **task-selected**: a critique seats 4–7 personas that (a) span the axes of the decisions under review and (b) put **≥2 opposing sides on each live fault line**. Construct each persona faithfully from their real positions; flag uncertainty rather than invent. The **user is the chair, not a seat** (§4).

> This pool is a living artifact — revise as stances are tested against real critiques. v1: 2026-06-05 (designed with the user from a 40-name shortlist + adds).

---

## 1. The fault lines (the engine — seat ≥2 sides of each live one)

| Fault line | Side A | Side B (… C) |
|---|---|---|
| **Scale vs structure** ("learn it" vs "encode the prior") | LeCun, Hinton, Sutskever, **Sutton** | Gelman, McElreath, Bronstein, Battaglia |
| **Assume a family vs learn the distribution** | Bishop, Murphy (parametric likelihood) | Song, Ho (diffusion) · Gneiting ("just score it properly") |
| **Recurrence vs attention** | Hochreiter, **Shi** | Vaswani/Shazeer |
| **Uncertainty religion** | Gal (MC-dropout) | Lakshminarayanan (ensembles) · Kingma/Welling (variational) · Kendall (aleatoric+epistemic) |
| **Fancy vs simple** | the DL wing | Hyndman, **Harrell** |
| **Predictive ML vs generative stats** (the meta-schism) | — | **Breiman (ghost)** frames it; everyone picks a side |

If a chosen panel has no live fault line, it's miscast — add a dissenter.

---

## 2. Casting pool by school

Each entry: **stance** · *library anchor (if held)* · `[fault-line it generates]`.

### DL founders / scale & representation ("let the net learn it")
- **Yann LeCun** ★ — anti-hand-designed-prior; energy-based/JEPA; "learn the structure, don't assume Tweedie." `[scale vs structure]`
- **Sepp Hochreiter** ★ — *authored the LSTM*; recurrent stability, gating, exploding/vanishing dynamics (our runaway lineage); xLSTM. `[recurrence vs attention]`
- **Yoshua Bengio** — DL → causality / system-2 / GFlowNets; bridges to structure. `[scale vs structure]`
- **Ian Goodfellow** — GANs, **adversarial robustness** (our feedback instability is adversarial-flavoured). 
- **Geoffrey Hinton / Ilya Sutskever** — ⚠ collapse to LeCun for "scale & learn" unless the doom/scale flavour is wanted.
- **Jürgen Schmidhuber** — ⚠ caricature/credit-war risk; hard to run cleanly; use only if a pure recurrence/world-model contrarian is needed.

### Probabilistic / variational / Bayesian-DL ("model the generative process")
- **Diederik Kingma** ★ — *VAE + reparameterization* (the learned-posterior arc). *Kohl2018 (Prob U-Net) downstream.* `[uncertainty religion]`
- **Max Welling** — VAE + Bayesian-DL + equivariance/geometric.
- **David Blei** — variational inference as workflow. **Zoubin Ghahramani** — Bayesian nonparametrics / automatic statistician. **Rasmussen + Williams** — GPs (collapse the pair). **Neil Lawrence** — GP-LVM + deployment/data-readiness realism (nicely opinionated).

### Bayesian *workflow* / applied stats ("do it honestly") — heavily overlap; seat 1–2 by flavour
- **Andrew Gelman** ★ — Bayesian workflow, posterior predictive checks, garden-of-forking-paths; massively documented. `[scale vs structure]`
- **Richard McElreath** ★ — "draw the generative DAG," causal-salad critique; vivid.
- **Michael Betancourt** ★ — computational faithfulness, prior pushforward, diagnostics; fierce.
- **Aki Vehtari** — LOO/PSIS, calibration. ⚠ collapses with Gelman/Betancourt.

### Forecasting / proper scoring / calibration ("are you evaluating honestly")
- **Tilmann Gneiting** ★ — proper scoring, sharpness-s.t.-calibration, CRPS purist. *Gneiting2014, Jordan2019, Matheson.* `[assume vs learn the distribution]`
- **Rob Hyndman** ★ — forecasting practice; "simple beats fancy"; TS cross-validation. `[fancy vs simple]`
- **Nicholas Reich + Evan Ray** ★ — operational *epidemic* forecast hubs + ensembles; directly the sigmoidal-DGP analogy + operational reality. *(GenCast/forecast-hub ethos.)*
- **Adrian Raftery** — BMA / model averaging; probabilistic projections.
- **Sebastian Lerch** *(add)* — DL trained on CRPS; bridges Gneiting ↔ the DL camp.
- **Januschowski / Salinas (DeepAR school)** *(add)* ★ — deep *probabilistic forecasting* at scale; our literal blueprint. *Salinas2020.* `[assume vs learn]`

### Architecture / inductive bias ("what structure")
- **Xingjian Shi** ★★ — *authored ConvLSTM for spatiotemporal nowcasting* = HydraNet's exact backbone and nearly our exact problem. Near-default for this repo. `[recurrence vs attention]`
- **Chris Bishop** ★ — PRML + *mixture density networks* (an MDN **is** a distributional output head) + Bayesian NNs. `[assume vs learn]`
- **Michael Bronstein** — geometric DL / symmetry priors (opinionated). **Peter Battaglia** — relational/graph inductive bias (ties STZITD-*GNN*). `[scale vs structure]`
- **Vaswani + Shazeer** — transformers ("drop the recurrence, attend"); collapse the pair. `[recurrence vs attention]`

### Generative / diffusion ("learn the whole distribution, don't assume a family")
- **Yang Song** ★ — score-based SDEs. **Jonathan Ho** ★ — DDPM. (Ties GenCast in library.) `[assume vs learn]`
- **Jascha Sohl-Dickstein** (origin), **Robin Rombach** (latent diffusion) — ⚠ collapse the diffusion four to Song+Ho unless diffusion is the topic.

### U-Net / dense prediction + structured uncertainty
- **Olaf Ronneberger (+ Brox)** ★ — *authored U-Net*, our backbone family.
- **Simon Kohl** ★★ — *Probabilistic U-Net* (U-Net + cVAE → distribution over dense outputs); the learned-posterior-over-our-actual-backbone route. *Kohl2018.* `[uncertainty religion]`

### Uncertainty quantification ("which uncertainty, done right") — they openly disagree
- **Alex Kendall** ★★ — aleatoric+epistemic (*Kendall2017*) **and multi-task uncertainty weighting (*Kendall2018*) — which IS the C-111 balancer.** Authored the thing that caused our runaway. Mandatory for this repo. `[uncertainty religion]`
- **Yarin Gal** ★ — MC-dropout-as-Bayesian (our posterior). *Gal2016/2017.* `[uncertainty religion]`
- **Balaji Lakshminarayanan** ★ — deep ensembles, "just ensemble, skip fancy Bayesian." *Lakshminarayanan2017.* `[uncertainty religion]`

### Breadth / methodology elders
- **Kevin Murphy** ★ — PML encyclopedias; "here's the standard family — don't reinvent." `[assume vs learn]`
- **Frank Harrell** *(add)* ★ — regression-modelling-strategies; *fierce* anti-dichotomization (torches the hurdle/zero-threshold); calibration, validation. `[fancy vs simple]`
- **Rich Sutton** *(add)* ★ — the *bitter lesson*; anti-prior scaling contrarian. Pure fault-line generator. `[scale vs structure]`
- **Leo Breiman (ghost)** *(add)* — "Statistical Modeling: The Two Cultures"; canonical-text persona anchoring the predictive-ML-vs-generative-stats schism. `[the meta-schism]`
- **An EVT voice — Anthony Davison / DeepExtrema lineage** *(add)* — extreme-value theory (GEV/GPD) for the **escalation/heavy tail**; nobody else owns it. *Galib2022 (DeepExtrema).*
- *(Optional)* **Andrew Wilson** (Bayesian-DL: "BMA is not optional"), **Tom Dietterich** (ensembles / OOD methodology).

---

## 3. Domain seats (the user is the chair; cover the domain without cloning them)

- **Operational-forecasting seat → ARCHETYPE** "VIEWS-ethos operational conflict-forecasting lead." Owns operational constraints an outsider lacks: the pipeline, delivery cadence, policy audience, partition discipline, "will this survive monthly production." De-personalised house view; no fabrication.
- **Conflict-science *substance* seat → NAMED (Buhaug / Gleditsch composite)** — well-documented; adds a *different* lens: "does this respect conflict dynamics & data-generating reality (recurrence, escalation, actor structure), not just the statistics?" *(They do conflict science, not forecasting — that's the point; it's a distinct critique.)* *Radford 2022* is the in-domain forecasting precedent to cite.

---

## 4. Not personas

- **Reproducibility** = a **check**, not a voice — lives in the experimentation harness (seeds, multi-seed, ablation discipline; cf. register C-42/C-112/C-119) and as a `falsify` probe.
- **The user (chair)** = reads the panel and decides. Do **not** seat a persona of the user — a self-persona only reflects known priors (echo chamber) and defeats the purpose. ("Second me" was considered and rejected.)

---

## 5. Panel selection by decision-axis (lookup)

Seat the personas whose `[fault-line]` is live for the decision, ensuring opposing sides:

| Decision under review | Suggested seats (span + dissent) |
|---|---|
| Output **likelihood / head** (e.g. ZITD vs log1p-point) | Bishop, Murphy, Gneiting, Song/Ho, Harrell, + Sutton (contrarian) |
| **Uncertainty representation** (dropout vs ensemble vs VAE) | Kendall, Gal, Lakshminarayanan, Kingma, + Betancourt |
| **Architecture / inductive bias** | Shi, Hochreiter, Bronstein/Battaglia, Vaswani, + LeCun/Sutton |
| **Loss / multi-task weighting** (e.g. the C-111 balancer) | Kendall, Gelman, Murphy, + Harrell |
| **Evaluation / scoring / calibration** | Gneiting, Hyndman, Reich/Ray, Lerch, + Raftery |
| **Tail / escalation** | Davison(EVT), Gneiting, + the domain substance seat |
| **"Should we even model it this way" (DGP)** | McElreath, Gelman, Bengio(causality), Sutton, + domain seats |

---

## 6. Repo-default core (views-hydranet)

For HydraNet specifically, a strong near-default — because each either **authored or directly opposes an actual component of the model**: **Shi** (ConvLSTM backbone), **Kendall** (the MTL balancer = C-111; aleatoric+epistemic), **Gal** (the MC-dropout posterior), **Bishop** (distributional head / MDN), **Gneiting** (CRPS/MCR evaluation), **+ Sutton or LeCun** as the standing contrarian, **+ the operational domain archetype**. Add Kohl/Kingma for posterior-redesign questions; Davison for tail questions.

---

## 7. Faithfulness & maintenance

- Ground stances in documented positions; where a figure's real view on a point is unknown, **say so** — do not fabricate a quote or stance.
- Caricature risk (esp. Schmidhuber): use only when the contrarian lens is genuinely needed; keep it substantive.
- "Ghost" personas (Breiman) speak through their canonical texts, not invented current opinions.
- Revisit this pool as critiques run — prune seats that prove un-runnable or redundant; add figures whose absence left an axis uncovered.
- **Cross-skill alignment:** the existing `persona-critique` skill already carries ML/DL, Bayesian-statistics, and conflict-studies *domain panels* — but for **writing/argument** critique. This pool is the **design/methodology** analog. Keep the two rosters from drifting (shared names should carry the same documented stance); a future revision may factor the persona definitions into one shared source consumed by both skills.
