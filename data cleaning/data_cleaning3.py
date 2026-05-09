import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

df = pd.read_csv(DATA_DIR / "komuter_2026.csv")

# Combine ridership for the same time regardless of origin/destination
hourly = (
    df.groupby("time", as_index=False)["ridership"]
      .sum()
      .sort_values("time")
)

hourly.to_csv(DATA_DIR / "hourly_ridership.csv", index=False)

print(hourly)
