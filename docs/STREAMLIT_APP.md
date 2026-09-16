# Interactive RBE Laboratory

Run:

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```

The application is a guided OBE-to-RBE workflow rather than a stand-alone score calculator.

1. Start / OBE Import
2. Programme & Course
3. CO → RCO Design
4. Performance Evidence
5. Resolution Gate
6. CARG & MRRP
7. RBE Attainment
8. PO/PSO Comparison
9. Capability Passport
10. Resolution Ledger
11. Audit & Improvement
12. Validation / Export

The importer supports the Theory of Computation workbook structure (`FLAT`, `Matrix`, `CO Calculation`, `PO Calculation`). Existing CO and PO/PSO calculations are recomputed before the RBE layer is applied. The `Matrix` sheet is treated as the canonical CO→PO/PSO mapping because the supplied workbook contains inconsistent references in part of its `PO Calculation` sheet.

Deterministic RBE is the default mode and requires no manually invented probability. Probabilistic RBE is available as an explicit advanced mode. The app keeps performance score and resolution status separate and exposes AR, AU, RN, NA, Deferred, PAR, RR, RAR, UAR, RNR, MRB and defer rate.

The MRRP page deliberately labels its immediate recommendation as a **one-step discriminating probe**. A full MRRP is a probe or adaptive policy whose terminal evidence reaches the declared resolution condition.

Exports include the complete RBE result package, evaluated learner table, Capability Passport and Resolution Ledger.

For consequential institutional use, locally validate decision standards, thresholds, perturbations, reliability, fairness, accessibility, privacy, security, appeals and governance. Software operation does not by itself establish empirical superiority.

Copyright (C) 2026 Mohammad Amir Khusru Akhtar

Apache License 2.0
