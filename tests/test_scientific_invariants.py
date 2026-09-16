"""Scientific integrity tests for the RBE reporting layer.

These tests are mechanism/invariant checks, not claims of educational effectiveness.
"""
from rbe.models import RCO, StudentRecord
from rbe.attainment import course_metrics


def _rco():
    return RCO("R1", "capability", ["exam"], ["transfer"], "certify", 60.0, 0.10, 3.0)


def _record(student_id, score, decision, burden, state, resolved):
    return StudentRecord(
        student_id=student_id,
        rco_id="R1",
        score=score,
        resolved_decision=decision,
        decision_risk=None,
        burden=burden,
        state=state,
        mode="deterministic",
        resolved=resolved,
    )


def test_equal_scores_can_have_different_resolution_states():
    rows = [
        _record("A", 82.0, "certify", 0.0, "AR", True),
        _record("B", 82.0, None, 1.0, "AU", False),
        _record("C", 82.0, "not", 1.0, "RN", True),
    ]
    assert len({x.score for x in rows}) == 1
    assert {x.state for x in rows} == {"AR", "AU", "RN"}


def test_course_metrics_preserve_attained_partition_identity():
    rows = [
        _record("A", 82.0, "certify", 0.0, "AR", True),
        _record("B", 82.0, None, 1.0, "AU", False),
        _record("C", 82.0, "not", 1.0, "RN", True),
        _record("D", 55.0, None, 0.0, "NA", False),
    ]
    m = course_metrics(rows)
    assert m["RAR"] <= m["PAR"]
    assert m["UAR"] <= m["PAR"]
    assert m["RNR"] <= m["PAR"]
    assert abs(m["PAR"] - (m["RAR"] + m["UAR"] + m["RNR"])) < 1e-9


def test_conservative_extension_case_can_have_zero_added_burden():
    row = _record("A", 82.0, "certify", 0.0, "AR", True)
    assert row.resolved is True
    assert row.burden == 0.0


def test_deferred_state_keeps_uncertainty_visible_at_burden_boundary():
    r = _rco()
    row = _record("E", 82.0, None, r.bmax, "Deferred", False)
    assert row.resolved is False
    assert row.burden == r.bmax
    assert row.state == "Deferred"
