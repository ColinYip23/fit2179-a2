import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Load files
brt = pd.read_csv(DATA_DIR / "brt_2026_daily.csv")
rail = pd.read_csv(DATA_DIR / "rapidrail_2026_daily.csv")

# Add mode labels
brt["mode"] = "BRT"

# Infer mode from station code prefix
def get_rail_mode(station):
    station = str(station)
    if station.startswith("KJ") or station.startswith("AG") or station.startswith("SP"):
        return "LRT"
    if station.startswith("KG") or station.startswith("PY"):
        return "MRT"
    return "Other"

rail["mode"] = rail["destination"].apply(get_rail_mode)

# Combine
df = pd.concat([brt, rail], ignore_index=True)

# Clean types
df["date"] = pd.to_datetime(df["date"])
df["ridership"] = pd.to_numeric(df["ridership"], errors="coerce")
df = df.dropna(subset=["ridership"])

# Remove "All Stations" from origin and destination
mask = (
    ~df["origin"].str.contains("All Stations", na=False) &
    ~df["destination"].str.contains("All Stations", na=False)
)

df = df[mask].copy()

# Keep only BRT, LRT, MRT
df = df[df["mode"].isin(["BRT", "LRT", "MRT"])]

# Aggregate daily ridership by mode
daily_mode = (
    df.groupby(["date", "mode"], as_index=False)["ridership"]
      .sum()
      .sort_values(["date", "mode"])
)

daily_mode.to_csv(DATA_DIR / "daily_mode_ridership.csv", index=False)

print(daily_mode)