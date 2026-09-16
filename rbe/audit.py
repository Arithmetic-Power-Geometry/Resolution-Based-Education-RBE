def audit_course(metrics: dict, fairness_flag: bool = False, reliability: float | None = None) -> list[str]:
    out = []
    if metrics.get("UAR", 0) > 10: out.append("High attained-but-unresolved proportion: review initial evidence and perturbation design.")
    if metrics.get("MRB", 0) > 2: out.append("High mean resolution burden: improve K0 discrimination or probe efficiency.")
    if metrics.get("DeferredRate", 0) > 5: out.append("Deferred cases are material: review burden cap, reassessment and progression policy.")
    if fairness_flag: out.append("Fairness/accessibility concern flagged: investigate before consequential use.")
    if reliability is not None and reliability < .8: out.append("Reliability below 0.80: calibrate assessors/probes before high-stakes use.")
    return out
