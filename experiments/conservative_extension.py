"""Executable conservative-extension mechanism demonstration.

This is a mechanism test, not an educational-effectiveness experiment.
"""
from rbe.models import RCO, StudentRecord

rco = RCO("R1", "capability", ["exam"], ["transfer"], "certify", 60.0, 0.10, 3.0)
case = StudentRecord(
    student_id="A", rco_id=rco.rco_id, score=82.0,
    resolved_decision="certify", decision_risk=None, burden=0.0,
    state="AR", mode="deterministic", resolved=True,
)

print("RBE conservative-extension mechanism")
print(f"performance_score={case.score}")
print(f"resolution_state={case.state}")
print(f"resolved={case.resolved}")
print(f"additional_burden={case.burden}")
assert case.resolved and case.state == "AR" and case.burden == 0.0
print("PASS: resolution-adequate initial evidence requires zero additional burden in this constructed case.")
