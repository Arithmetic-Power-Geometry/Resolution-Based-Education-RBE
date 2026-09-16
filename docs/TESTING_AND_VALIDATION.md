# Testing and Validation

## Software verification

The repository tests the mathematical and software invariants that must hold independently of any empirical claim:

- deterministic resolution requires every still-compatible world to have a known and identical certification decision;
- CARG remains when compatible worlds require different decisions;
- probabilistic resolution is explicit and optional, not a manually invented requirement for deterministic RBE;
- low risk alone cannot create positive attainment without a positive resolved decision;
- AR, AU, RN, NA and Deferred are separated;
- `PAR = RAR + UAR + RNR` under the stated exhaustive attained-case partition;
- probe admissibility enforces resolution-gain, accessibility, reliability, group-disparity, leakage, privacy and construct constraints;
- OBE CO calculations reproduce the supplied workbook formula pattern and thresholds;
- zero mapping denominators return `N/A` rather than division errors;
- the workbook importer reads FLAT, Matrix, CO Calculation and PO Calculation and treats Matrix as the canonical CO→PO/PSO mapping.

## Supplied Theory of Computation workbook cross-check

Independent recomputation on the supplied 71-learner workbook produced the same rounded CO summary values stored by the workbook:

| CO | Mean score | Mean attainment |
|---|---:|---:|
| CO1 | 0.48 | 1.75 |
| CO2 | 0.52 | 2.10 |
| CO3 | 0.45 | 1.46 |
| CO4 | 0.57 | 2.15 |

The cross-check also identified a cached `#DIV/0!` for PO8 where the mapping denominator is zero, and a mapping inconsistency between the PO Calculation sheet and the Matrix sheet beginning at CO1/PO3. The software does not reproduce those defects: it reports `N/A` for a zero denominator and uses Matrix as the canonical mapping source.

## Research validation is a different question

Passing software tests does **not** establish that RBE is educationally superior. Before consequential use, validation should proceed through content/construct review, shadow mode, low-stakes pilot, controlled comparison, limited certification pilot, programme-scale evaluation and external review.

A controlled study should compare current OBE, enhanced AI-aware OBE, an evidence-rich/programmatic comparator where applicable, and RBE on the same capability claims and an independent future criterion. Outcomes should include transfer, error detection, constraint adaptation, misleading-AI resistance, calibration, certification error/risk, coverage, unresolved/defer rate, learner/faculty burden, reliability and fairness.

A prospective falsification rule should be retained: if RBE does not improve the relevant risk–coverage–burden frontier against strong comparators, superiority is not demonstrated.
