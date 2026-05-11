import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

df = pd.read_csv(DATA_DIR / "rapidrail_2026_daily.csv")

df["ridership"] = pd.to_numeric(df["ridership"], errors="coerce")
df = df.dropna(subset=["ridership"])

# Remove aggregate rows
mask = (
    ~df["origin"].str.contains("All Stations", na=False) &
    ~df["destination"].str.contains("All Stations", na=False)
)
df = df[mask].copy()

# Count station ridership as origin + destination activity
origin_totals = (
    df.groupby("origin", as_index=False)["ridership"]
      .sum()
      .rename(columns={"origin": "station"})
)

destination_totals = (
    df.groupby("destination", as_index=False)["ridership"]
      .sum()
      .rename(columns={"destination": "station"})
)

station_totals = pd.concat([origin_totals, destination_totals], ignore_index=True)

station_totals = (
    station_totals.groupby("station", as_index=False)["ridership"]
      .sum()
      .sort_values("ridership", ascending=False)
      .head(15)
)

station_totals.to_csv(DATA_DIR / "top_stations_ridership.csv", index=False)

print(station_totals)