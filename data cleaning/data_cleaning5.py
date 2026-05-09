import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

df = pd.read_csv(DATA_DIR / "2025 ridership.csv")

# Remove total column because heatmap should compare ride types
df = df.drop(columns=["Total Ridership"])

# Convert wide to long
long_df = df.melt(
    id_vars="Month",
    var_name="ride_type",
    value_name="ridership"
)

# Force ridership to numeric
long_df["ridership"] = (
    long_df["ridership"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

long_df["ridership"] = pd.to_numeric(long_df["ridership"], errors="coerce")

print(long_df[long_df["ridership"].isna()])

long_df.to_csv(DATA_DIR / "monthly_ridership_long.csv", index=False)

print(long_df)
