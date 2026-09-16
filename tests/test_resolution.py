from rbe.models import RCO
from rbe.resolution import decision_risk, classify_state, positive_resolution

def test_decision_risk():
    assert abs(decision_risk({"certify":0.9,"not":0.1}) - 0.1) < 1e-9

def test_positive_resolution_requires_positive_decision():
    r = RCO("R1","x",[],[])
    assert positive_resolution(80,r,"certify",0.05)
    assert not positive_resolution(80,r,"not",0.05)

def test_states():
    r = RCO("R1","x",[],[], threshold=60, epsilon=0.1, burden_max=3)
    assert classify_state(80,r,"certify",0.05,1) == "AR"
    assert classify_state(80,r,"not",0.05,1) == "RN"
    assert classify_state(80,r,None,0.5,1) == "AU"
    assert classify_state(80,r,None,0.5,3) == "Deferred"
    assert classify_state(40,r,None,None,0) == "NA"
