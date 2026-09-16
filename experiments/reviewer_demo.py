"""Console counterpart of the Streamlit 3-minute reviewer demo."""
import pandas as pd

rows = [
    ["A",82,"Attained","resolved-positive","AR","stop; zero added burden"],
    ["B",82,"Attained","unresolved","AU","seek discriminating evidence"],
    ["C",82,"Attained","resolved-negative","RN","do not certify capability"],
    ["D",55,"Not attained","—","NA","development / ordinary course process"],
    ["E",82,"Attained","unresolved at Bmax","Deferred","retain uncertainty"],
]
df = pd.DataFrame(rows, columns=["learner","score","performance","resolution","state","action"])
print(df.to_string(index=False))
assert len(set(df.loc[df.learner.isin(["A","B","C"]),"score"])) == 1
assert set(df.loc[df.learner.isin(["A","B","C"]),"state"]) == {"AR","AU","RN"}
print("\nPASS: equal performance scores can coexist with distinct certification-resolution states.")
