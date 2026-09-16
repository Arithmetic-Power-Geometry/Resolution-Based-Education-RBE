def audit_course(metrics: dict, fairness_flag: bool = False, reliability: float | None = None) -> list[str]:
    findings = []
    if metrics.get("PAR",0) >= 75 and metrics.get("UAR",0) >= 10:
        findings.append("High performance attainment with material unresolved attainment: review certification evidence design.")
    if metrics.get("MRB",0) > 2:
        findings.append("Mean resolution burden is high: improve initial assessment discrimination or probe efficiency.")
    if fairness_flag:
        findings.append("Fairness flag raised: pause strong fairness claims and investigate subgroup/access effects.")
    if reliability is not None and reliability < 0.8:
        findings.append("Reliability below operating target: recalibrate assessors/probes before high-stakes use.")
    if not findings:
        findings.append("No automatic audit trigger raised; continue routine moderation and continuous improvement.")
    return findings
