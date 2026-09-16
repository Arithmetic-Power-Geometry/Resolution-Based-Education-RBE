from .models import RCO, EvidenceState, Probe
from .resolution import classify_state
from .mrrp import admissible_probes, select_minimum_probe

def run_resolution_episode(
    rco: RCO,
    state: EvidenceState,
    resolved_decision: str | None,
    risk: float | None,
    probes: list[Probe],
    min_resolution_gain: float = 0.2,
):
    state_name = classify_state(state.performance_score, rco, resolved_decision, risk, state.burden)
    if state_name in {"AR","RN","NA","Deferred"}:
        return state_name, None
    candidates = admissible_probes(probes, min_resolution_gain=min_resolution_gain)
    probe = select_minimum_probe(candidates)
    return "AU", probe
