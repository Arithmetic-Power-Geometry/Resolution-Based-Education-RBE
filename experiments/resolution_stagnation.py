"""Constructed resolution-stagnation demonstration.

Two certification-incompatible worlds produce identical observations under the
current evidence language. Repeating that observation cannot separate them.
A discriminating perturbation is then shown to separate the decision classes.
"""
worlds = {"w_robust": "certify", "w_pattern": "not"}

def ordinary_observation(world):
    return "same-polished-artifact"

def constraint_shift(world):
    return "adapts-and-justifies" if world == "w_robust" else "fails-material-shift"

ordinary = {w: ordinary_observation(w) for w in worlds}
assert len(set(ordinary.values())) == 1
assert len(set(worlds.values())) == 2

for _ in range(10):
    assert len({ordinary_observation(w) for w in worlds}) == 1

perturbed = {w: constraint_shift(w) for w in worlds}
assert len(set(perturbed.values())) == 2

print("Resolution-stagnation mechanism")
print("ordinary evidence:", ordinary)
print("required decisions:", worlds)
print("after discriminating perturbation:", perturbed)
print("PASS: more observations of the non-discriminating kind do not resolve the decision; the constructed perturbation does.")
