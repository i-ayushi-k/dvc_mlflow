import pandas as pd

DATA = "data/diabetes.csv"

df = pd.read_csv(DATA)

# Version 2 demonstration:
# keep exactly the same observations and columns, but reorder the dataset
# deterministically so DVC detects a new file version without inventing data.
df = df.sort_values(
    by=["glucose", "bloodpressure", "diabetes"],
    ascending=[True, True, True],
    kind="mergesort",
).reset_index(drop=True)

df.to_csv(DATA, index=False)
print(f"Version 2 created: {len(df)} rows, {len(df.columns)} columns")
