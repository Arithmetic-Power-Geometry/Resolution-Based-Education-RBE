from rbe.models import Probe
from rbe.mrrp import admissible_probes, select_minimum_probe

def test_probe_filter_and_selection():
    probes = [
        Probe("p1","transfer",cost=1.0,leakage=.1,accessibility=.95,reliability=.9,group_disparity=.05,resolution_gain=.4),
        Probe("p2","viva",cost=.8,leakage=.5,accessibility=.9,reliability=.9,group_disparity=.05,resolution_gain=.4),
        Probe("bad","x",cost=.1,accessibility=.2,reliability=.9,resolution_gain=.9),
    ]
    ok = admissible_probes(probes,.3)
    assert {p.probe_id for p in ok} == {"p1","p2"}
    assert select_minimum_probe(ok).probe_id == "p1"
