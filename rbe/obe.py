from dataclasses import dataclass
from typing import Dict, Iterable

@dataclass
class OBEStudent:
    student_id: str
    name: str
    marks: Dict[str, float]

def normalized_co_score(marks: Dict[str, float], max_marks: Dict[str, float], co_alloc: Dict[str, float]) -> float | None:
    denom = sum(float(v or 0) for v in co_alloc.values())
    if denom <= 0:
        return None
    total = 0.0
    for comp, alloc in co_alloc.items():
        mx = float(max_marks.get(comp, 0) or 0)
        if mx <= 0 and float(alloc or 0) > 0:
            return None
        total += (float(marks.get(comp, 0) or 0) / mx) * float(alloc or 0) if mx > 0 else 0
    return total / denom

def attainment_level(score01: float | None) -> int | None:
    if score01 is None:
        return None
    return 3 if score01 > .59 else 2 if score01 > .50 else 1 if score01 > .40 else 0

def calculate_co_results(students: Iterable[OBEStudent], max_marks: Dict[str, float], co_allocations: Dict[str, Dict[str, float]]) -> tuple[list[dict], dict]:
    rows = []
    co_ids = list(co_allocations)
    for student in students:
        row = {"student_id": student.student_id, "name": student.name, **student.marks}
        for co in co_ids:
            score = normalized_co_score(student.marks, max_marks, co_allocations[co])
            row[f"{co}_score01"] = score
            row[f"{co}_level"] = attainment_level(score)
        rows.append(row)
    summary = {}
    for co in co_ids:
        vals = [r[f"{co}_score01"] for r in rows if r[f"{co}_score01"] is not None]
        levels = [r[f"{co}_level"] for r in rows if r[f"{co}_level"] is not None]
        summary[co] = {"mean_score01": sum(vals) / len(vals) if vals else None, "mean_level": sum(levels) / len(levels) if levels else None}
    return rows, summary

def weighted_po_attainment(co_attainment: Dict[str, float | None], mapping: Dict[str, Dict[str, float]]) -> Dict[str, float | None]:
    outcomes = sorted({po for m in mapping.values() for po in m})
    result = {}
    for po in outcomes:
        pairs = [(float(mapping[co].get(po, 0) or 0), co_attainment.get(co)) for co in mapping]
        pairs = [(w, a) for w, a in pairs if w > 0 and a is not None]
        denom = sum(w for w, _ in pairs)
        result[po] = sum(w * float(a) for w, a in pairs) / denom if denom > 0 else None
    return result
