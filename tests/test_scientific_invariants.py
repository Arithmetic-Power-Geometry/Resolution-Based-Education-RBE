"""Scientific integrity tests for the RBE reporting layer.

These tests are not claims of educational effectiveness. They verify internal
relationships that the reference implementation must preserve.
"""
from rbe.models import RCO, StudentRecord
from rbe.attainment import course_metrics


def _rco():
    return RCO("R1", "capability", ["exam"], ["transfer"], "certify", 60.0, 0.10, 3.0)


def test_equal_scores_can_have_different_resolution_states():
    r = _rco()
    rows = [
        StudentRecord("A", r.rco_id, 82.0, "certify", None, 0.0, "AR", "deterministic", True),
        StudentRecord("B", r.rco_id, 82.0, None, None, 1.0, "AU", "deterministic", False),
        StudentRecord("C", r.rco_id, 82.0, "not", None, 1.0, "RN", "deterministic", True),
    ]
    assert len({x.score for x in rows}) == 1
    assert {x.state for x in rows} == {"AR", "AU", "RN"}


def test_course_metrics_preserve_attained_partition_identity():
    r = _rco()
    rows = [
        StudentRecord("A", r.rco_id, 82.0, "certify", None, 0.0, "AR", "deterministic", True),
        StudentRecord("B", r.rco_id, 82.0, None, None, 1.0, "AU", "deterministic", False),
        StudentRecord("C", r.rco_id, 82.0, "not", None, 1.0, "RN", "deterministic", True),
        StudentRecord("D", r.rco_id, 55.0, None, None, 0.0, "NA", "deterministic", False),
    ]
    m = course_metrics(rows)
    assert m["RAR"] <= m["PAR"]
    assert m["UAR"] <= m["PAR"]
    assert m["RNR"] <= m["PAR"]
    assert abs(m["PAR"] - (m["RAR"] + m["UAR"] + m["RNR"])) < 1e-9


def test_conservative_extension_case_can_have_zero_added_burden():
    r = _rco()
    row = StudentRecord("A", r.rco_id, 82.0, "certify", None, 0.0, "AR", "deterministic", True)
    assert row.resolved is True
    assert row.burden == 0.0


def test_deferred_state_keeps_uncertainty_visible_at_burden_boundary():
    r = _rco()
    row = StudentRecord("E", r.rco_id, 82.0, None, None, r.bmax, "Deferred", "deterministic", False)
    assert row.resolved is False
    assert row.burden == r.bmax
    assert row.state == "Deferred"
