from rbe.models import RCO, EvidenceState, Probe
from rbe.engine import run_resolution_episode

def test_zero_extra_evidence_when_deterministically_resolved():
    r=RCO("R","cap",[],[],threshold=60,epsilon=.1)
    state=EvidenceState(80,{"w1","w2"},{"w1":"certify","w2":"certify"},burden=0)
    status,probe,decision,risk=run_resolution_episode(r,state,[])
    assert status=="AR" and probe is None and decision=="certify" and risk is None

def test_select_probe_when_deterministically_unresolved():
    r=RCO("R","cap",[],[],threshold=60,epsilon=.1)
    state=EvidenceState(80,{"w1","w2"},{"w1":"certify","w2":"not"},burden=0)
    probes=[Probe("p","transfer",1,resolution_gain=.5)]
    status,probe,decision,risk=run_resolution_episode(r,state,probes)
    assert status=="AU" and probe.probe_id=="p" and decision is None

def test_probabilistic_mode_is_explicit():
    r=RCO("R","cap",[],[],threshold=60,epsilon=.1)
    state=EvidenceState(80,posterior={"certify":.95,"not":.05})
    status,probe,decision,risk=run_resolution_episode(r,state,[],mode="probabilistic")
    assert status=="AR" and decision=="certify" and risk<.1
