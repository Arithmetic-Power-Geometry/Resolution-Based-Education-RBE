def validate_rco(rco) -> list[str]:
    issues = []
    if not str(rco.rco_id).strip(): issues.append("RCO identifier is required.")
    if not str(rco.capability).strip(): issues.append("Capability claim C is required.")
    if not rco.environments: issues.append("At least one environment E is required.")
    if not str(rco.positive_decision).strip(): issues.append("Positive certification decision is required.")
    if not 0 <= rco.threshold <= 100: issues.append("Performance threshold must be between 0 and 100.")
    if not 0 <= rco.epsilon <= 1: issues.append("Probabilistic epsilon must be between 0 and 1.")
    if rco.burden_max < 0: issues.append("Burden cap cannot be negative.")
    return issues

def validate_student_rows(rows: list[dict]) -> list[str]:
    issues, ids = [], []
    for i, row in enumerate(rows, 1):
        sid = str(row.get("student_id", "")).strip(); ids.append(sid)
        if not sid: issues.append(f"Row {i}: student_id is required.")
        try:
            score = float(row.get("score", 0))
            if not 0 <= score <= 100: issues.append(f"{sid or 'Row '+str(i)}: score must be 0..100.")
        except Exception:
            issues.append(f"{sid or 'Row '+str(i)}: score is not numeric.")
    duplicates = {x for x in ids if x and ids.count(x) > 1}
    if duplicates: issues.append("Duplicate student_id(s): " + ", ".join(sorted(duplicates)))
    return issues
