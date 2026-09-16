from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional

@dataclass(frozen=True)
class RCO:
    rco_id: str
    capability: str
    environments: List[str]
    perturbations: List[str]
    positive_decision: str = "certify"
    threshold: float = 60.0
    epsilon: float = 0.10
    burden_max: float = 3.0

@dataclass
class EvidenceState:
    performance_score: float
    compatible_worlds: Set[str] = field(default_factory=set)
    world_decisions: Dict[str, str] = field(default_factory=dict)
    posterior: Dict[str, float] = field(default_factory=dict)
    burden: float = 0.0
    history: List[dict] = field(default_factory=list)

@dataclass(frozen=True)
class Probe:
    probe_id: str
    family: str
    cost: float
    leakage: float = 0.0
    accessibility: float = 1.0
    reliability: float = 1.0
    group_disparity: float = 0.0
    resolution_gain: float = 0.0
    privacy_ok: bool = True
    construct_relevant: bool = True
    learner_time: float = 0.0
    assessor_effort: float = 0.0
    resource_cost: float = 0.0
    fairness_burden: float = 0.0

    def burden(self, leakage_weight: float = 1.0) -> float:
        return float(self.cost) + leakage_weight * float(self.leakage)

@dataclass
class StudentRecord:
    student_id: str
    rco_id: str
    score: float
    resolved_decision: Optional[str] = None
    decision_risk: Optional[float] = None
    burden: float = 0.0
    state: Optional[str] = None
    resolution_mode: str = "deterministic"
    resolved: Optional[bool] = None
