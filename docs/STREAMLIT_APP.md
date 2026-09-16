# Interactive RBE Lab

The Streamlit application provides an 11-step guided workflow:

1. Programme Context
2. RCO Design
3. Assessment Evidence
4. Resolution Gate
5. MRRP / Adaptive Probe
6. Course Attainment
7. Programme Mapping
8. Capability Passport
9. Resolution Ledger
10. Audit & Continuous Improvement
11. Export / Test Report

## Run

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

The interface starts with a Theory of Computation demonstration dataset. Users can edit learner evidence, thresholds, resolution parameters, probe candidates and programme mappings. Every stage contains contextual help, and the sidebar allows direct navigation through the full RBE workflow.

The application can export a Capability Passport, Resolution Ledger, evaluated learner table and complete RBE result package.

## Implementation boundary

The application is a research/reference implementation. High-stakes institutional use requires local validation of thresholds, decision models, perturbations, fairness, accessibility, reliability, privacy, due process and governance.

Copyright (C) 2026 Mohammad Amir Khusru Akhtar

Apache License 2.0
