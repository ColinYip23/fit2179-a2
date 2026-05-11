import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

df = pd.read_csv(DATA_DIR / "rapidrail_2026_daily.csv")

df["date"] = pd.to_datetime(df["date"])
df["ridership"] = pd.to_numeric(df["ridership"], errors="coerce")
df = df.dropna(subset=["ridership"])

mask = (
    ~df["origin"].str.contains("All Stations", na=False) &
    ~df["destination"].str.contains("All Stations", na=False)
)

df = df[mask].copy()

daily = (
    df.groupby("date", as_index=False)["ridership"]
      .sum()
      .sort_values("date")
)

daily["rolling_7day_std"] = (
    daily["ridership"]
    .rolling(window=7, min_periods=3)
    .std()
)

daily.to_csv(DATA_DIR / "ridership_volatility.csv", index=False)