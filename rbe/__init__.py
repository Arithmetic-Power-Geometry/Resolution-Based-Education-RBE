"""Resolution-Based Education reference implementation."""
__version__ = "1.0.0"
from .models import RCO, EvidenceState, Probe, StudentRecord
from .resolution import deterministic_resolved, carg_exists, decision_risk, probabilistic_resolved, positive_resolution, classify_state
from .attainment import course_metrics, programme_metrics
from .mrrp import admissible_probes, select_minimum_probe, select_resolution_restoring_policy
from .audit import audit_course
from .obe import calculate_co_results, weighted_po_attainment

__all__ = ["RCO","EvidenceState","Probe","StudentRecord","deterministic_resolved","carg_exists","decision_risk","probabilistic_resolved","positive_resolution","classify_state","course_metrics","programme_metrics","admissible_probes","select_minimum_probe","select_resolution_restoring_policy","audit_course","calculate_co_results","weighted_po_attainment"]
