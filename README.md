# Resolution-Based Education (RBE)

> **Performance attainment is not necessarily certification resolution.**

Resolution-Based Education (RBE) is a decision-relative educational operating architecture for capability certification. It preserves existing outcomes, marks, programme structures, CO/PO/PSO mappings, approved assessment practices, and continuous-improvement processes, while adding an explicit evidential question before a capability-bearing certification claim is made:

**Does the available evidence distinguish learner possibilities that would require different certification decisions?**

This repository is the reference implementation and reproducibility support for:

**Akhtar, M. A. K. (2026). _Resolution-Based Education: A Decision-Relative Architecture for Capability Certification in the Generative-AI Era_ (Version V1). Zenodo. https://doi.org/10.5281/zenodo.22814101**

The educational architecture and its validity claims are defined in the paper and do not depend on a particular software interface.

## Scientific flow

```text
Existing OBE evidence
        ↓
Performance result
        ↓
RBE Resolution Gate
        ↓
   ┌────┴────┐
 adequate   inadequate
   ↓          ↓
 STOP        CARG
 zero         ↓
 added       MRRP / adaptive resolving evidence
 burden       ↓
         re-evaluate resolution
              ↓
        AR / AU / RN / Deferred
              ↓
 PAR / RR / RAR / UAR / RNR / MRB
              ↓
 Programme evidence → Passport → Ledger → Audit → Improvement
```

The formal adequacy condition is

```math
w_i \sim_A w_j \Rightarrow g(w_i)=g(w_j).
```

All learner possibilities that remain observationally indistinguishable under the available assessment evidence must require the same certification decision. If this already holds, RBE stops with zero additional RBE assessment burden. If it fails, a **Certification–Assessment Resolution Gap (CARG)** exists and additional evidence is targeted only at the unresolved decision-relevant ambiguity.

## RBE as a complete educational operating architecture

RBE is not a post-examination add-on and is not another attainment calculator. The complete architecture connects educational purpose to certification and renewal through nineteen operating stages.

| No. | Stage | Principal output |
|---:|---|---|
| 1 | Purpose and stakeholders | Mission, needs, constraints |
| 2 | Programme objectives | PEOs and review cycle |
| 3 | Graduate capabilities | POs/PSOs/graduate attributes |
| 4 | RCO design | `(C, E, P, D)` |
| 5 | Curriculum architecture | Curriculum/RCO map |
| 6 | Pedagogy | CCVRT learning design |
| 7 | Learning evidence | LE record |
| 8 | Performance assessment | Score/grade and initial evidence `K0` |
| 9 | Resolution Gate | Stop or unresolved status |
| 10 | CARG diagnosis | Explicit decision-relevant ambiguity set |
| 11 | Evidence acquisition | Admissible probe/policy candidates |
| 12 | MRRP and stopping | Resolved or Deferred |
| 13 | Certification state | AR, AU, RN, NA, Deferred |
| 14 | Student attainment | `RCA_ij` |
| 15 | Course evaluation | PAR, RR, RAR, UAR, RNR, MRB |
| 16 | Programme evaluation | PPO/RPO/UPO |
| 17 | Evidence records | Capability Passport and Resolution Ledger |
| 18 | Governance/QA | Audit trail and actions |
| 19 | Renewal | Closed-loop improvement |

The resolution layer is therefore embedded between performance evidence and capability-bearing certification rather than replacing the upstream educational system.

## Resolvable Capability Outcomes

For course capability `j`, RBE uses

```math
RCO_j=(C_j,E_j,P_j,D_j),
```

where:

- `C_j` — capability claim,
- `E_j` — relevant environments and tool conditions,
- `P_j` — admissible perturbation/evidence family,
- `D_j` — certification distinction.

An RCO enriches an existing course outcome rather than replacing it. The certification distinction supplies the decision-relative target against which evidence adequacy is tested.

## CCVRT pedagogy

RBE uses a compact learning-to-transfer cycle:

```text
Construct → Challenge → Verify → Revise → Transfer
```

CCVRT develops adaptability and evaluative judgement before those qualities are used in certification. It is not presented as a replacement for established active, authentic, reflective, or feedback-rich pedagogy.

## Learning evidence is not certification evidence

Learning evidence (LE) and certification evidence (CE) can overlap in observable form but differ in purpose. Feedback, collaboration, retries, hints, and AI assistance may be appropriate for learning while not being sufficient as the sole evidence for an independent capability claim.

