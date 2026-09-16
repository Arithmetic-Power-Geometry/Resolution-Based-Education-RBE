# RBE Software Final Validation Report

Copyright (C) 2026 Mohammad Amir Khusru Akhtar

## Framework basis

The software implements the merged RBE architecture with the research blueprint as the mathematical core and the operating blueprint for governance, attainment, audit and implementation controls.

## Supplied Theory of Computation workbook

Workbook sheets detected: FLAT, Matrix, CO Calculation, PO Calculation. Learners parsed: 71.

Independent recomputation reproduces the workbook's rounded CO summaries:

- CO1: mean normalized score 0.48; mean attainment 1.75
- CO2: mean normalized score 0.52; mean attainment 2.10
- CO3: mean normalized score 0.45; mean attainment 1.46
- CO4: mean normalized score 0.57; mean attainment 2.15

Detected source-workbook issues:

1. PO8 cached attainment contains `#DIV/0!` because its mapping denominator is zero. The software returns `N/A` instead.
2. `PO Calculation` mapping differs from `Matrix` beginning at CO1/PO3. The software uses `Matrix` as the canonical mapping source.

## Corrected software invariants

- Deterministic RBE is the default; probabilistic risk is optional.
- Positive resolution requires a positive resolved decision; low risk alone is insufficient.
- Missing world decisions cannot count as deterministic resolution.
- AR, AU, RN, NA and Deferred are distinct.
- `PAR = RAR + UAR + RNR` when performance-attained cases are exhaustively partitioned.
- Zero PO/PSO mapping denominators are `N/A`, not zero and not division errors.
- One-step discriminating probe selection is distinguished from a full resolution-restoring adaptive MRRP policy.
- Existing OBE results are preserved and shown before RBE extension.

## Verification

The final build was compiled and exercised against the supplied workbook during development. The repository GitHub Actions workflow independently installs requirements, runs pytest, runs the Theory of Computation example, generates reproducibility artifacts and uploads the artifact bundle.

## Research boundary

Passing software tests establishes implementation consistency, not empirical superiority. RBE should be evaluated in shadow mode and controlled comparative studies before high-stakes adoption.
