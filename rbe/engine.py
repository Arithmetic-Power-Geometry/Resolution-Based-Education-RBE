from .models import RCO, EvidenceState, Probe
from .resolution import classify_state, deterministic_resolved, probabilistic_resolved
from .mrrp import admissible_probes, select_minimum_probe

def run_resolution_episode(rco: RCO, state: EvidenceState, probes: list[Probe], mode: str = "deterministic", decision_posterior: dict | None = None, min_resolution_gain: float = .2):
    if state.performance_score < rco.threshold:
        return "NA", None, None, None
    if mode == "deterministic":
        resolved, decision = deterministic_resolved(state); risk = None
    elif mode == "probabilistic":
        resolved, decision, risk = probabilistic_resolved(decision_posterior or state.posterior, rco.epsilon)
    else:
        raise ValueError("mode must be deterministic or probabilistic")
    status = classify_state(state.performance_score, rco, decision, risk, state.burden, resolved=resolved)
    if status in {"AR", "RN", "NA", "Deferred"}:
        return status, None, decision, risk
    probe = select_minimum_probe(admissible_probes(probes, min_resolution_gain))
    return "AU", probe, decision, risk
