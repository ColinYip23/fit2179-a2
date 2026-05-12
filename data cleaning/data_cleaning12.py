import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Load OD dataset
df = pd.read_csv(DATA_DIR / "cleaned_flow_data.csv")

# Aggregate incoming ridership
station_inflow = (
    df.groupby(
        ['destination', 'end_lat', 'end_lon'],
        as_index=False
    )
    .agg(incoming_ridership=('ridership', 'sum'))
)

# Rename columns
station_inflow = station_inflow.rename(columns={
    'destination': 'station',
    'end_lat': 'lat',
    'end_lon': 'lon'
})

# Keep top stations only
station_inflow = (
    station_inflow
    .sort_values('incoming_ridership', ascending=False)
    .head(50)
)

# Save compact dataset
station_inflow.to_csv(DATA_DIR / "station_inflow.csv", index=False)

print(station_inflow.head())
print("Saved as station_inflow.csv")