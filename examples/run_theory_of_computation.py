from pathlib import Path
import csv
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rbe.models import RCO, StudentRecord
from rbe.resolution import classify_state
from rbe.attainment import course_metrics, programme_metrics
from rbe.audit import audit_course

rco = RCO(
    "TOC-RCO4",
    "Construct and justify computational models, diagnose invalid reasoning, and adapt under changed constraints.",
    ["written exam", "transfer task", "AI-assisted analysis"],
    ["constraint shift", "misleading evidence", "transfer"],
    threshold=60,
    epsilon=0.10,
    burden_max=3.0,
)

records = []
with open(ROOT / "data/theory_of_computation.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        score = float(row["score"])
        risk = None if row["risk"] in {"", "None"} else float(row["risk"])
        decision = None if row["decision"] in {"", "None"} else row["decision"]
        burden = float(row["burden"])
        state = classify_state(score, rco, decision, risk, burden)
        records.append(StudentRecord(row["student_id"], row["rco_id"], score, decision, risk, burden, state))

metrics = course_metrics(records)
programme = programme_metrics(
    [{"rco_id": "TOC-RCO4", **metrics}],
    {"TOC-RCO4": {"PO1": 2, "PO2": 3, "PO5": 2}},
)
report = {
    "course": "Theory of Computation",
    "rco": rco.rco_id,
    "students": [r.__dict__ for r in records],
    "metrics": metrics,
    "programme": programme,
    "audit": audit_course(metrics),
}
out = ROOT / "artifacts"
out.mkdir(exist_ok=True)
(out / "theory_of_computation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
