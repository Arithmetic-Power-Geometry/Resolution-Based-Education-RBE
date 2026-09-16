from typing import Dict, Tuple
from .models import EvidenceState, RCO

def deterministic_resolved(state: EvidenceState) -> Tuple[bool, str | None]:
    if not state.compatible_worlds:
        return False, None
    decisions = {state.world_decisions[w] for w in state.compatible_worlds if w in state.world_decisions}
    if len(decisions) == 1:
        return True, next(iter(decisions))
    return False, None

def decision_risk(decision_posterior: Dict[str, float]) -> float:
    if not decision_posterior:
        return 1.0
    total = sum(decision_posterior.values())
    if total <= 0:
        return 1.0
    probs = [v / total for v in decision_posterior.values()]
    return 1.0 - max(probs)

def positive_resolution(score: float, rco: RCO, resolved_decision: str | None, risk: float | None) -> bool:
    return (
        score >= rco.threshold
        and resolved_decision == rco.positive_decision
        and risk is not None
        and risk <= rco.epsilon
    )

def classify_state(score: float, rco: RCO, resolved_decision: str | None, risk: float | None, burden: float) -> str:
    attained_perf = score >= rco.threshold
    if not attained_perf:
        return "NA"
    if resolved_decision is not None and risk is not None and risk <= rco.epsilon:
        if resolved_decision == rco.positive_decision:
            return "AR"
        return "RN"
    if burden >= rco.burden_max:
        return "Deferred"
    return "AU"
