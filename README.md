# Resolution-Based Education (RBE)

A software and reproducibility implementation of **Resolution-Based Education (RBE)**, a complete educational architecture for curriculum, learning, assessment, certification resolution, attainment, programme evaluation, and continuous improvement in the AI era.

The central proposition is:

> **Education must distinguish performance measurement from certification resolution.**

RBE preserves conventional outcomes, marks, grades, credits, programme structures, and continuous improvement. It adds an explicit decision-relative certification layer that asks whether the available evidence is sufficient for the distinction a credential claims to make.

## Scope

This repository implements the strongest compatible elements of the two current RBE system blueprints: the research-oriented mathematical specification and validation programme, and the institution-oriented operating architecture, governance, audit, and implementation controls.

The software covers:

- Programme purpose, PEO/PO/PSO/RCO structures and mappings
- Resolvable Capability Outcomes `RCO=(C,E,P,D)`
- CCVRT learning cycle
- Learning Evidence vs Certification Evidence
- Performance scoring and threshold attainment
- Deterministic and probabilistic Resolution Gates
- Certification-Assessment Resolution Gap (CARG)
- Minimum Resolution-Restoring Perturbation (MRRP)
- Finite stopping / burden cap / defer state
- Student states: AR, AU, RN, NA, Deferred
- Positive-resolution attainment `RCA=A*Q+`
- Course metrics: PAR, RR, RAR, UAR, RNR, MRB
- Programme metrics: PPO, RPO, UPO
- Capability Passport
- Resolution Ledger and provenance
- Reliability, validity, fairness, accessibility and burden controls
- Governance, continuous improvement and audit checks
- A reproducible Theory of Computation example

## Mathematical core

For learner `i` and RCO `j`:

```text
A_ij   = 1[S_ij >= T_j]
Q+_ij  = 1[r_ij <= epsilon_j and Dhat_ij = d+_j]
RCA_ij = A_ij * Q+_ij
```

The course-level performance and resolved-attainment metrics are:

```text
PAR_j = sum_i A_ij / N
RAR_j = sum_i RCA_ij / N
UAR_j = unresolved-performance-attained / N
RNR_j = resolved-negative-performance-attained / N
MRB_j = mean additional resolution burden
```

When resolved-negative performance-attained cases are possible:

```text
PAR_j = RAR_j + UAR_j + RNR_j
```

The structural Resolution Adequacy condition is:

```text
w_i ~_A w_j  =>  g(w_i) = g(w_j)
```

A Certification-Assessment Resolution Gap exists when that condition fails.

## Software architecture

```text
Programme definition
    -> RCO and mapping validation
    -> performance evidence ingestion
    -> initial evidence state K0
    -> resolution test
    -> CARG detection
    -> admissible probe filtering
    -> MRRP selection
    -> posterior / compatible-world update
    -> certify | not-attained | unresolved/deferred
    -> course attainment
    -> programme aggregation
    -> capability passport
    -> audit and continuous-improvement report
```

## Quick start

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python examples/run_theory_of_computation.py
python scripts/generate_artifacts.py
```

Generated reproducibility artifacts are written to `artifacts/`.

## Important implementation principles

- Marks measure performance; resolution governs capability certification.
- Resolution is not converted into extra marks.
- No extra viva or probe is added when existing evidence is already resolution-adequate.
- A low decision-risk value does not by itself imply positive attainment; the resolved decision must support the intended positive certification decision.
- Adaptive evidence is constrained by validity, accessibility, reliability, fairness, privacy, leakage and burden.
- `Unresolved/Deferred` is a legitimate outcome when the evidence budget is exhausted.
- RBE is designed as a conservative extension of established OBE and accreditation practice, not as a rejection of them.

## Reproducibility

The repository contains deterministic examples, unit tests, audit fixtures, JSON/CSV artifacts, and a GitHub Actions workflow. The included example is intended to demonstrate the full chain from RCO -> performance -> Resolution Gate -> adaptive evidence -> attainment -> PO aggregation.

## Author

**Mohammad Amir Khusru Akhtar**

## Copyright and license

Copyright (C) 2026 Mohammad Amir Khusru Akhtar

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).
