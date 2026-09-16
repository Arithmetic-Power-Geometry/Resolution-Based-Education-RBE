# RBE Software Specification

## Purpose
This implementation operationalizes Resolution-Based Education as a decision-relative educational system rather than an extra examination component.

## Core entities
- Programme purpose / PEO / PO / PSO
- Resolvable Capability Outcome: `RCO=(C,E,P,D)`
- Performance evidence and threshold
- Evidence state `K_t`
- Resolution rule
- Candidate probe / perturbation
- Resolution episode
- Student capability state
- Course and programme metrics
- Capability Passport
- Resolution Ledger
- Continuous-improvement action

## Certification logic
Performance and certification resolution are separate. A student can have high performance and unresolved evidence. Positive resolved attainment requires both the performance criterion and positive resolution.

## Resolution modes
### Deterministic
The remaining compatible learner worlds must all imply the same required certification decision.

### Probabilistic
`r_t = 1 - max_d P(D=d | K_t)`. Resolution occurs when `r_t <= epsilon`, but positive attainment also requires the selected decision to be the intended positive decision.

## Adaptive evidence
A probe is eligible only when it satisfies declared resolution-gain, construct, accessibility, reliability, fairness, privacy and leakage constraints. The one-step selector chooses minimum burden among admissible probes. A full MRRP should be represented as an adaptive policy/tree whose terminal leaves satisfy the stopping condition.

## Finite stopping
The engine must respect `B_max`. If evidence remains unresolved when the burden cap is exhausted, the output is `Deferred/Unresolved`, not manufactured certainty.

## Attainment
The implementation distinguishes:
- `AR`: attained and resolved-positive
- `AU`: attained by performance but unresolved
- `RN`: performance-attained but resolved-negative
- `NA`: not attained by performance
- `Deferred`: unresolved at procedural/burden boundary

When RN cases are possible, `PAR = RAR + UAR + RNR`.

## Programme aggregation
Course-level weighted PO aggregation is implemented for compatibility, but complex programme capabilities should also use direct programme-level evidence rather than relying only on weighted course averages.

## Audit
Audit outputs flag unresolved attainment, excessive burden, fairness concerns and low reliability. Human review remains necessary for high-stakes implementation.

## Governance boundary
The software is a reference implementation. It does not alter statutory grades, awards, credits or accreditation rules by itself. High-stakes use requires institutional approval, validation, due process and applicable legal/regulatory controls.
