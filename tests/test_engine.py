from rbe.models import RCO, EvidenceState, Probe
from rbe.engine import run_resolution_episode

def test_zero_extra_evidence_when_resolved():
    r=RCO("R","cap",[],[],threshold=60,epsilon=.1)
    st=EvidenceState(80,burden=0)
    status,probe=run_resolution_episode(r,st,"certify",.05,[])
    assert status=="AR" and probe is None

def test_select_probe_when_unresolved():
    r=RCO("R","cap",[],[],threshold=60,epsilon=.1)
    st=EvidenceState(80,burden=0)
    probes=[Probe("p","transfer",1,resolution_gain=.5)]
    status,probe=run_resolution_episode(r,st,None,.5,probes)
    assert status=="AU" and probe.probe_id=="p"
