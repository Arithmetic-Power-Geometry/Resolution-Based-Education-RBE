from typing import Iterable, Dict
from .models import StudentRecord

def course_metrics(records: Iterable[StudentRecord]) -> Dict[str, float]:
    rows = list(records)
    n = len(rows)
    if n == 0:
        return {k: 0.0 for k in ["PAR","RR","RAR","UAR","RNR","MRB"]}
    perf = sum(r.state in {"AR","AU","RN","Deferred"} for r in rows)
    resolved = sum(r.state in {"AR","RN","NA"} and r.decision_risk is not None for r in rows)
    ar = sum(r.state == "AR" for r in rows)
    au = sum(r.state in {"AU","Deferred"} for r in rows)
    rn = sum(r.state == "RN" for r in rows)
    return {
        "PAR": 100.0 * perf / n,
        "RR": 100.0 * resolved / n,
        "RAR": 100.0 * ar / n,
        "UAR": 100.0 * au / n,
        "RNR": 100.0 * rn / n,
        "MRB": sum(r.burden for r in rows) / n,
    }

def programme_metrics(course_rows: Iterable[dict], mapping: Dict[str, Dict[str, float]]) -> Dict[str, dict]:
    course_rows = list(course_rows)
    by_rco = {r["rco_id"]: r for r in course_rows}
    result = {}
    pos = sorted({po for m in mapping.values() for po in m})
    for po in pos:
        weighted = {"PPO":0.0,"RPO":0.0,"UPO":0.0}
        denom = 0.0
        for rco_id, po_map in mapping.items():
            w = po_map.get(po,0.0)
            if w <= 0 or rco_id not in by_rco:
                continue
            denom += w
            row = by_rco[rco_id]
            weighted["PPO"] += w * row["PAR"]
            weighted["RPO"] += w * row["RAR"]
            weighted["UPO"] += w * row["UAR"]
        result[po] = {k:(v/denom if denom else 0.0) for k,v in weighted.items()}
    return result
