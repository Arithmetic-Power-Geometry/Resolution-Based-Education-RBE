from typing import Dict, Tuple
from .models import EvidenceState, RCO

def deterministic_resolved(state: EvidenceState) -> Tuple[bool, str | None]:
    if not state.compatible_worlds:
        return False, None
    if any(w not in state.world_decisions for w in state.compatible_worlds):
        return False, None
    decisions = {state.world_decisions[w] for w in state.compatible_worlds}
    if len(decisions) == 1:
        return True, next(iter(decisions))
    return False, None

def carg_exists(state: EvidenceState) -> bool:
    if not state.compatible_worlds:
        return False
    decisions = {state.world_decisions.get(w) for w in state.compatible_worlds}
    return None in decisions or len(decisions) > 1

def decision_risk(decision_posterior: Dict[str, float]) -> float:
    if not decision_posterior:
        return 1.0
    vals = [max(0.0, float(v)) for v in decision_posterior.values()]
    total = sum(vals)
    if total <= 0:
        return 1.0
    return 1.0 - max(v / total for v in vals)

def probabilistic_resolved(decision_posterior: Dict[str, float], epsilon: float) -> Tuple[bool, str | None, float]:
    if not decision_posterior:
        return False, None, 1.0
    total = sum(max(0.0, float(v)) for v in decision_posterior.values())
    if total <= 0:
        return False, None, 1.0
    norm = {k: max(0.0, float(v)) / total for k, v in decision_posterior.items()}
    decision = max(norm, key=norm.get)
    risk = 1.0 - norm[decision]
    return risk <= epsilon, (decision if risk <= epsilon else None), risk

def classify_state(score: float, rco: RCO, resolved_decision: str | None, risk: float | None, burden: float, *, resolved: bool | None = None) -> str:
    if score < rco.threshold:
        return "NA"
    if resolved is None:
        resolved = resolved_decision is not None and (risk is None or risk <= rco.epsilon)
    if resolved:
        return "AR" if resolved_decision == rco.positive_decision else "RN"
    return "Deferred" if burden >= rco.burden_max else "AU"

def positive_resolution(score: float, rco: RCO, resolved_decision: str | None, risk: float | None = None, *, resolved: bool | None = None) -> bool:
    if score < rco.threshold or resolved_decision != rco.positive_decision:
        return False
    if resolved is not None:
        return bool(resolved)
    return risk is not None and risk <= rco.epsilon
