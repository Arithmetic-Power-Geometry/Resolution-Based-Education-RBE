# Resolution-Based Education (RBE)

> **Performance attainment is not necessarily certification resolution.**

RBE is a decision-relative extension of outcome-based education. It preserves existing marks, grades, CO/PO/PSO mappings and continuous-improvement evidence, then asks a separate question before a capability-bearing certification claim is made:

**Does the available evidence resolve every distinction required by the certification decision?**

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

In words: all learner possibilities that remain observationally indistinguishable under the available assessment evidence must require the same certification decision. If this already holds, RBE stops and adds no assessment. If it fails, a Certification–Assessment Resolution Gap (CARG) is present and additional evidence must be decision-targeted rather than automatically larger in volume.

## 3-minute reviewer demo

The Streamlit app contains a **Reviewer Demo** that exposes the central mechanism without requiring a workbook. Five learners deliberately show why a mark and a certification-resolution state are different objects.

| Learner | Score | Conventional performance | Resolution status | RBE state | Action |
|---|---:|---|---|---|---|
| A | 82 | Attained | resolved-positive | AR | stop; zero added burden |
| B | 82 | Attained | unresolved | AU | seek discriminating evidence |
| C | 82 | Attained | resolved-negative | RN | do not certify the capability |
| D | 55 | Not attained | — | NA | development / ordinary course process |
| E | 82 | Attained | unresolved at burden boundary | Deferred | do not manufacture certainty |

**The same performance score can therefore coexist with different certification-resolution states.** RBE does not change the original mark to express this distinction.

## What RBE adds—and what it does not claim to invent

| Established approach / object | Established role | RBE-specific use |
|---|---|---|
| Outcome-based education | outcomes, mapping and attainment | supplies the initial evidence state K0 |
| Authentic assessment | realistic performance | candidate evidence source |
| Oral defence / verification | targeted verification | candidate probe, not RBE itself |
| Adaptive testing | sequential evidence acquisition | methodological ancestor |
| Programmatic assessment | longitudinal, multiple evidence | strong comparator |
| Resolution Gate | — | tests decision-relative evidence adequacy |
| CARG | — | identifies a mismatch between assessment-equivalence and required certification decisions |
| MRRP | — | least-burden complete resolution-restoring probe or adaptive policy under declared constraints |
| AR/AU/RN/Deferred | — | keeps certification-resolution status separate from marks |

RBE does **not** claim invention of authentic assessment, oral defence, programmatic assessment, adaptive testing, Bayesian updating, equivalence relations, information gain, abstention or Pareto frontiers.

## Theory → software traceability

| Scientific object | Meaning | Reference implementation |
|---|---|---|
| `W` | certification-relevant learner possibilities | `rbe/models.py` |
| `A` | assessment protocol / evidence language | `rbe/resolution.py` |
| `w_i ~_A w_j` | assessment equivalence | `rbe/resolution.py` |
| `g(w)` | required certification decision | `rbe/models.py` |
| CARG | decision-incompatible worlds remain indistinguishable | `rbe/resolution.py` |
| `RCO=(C,E,P,D)` | resolvable capability outcome | `rbe/models.py` |
| Resolution Gate | stop or seek additional evidence | `rbe/resolution.py`, `rbe/engine.py` |
| MRRP | burden-constrained resolving evidence policy | `rbe/mrrp.py` |
| `Q+`, RCA | positive resolved attainment | `rbe/attainment.py` |
| PAR/RR/RAR/UAR/RNR/MRB | course reporting | `rbe/attainment.py` |
| audit | continuous-improvement checks | `rbe/audit.py` |
| OBE import | conservative-extension baseline | `rbe/workbook.py`, `rbe/obe.py` |

## Full operational workflow

The app retains the complete educational lifecycle but groups it into three scientific layers:

**I · Existing Education System** — OBE import → programme/course → CO/PO baseline → performance evidence.

**II · RBE Resolution Layer** — CO→RCO → Resolution Gate → CARG → MRRP/adaptive evidence → certification state.

**III · Evidence, Reporting & Improvement** — course/programme metrics → Capability Passport → Resolution Ledger → audit → validation/export.

This organization is deliberate: **RBE is a resolution layer over an existing evidence architecture, not a replacement attainment calculator.**

## Core attainment mathematics

For learner `i` and RCO `j`:

```text
A_ij   = 1[S_ij >= T_j]
Q+_ij  = 1[resolution criterion met AND resolved decision = positive decision]
RCA_ij = A_ij * Q+_ij
```

Operational states remain explicit: `AR`, `AU`, `RN`, `NA`, `Deferred`. Course reporting includes `PAR`, `RR`, `RAR`, `UAR`, `RNR`, `MRB` and Deferred rate. When performance-attained cases are exhaustively partitioned into resolved-positive, unresolved and resolved-negative states:

```text
PAR = RAR + UAR + RNR
```

## Reproduce the mechanisms

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

`experiments/reviewer_demo.py` reproduces the equal-score/different-resolution demonstration. `experiments/conservative_extension.py` verifies the zero-added-burden constructed case. `experiments/resolution_stagnation.py` demonstrates why repeating a non-discriminating observation need not resolve a decision distinction. These are mechanism demonstrations, not claims of educational effectiveness.

GitHub Actions executes the repository test suite and artifact generation on pushes and pull requests.

## Validation layers

The project deliberately separates:

1. **Software validation** — implementation and scientific-invariant tests.
2. **Calculation/reproduction validation** — workbook and declared example reproduction.
3. **Educational validation** — prospective comparison against strong alternatives.

The first two do not establish the third. See `docs/VALIDATION_LAYERS.md`.

Strong educational comparisons should report certification error/risk, coverage, burden, transfer, error detection, constraint adaptation, misleading-AI resistance, inter-rater reliability and subgroup effects. If RBE does not improve the relevant risk–coverage–burden frontier against strong comparators, superiority is not demonstrated.

## Reviewer navigation

- `docs/REVIEWER_GUIDE.md` — five-minute scientific reading path.
- `docs/NOVELTY_MAP.md` — explicit novelty/prior-concept boundary.
- `docs/SCIENTIFIC_WORKFLOW.md` — decision flow and stop/failure rules.
- `docs/VALIDATION_LAYERS.md` — software vs reproduction vs educational evidence.
- `docs/REVIEWER_CHECKLIST.md` — compact reproducibility/claim-control checklist.
- `docs/README_Q1_REVIEW_PATH.md` — shortest Q1-review path.
- `tests/test_scientific_invariants.py` — executable internal scientific relationships.

## Theoretical foundation

**Mohammad Amir Khusru Akhtar (2026). _Beyond Outcome Attainment: Resolution-Based Education and the Certification–Assessment Resolution Gap in the Generative-AI Era._**

DOI: `10.5281/zenodo.22797079`

This repository implements the foundation as an educational operating and reproducibility architecture. The foundation supplies CARG, the certification-resolution necessity condition, conservative evidence reuse, the distinction between one-step probes and complete resolution-restoring policies, and resolved-attainment mathematics; the software operationalizes these objects rather than re-presenting them as separate novelty claims.

## Citation

Please cite the foundation paper above when using the RBE theory. Repository/software citation metadata are provided in `CITATION.cff`.

## Author and license

**Mohammad Amir Khusru Akhtar**  
Usha Martin University, Ranchi, India

Copyright (C) 2026 Mohammad Amir Khusru Akhtar. Licensed under the Apache License, Version 2.0. See `LICENSE`.
