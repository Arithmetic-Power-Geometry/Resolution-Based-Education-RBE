from typing import Iterable, Dict
from .models import StudentRecord

def course_metrics(records: Iterable[StudentRecord]) -> Dict[str, float]:
    rows = list(records)
    n = len(rows)
    if not n:
        return {k: 0.0 for k in ["PAR", "RR", "RAR", "UAR", "RNR", "MRB", "DeferredRate"]}
    perf = sum(r.state in {"AR", "AU", "RN", "Deferred"} for r in rows)
    resolved = sum(r.state in {"AR", "RN"} or (r.state == "NA" and r.resolved is True) for r in rows)
    ar = sum(r.state == "AR" for r in rows)
    rn = sum(r.state == "RN" for r in rows)
    unresolved_attained = sum(r.state in {"AU", "Deferred"} for r in rows)
    deferred = sum(r.state == "Deferred" for r in rows)
    return {
        "PAR": 100.0 * perf / n,
        "RR": 100.0 * resolved / n,
        "RAR": 100.0 * ar / n,
        "UAR": 100.0 * unresolved_attained / n,
        "RNR": 100.0 * rn / n,
        "MRB": sum(float(r.burden) for r in rows) / n,
        "DeferredRate": 100.0 * deferred / n,
    }

def programme_metrics(course_rows: Iterable[dict], mapping: Dict[str, Dict[str, float]]) -> Dict[str, dict]:
    rows = list(course_rows)
    by_rco = {r["rco_id"]: r for r in rows}
    result = {}
    pos = sorted({po for m in mapping.values() for po in m})
    for po in pos:
        active = [(r, float(mapping[r].get(po, 0) or 0)) for r in mapping if r in by_rco and float(mapping[r].get(po, 0) or 0) > 0]
        denom = sum(w for _, w in active)
        if denom <= 0:
            result[po] = {"PPO": None, "RPO": None, "UPO": None}
            continue
        result[po] = {
            "PPO": sum(w * float(by_rco[r]["PAR"]) for r, w in active) / denom,
            "RPO": sum(w * float(by_rco[r]["RAR"]) for r, w in active) / denom,
            "UPO": sum(w * float(by_rco[r]["UAR"]) for r, w in active) / denom,
        }
    return result
