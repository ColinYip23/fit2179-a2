import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

df = pd.read_csv(DATA_DIR / "rapidrail_2026_daily.csv")

# Ensure ridership is numeric
df["ridership"] = pd.to_numeric(df["ridership"], errors="coerce")

# Remove rows with missing ridership
df = df.dropna(subset=["ridership"])

# Remove aggregate station rows
mask = (
    ~df["origin"].str.contains("All Stations", na=False) &
    ~df["destination"].str.contains("All Stations", na=False)
)

df_clean = df[mask].copy()

# Remove self-loops
df_clean = df_clean[
    df_clean["origin"] != df_clean["destination"]
]

# Aggregate OD flows
flows = (
    df_clean
    .groupby(["origin", "destination"], as_index=False)["ridership"]
    .sum()
)

# Keep top 30 strongest flows
flows = (
    flows
    .sort_values("ridership", ascending=False)
    .head(30)
)

# Rename for Sankey
flows = flows.rename(columns={
    "origin": "source",
    "destination": "target",
    "ridership": "value"
})

flows.to_csv(DATA_DIR / "rapidrail_sankey_top30.csv", index=False)

print(flows)