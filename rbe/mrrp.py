from typing import Iterable, List
from .models import Probe

def admissible_probes(
    probes: Iterable[Probe],
    min_resolution_gain: float,
    min_accessibility: float = 0.8,
    min_reliability: float = 0.8,
    max_group_disparity: float = 0.2,
    max_leakage: float = 1.0,
) -> List[Probe]:
    out = []
    for p in probes:
        if (
            p.resolution_gain >= min_resolution_gain
            and p.accessibility >= min_accessibility
            and p.reliability >= min_reliability
            and p.group_disparity <= max_group_disparity
            and p.leakage <= max_leakage
            and p.privacy_ok
            and p.construct_relevant
        ):
            out.append(p)
    return out

def select_minimum_probe(probes: Iterable[Probe], leakage_weight: float = 1.0) -> Probe | None:
    probes = list(probes)
    if not probes:
        return None
    return min(probes, key=lambda p: (p.burden(leakage_weight), -p.resolution_gain, p.probe_id))
