from typing import Iterable, List, Callable, Any
from .models import Probe

def admissible_probes(probes: Iterable[Probe], min_resolution_gain: float, min_accessibility: float = 0.8, min_reliability: float = 0.8, max_group_disparity: float = 0.2, max_leakage: float = 1.0) -> List[Probe]:
    return [p for p in probes if p.resolution_gain >= min_resolution_gain and p.accessibility >= min_accessibility and p.reliability >= min_reliability and p.group_disparity <= max_group_disparity and p.leakage <= max_leakage and p.privacy_ok and p.construct_relevant]

def select_minimum_probe(probes: Iterable[Probe], leakage_weight: float = 1.0) -> Probe | None:
    probes = list(probes)
    return min(probes, key=lambda p: (p.burden(leakage_weight), -p.resolution_gain, p.probe_id)) if probes else None

def select_resolution_restoring_policy(policies: Iterable[Any], terminal_resolved: Callable[[Any], bool], burden: Callable[[Any], float]) -> Any | None:
    feasible = [p for p in policies if terminal_resolved(p)]
    return min(feasible, key=burden) if feasible else None