RBE therefore does not impose a blanket AI-allowed or AI-banned rule. Tool conditions are defined relative to the RCO and the certification decision.

## Performance assessment is preserved

RBE preserves the institutionally approved performance scheme. It does **not** convert resolution into another marks component and does not average “resolution marks” into the original performance score.

The approved assessment produces the performance result and initial evidence state `K0`. RBE then asks whether that evidence is adequate for the certification distinction.

## Resolution Gate and CARG

Let `W` be certification-relevant learner worlds and `g: W → D` the certification rule. Under assessment protocol `A`,

```math
w_i \sim_A w_j
```

means that the worlds are observationally indistinguishable under the evidence obtainable through `A`.

Certification resolution requires

```math
w_i \sim_A w_j \Rightarrow g(w_i)=g(w_j).
```

A CARG exists when

```math
\exists w_i,w_j:\; w_i\sim_A w_j \land g(w_i)\ne g(w_j).
```

An unresolved record is not automatically a CARG. CARG is the structural case in which observationally compatible learner possibilities require different certification decisions.

**Unresolved is an evidential state, not an allegation of cheating, AI misuse, incompetence, or bad faith.**

## Conservative evidence reuse

RBE begins from evidence already produced by the approved educational system. If `K0` already resolves the required certification distinction,

```math
B_{add}(K_0)=0.
```

Thus resolution-adequate OBE is a zero-additional-evidence case of RBE. The framework does not automatically require a viva, second examination, or perturbation for every learner.

## Admissible perturbation families

When a CARG exists, additional evidence must target the unresolved distinction. Candidate families include constraint shifts, misleading or contradictory evidence, transfer, explanation/justification, resource or tool changes, uncertainty/defer decisions, and recovery after failure.

These are candidate evidence mechanisms, not RBE itself. Each must be validated against the RCO and local educational context.

## MRRP and finite stopping

A candidate probe `e` may have burden

```math
B_\lambda(e)=c(e)+\lambda L(e), \qquad \lambda\ge 0,
```

where `c(e)` represents direct assessment burden and `L(e)` represents assessment leakage.

A single informative question is not automatically an MRRP. RBE reserves **Minimum Resolution-Restoring Policy (MRRP)** for a probe or adaptive policy/tree whose terminal evidence reaches the declared resolution condition while satisfying validity, reliability, accessibility, fairness, privacy, leakage, construct, and maximum-burden constraints.

If no admissible continuation can restore resolution within the approved boundary, the case may be **Deferred** rather than forced into a false binary decision.

## Deterministic and probabilistic resolution

The deterministic formulation is the theoretical core: do the remaining compatible possibilities cross a certification-decision boundary?

For noisy evidence, a calibrated probabilistic implementation may use posterior decision risk

```math
r_t=1-\max_{d\in D}P(D=d\mid K_t).
```

Probabilistic resolution requires a defensible model, calibration evidence, and a declared threshold. Low risk alone does not imply positive attainment because the resolved decision may be negative.

## Certification states

| State | Performance | Resolution | Interpretation |
|---|---|---|---|
| AR | Attained | Resolved positive | Performance attained and evidence supports the positive certification decision |
| AU | Attained | Unresolved | Mark retained; certification evidence is not yet decision-sufficient |
| RN | Attained | Resolved negative | Performance attained but the declared capability decision resolves negatively |
| NA | Not attained | — | Existing performance criterion not met; local rules govern development/remediation |
| Deferred | Usually unresolved | Boundary/pending | No forced decision; authorised continuation or later review is required |

The same performance score can therefore coexist with different certification-resolution states without changing the original mark.

## Attainment mathematics

For learner `i` and RCO `j`:

```text
A_ij   = 1[S_ij >= T_j]
Q+_ij  = 1[resolution criterion met AND resolved decision = positive decision]
RCA_ij = A_ij * Q+_ij
```

Course reporting preserves performance and resolution separately through:

- `PAR` — performance-attained rate,
- `RR` — resolution rate,
- `RAR` — resolved-positive attainment rate,
- `UAR` — unresolved attained rate,
- `RNR` — resolved-negative attained rate,
- `MRB` — mean additional resolution burden.

When the performance-attained population is exhaustively partitioned into resolved-positive, unresolved, and resolved-negative states:

```math
PAR=RAR+UAR+RNR.
```

