from rbe.models import StudentRecord
from rbe.attainment import course_metrics, programme_metrics

def test_course_metrics_identity_with_rn():
    rows = [
        StudentRecord("s1","R1",80,"certify",.05,1,"AR"),
        StudentRecord("s2","R1",80,None,.5,1,"AU"),
        StudentRecord("s3","R1",80,"not",.05,1,"RN"),
        StudentRecord("s4","R1",40,None,None,0,"NA"),
    ]
    m = course_metrics(rows)
    assert m["PAR"] == 75.0
    assert m["RAR"] == 25.0
    assert m["UAR"] == 25.0
    assert m["RNR"] == 25.0
    assert abs(m["PAR"] - (m["RAR"]+m["UAR"]+m["RNR"])) < 1e-9

def test_programme_metrics():
    rows=[{"rco_id":"R1","PAR":80,"RAR":70,"UAR":10},{"rco_id":"R2","PAR":60,"RAR":50,"UAR":10}]
    mapping={"R1":{"PO1":3},"R2":{"PO1":1}}
    p=programme_metrics(rows,mapping)["PO1"]
    assert p["PPO"] == 75
    assert p["RPO"] == 65
