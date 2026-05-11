import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

df = pd.read_csv(DATA_DIR / "cleaned_flow_data.csv")

df["ridership"] = pd.to_numeric(df["ridership"], errors="coerce")
df = df.dropna(subset=["ridership"])

# Haversine distance in km
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

df["distance_km"] = haversine(
    df["start_lat"],
    df["start_lon"],
    df["end_lat"],
    df["end_lon"]
)

# Remove invalid/self-loop distances
df = df[df["distance_km"] > 0].copy()

# Optional: aggregate same OD pairs
distance_decay = (
    df.groupby(["origin", "destination", "distance_km"], as_index=False)["ridership"]
      .sum()
)

distance_decay.to_csv(DATA_DIR / "distance_decay.csv", index=False)

print(distance_decay)