For programme compatibility reporting, mapped summaries `PPO`, `RPO`, and `UPO` preserve the distinction between conventional performance attainment and resolution-aware attainment. They are supporting indicators and do not automatically replace direct programme-level evidence for integrative capabilities.

## Capability Passport and Resolution Ledger

The **Capability Passport** is a learner-facing evidence summary additional to, not a replacement for, the statutory degree or marksheet.

The **Resolution Ledger** is the institution-facing provenance record for decision-relevant evidence, probes, responses, assessor/rubric versions, moderation, decisions, burden, and authorised audit fields.

Data minimisation is a design requirement: only evidence necessary for the declared educational and governance purpose should be retained.

## Governance and admissibility

Validity, reliability, accessibility, fairness, privacy, leakage, burden, transparency, moderation, appeals, and assessor calibration constrain what counts as admissible resolution evidence. Resolution rules, perturbation libraries, burden caps, and stopping/defer rules should be approved before consequential use and versioned for auditability.

RBE separates academic design, assessment administration, certification decision, appeal/adjudication, and quality audit as functions even where institutional roles overlap.

## Continuous improvement

Resolution patterns feed back into curriculum, pedagogy, assessment design, RCO specification, perturbation quality, assessor calibration, fairness controls, and governance. A high unresolved-attainment rate is a diagnostic signal, not automatically evidence of poor teaching.

The improvement loop is:

```text
Finding → cause → action → owner → deadline → re-measurement
```

## Novelty boundary

| Established object | Role inside RBE |
|---|---|
| Outcome-based education / constructive alignment | Supplies outcomes, mappings, performance evidence and initial evidence `K0` |
| Authentic assessment | Candidate evidence source |
| Oral defence / verification | Candidate perturbation/probe |
| Programmatic assessment | Compatible evidence architecture and strong comparator |
| Adaptive/sequential testing | Methodological ancestor for sequential evidence acquisition |
| Bayesian updating / information gain | Optional stochastic mechanism for resolution analysis |
| Resolution Gate | Tests decision-relative evidence adequacy |
| CARG | Identifies mismatch between assessment equivalence and required certification decisions |
| MRRP | Least-burden complete resolution-restoring policy under declared constraints |
| AR/AU/RN/NA/Deferred | Keeps certification-resolution status separate from the original mark |

RBE does **not** claim invention of authentic assessment, oral defence, programmatic assessment, adaptive testing, Bayesian updating, equivalence relations, information gain, abstention, or Pareto frontiers. Its contribution is the decision-relative resolution object and its integration into a complete educational evidence-to-certification architecture.

## Theory → reference implementation traceability

| Scientific object | Reference implementation |
|---|---|
| learner worlds and certification decisions | `rbe/models.py` |
| assessment equivalence / CARG | `rbe/resolution.py` |
| RCO | `rbe/models.py` |
| Resolution Gate | `rbe/resolution.py`, `rbe/engine.py` |
| MRRP | `rbe/mrrp.py` |
| resolved attainment and course metrics | `rbe/attainment.py` |
| audit and improvement checks | `rbe/audit.py` |
| conservative OBE evidence import | `rbe/workbook.py`, `rbe/obe.py` |

The implementation operationalizes the paper's objects; it does not redefine the educational theory.

## Reproducibility

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python experiments/reviewer_demo.py
python experiments/conservative_extension.py
python experiments/resolution_stagnation.py
python examples/run_theory_of_computation.py
python scripts/generate_artifacts.py
streamlit run streamlit_app.py
```

The mechanism demonstrations and software tests establish implementation behavior and reproducibility. They do **not** by themselves establish educational superiority.

Prospective educational validation should compare RBE against strong fixed/authentic and programmatic alternatives using certification error/risk, coverage, burden, transfer, error detection, constraint adaptation, misleading-AI resistance, reliability, accessibility, and subgroup effects.

## Citation

Please cite the RBE paper as:

**Akhtar, M. A. K. (2026). _Resolution-Based Education: A Decision-Relative Architecture for Capability Certification in the Generative-AI Era_ (Version V1). Zenodo. https://doi.org/10.5281/zenodo.22814101**

Repository citation metadata are provided in `CITATION.cff`.

## Author and license

**Mohammad Amir Khusru Akhtar**  
Usha Martin University, Ranchi, India

Copyright (C) 2026 Mohammad Amir Khusru Akhtar. Licensed under the Apache License, Version 2.0. See `LICENSE`.
