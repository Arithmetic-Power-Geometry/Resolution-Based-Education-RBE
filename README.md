# Resolution-Based Education (RBE)

A reference software and reproducibility implementation of **Resolution-Based Education (RBE)** for curriculum, learning, assessment, certification resolution, attainment, programme evaluation and continuous improvement.

> **Education must distinguish performance measurement from certification resolution.**

RBE preserves existing outcomes, marks, grades, credits, CO/PO/PSO mappings and continuous-improvement practice. It adds a decision-relative certification layer: before a capability-bearing claim is made, the available evidence should resolve the distinctions that the claim requires.

## Final software workflow

The Streamlit laboratory implements a guided 12-stage workflow:

`OBE workbook → programme/course → CO→RCO → performance evidence → Resolution Gate → CARG/MRRP → RBE attainment → PO/PSO comparison → Capability Passport → Resolution Ledger → audit/improvement → validation/export`

The app can directly import the supplied Theory of Computation workbook structure with the sheets `FLAT`, `Matrix`, `CO Calculation` and `PO Calculation`. It recomputes the existing OBE baseline before adding RBE. This is deliberate: **RBE extends OBE; it does not erase it.**

## Core RBE objects

- Resolvable Capability Outcome: `RCO=(C,E,P,D)`
- Outcome–Resolution Separation: `Outcome Attainment ⇏ Certification Resolution`
- Deterministic resolution: all still-compatible learner worlds imply the same required decision
- Probabilistic extension: `r_t = 1 - max_d P(D=d | K_t)`
- CARG: certification-incompatible worlds remain observationally indistinguishable under the current protocol
- Resolution Gate: stop immediately when current evidence is already adequate
- Adaptive evidence: select admissible discriminating evidence under burden, accessibility, reliability, fairness, leakage, privacy and construct constraints
- Finite stopping: unresolved cases may be explicitly Deferred rather than forced into a claim

## Attainment

For learner `i` and RCO `j`:

```text
A_ij   = 1[S_ij >= T_j]
Q+_ij  = 1[resolution criterion met AND resolved decision = positive decision]
RCA_ij = A_ij * Q+_ij
```

Operational states remain visible: `AR`, `AU`, `RN`, `NA`, `Deferred`.

Course reporting includes `PAR`, `RR`, `RAR`, `UAR`, `RNR`, `MRB` and Deferred rate. When performance-attained cases are exhaustively partitioned into resolved-positive, unresolved and resolved-negative:

```text
PAR = RAR + UAR + RNR
```

Programme-level RBE reporting uses mapped `PPO`, `RPO` and `UPO`, while preserving the underlying evidence and avoiding false precision from mapping weights.

## Existing OBE workbook validation

The importer reproduces the supplied Theory of Computation workbook's rounded CO results:

| CO | Mean normalized score | Mean attainment (0–3) |
|---|---:|---:|
| CO1 | 0.48 | 1.75 |
| CO2 | 0.52 | 2.10 |
| CO3 | 0.45 | 1.46 |
| CO4 | 0.57 | 2.15 |

The software also detects two issues in the supplied workbook rather than propagating them silently: a cached `#DIV/0!` for a zero-mapped PO and a mismatch between the `PO Calculation` mapping and the canonical `Matrix` sheet. The importer uses `Matrix` as the mapping source and returns `N/A` for zero denominators.

## Run the interactive app

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Test and generate reproducibility artifacts

```bash
python -m pytest -q
python examples/run_theory_of_computation.py
python scripts/generate_artifacts.py
```

GitHub Actions repeats the tests and artifact generation on pushes and pull requests.

## Research-use boundary

Software correctness is not empirical validation of RBE. High-stakes adoption should proceed through content/construct review, shadow mode, low-stakes calibration, controlled comparison, limited certification pilot and external review. Comparative work should include strong OBE/evidence-rich baselines and measure transfer, error detection, constraint adaptation, misleading-AI resistance, calibration, certification error/risk, coverage, burden, reliability and fairness. If RBE does not improve the relevant risk–coverage–burden frontier, superiority is not demonstrated.

RBE does not claim invention of authentic assessment, oral defence, adaptive testing, Bayesian updating, equivalence relations or Pareto frontiers, and the repository does not claim that accreditation or regulatory bodies endorse RBE.

## Author

**Mohammad Amir Khusru Akhtar**

## Copyright and license

Copyright (C) 2026 Mohammad Amir Khusru Akhtar

Licensed under the Apache License, Version 2.0. See `LICENSE`.
