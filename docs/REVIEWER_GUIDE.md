# RBE Reviewer Guide

## The scientific question

A learner can cross a performance threshold without the available evidence necessarily resolving the capability distinction that a credential intends to certify. RBE therefore separates performance measurement from certification resolution.

## Read the repository in five minutes

1. Start with the scientific flow in `README.md`.
2. Run the Streamlit **Reviewer Demo**.
3. Compare learners A, B and C: all score 82, but their evidence supports resolved-positive, unresolved and resolved-negative states respectively.
4. Inspect the Resolution Gate and CARG/MRRP stages.
5. Run `python -m pytest -q` and `python scripts/generate_artifacts.py` to inspect implementation reproducibility.

## Three mechanism cases

### A. Conservative extension
If current evidence is already resolution-adequate, the Resolution Gate stops immediately. Added RBE assessment burden is zero.

### B. Decision-relevant ambiguity
If current evidence leaves compatible learner possibilities requiring different certification decisions, the case is unresolved. RBE does not infer capability from the mark alone; it seeks admissible discriminating evidence.

### C. Finite stopping
If the required distinction cannot be resolved within the approved evidence/burden boundary, the state is Deferred rather than a forced certification claim.

## Interpretation boundary

Software correctness is not educational-effectiveness evidence. Synthetic examples demonstrate mechanisms. Workbook reproduction tests calculations. Prospective comparative studies are required for claims about educational benefit, fairness, reliability or institutional superiority.

## Foundation

Akhtar, M. A. K. (2026), *Beyond Outcome Attainment: Resolution-Based Education and the Certification–Assessment Resolution Gap in the Generative-AI Era*. DOI `10.5281/zenodo.22797079`.
