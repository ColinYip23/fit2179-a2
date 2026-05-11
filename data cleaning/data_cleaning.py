import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MIN_AVERAGE_DAILY_FLOW = 250
FLOW_COLUMNS = [
    "origin",
    "destination",
    "ridership",
    "start_lat",
    "start_lon",
    "end_lat",
    "end_lon",
]

def clean_transit_data(ridership_path, stops_path):
    ridership = pd.read_csv(
        ridership_path,
        usecols=["origin", "destination", "ridership"],
    )
    stops = pd.read_csv(
        stops_path,
        usecols=["stop_id", "stop_lat", "stop_lon"],
    )

    ridership["ridership"] = pd.to_numeric(ridership["ridership"], errors="coerce")

    valid_station_pair = (
        ridership["ridership"].notna()
        & ~ridership["origin"].str.contains("All Stations", na=False)
        & ~ridership["destination"].str.contains("All Stations", na=False)
        & (ridership["origin"] != ridership["destination"])
    )
    flows = ridership.loc[valid_station_pair].copy()

    # Collapse daily records into one average daily flow per OD pair.
    flows = (
        flows.groupby(["origin", "destination"], as_index=False)["ridership"]
        .mean()
        .round()
    )

    flows["origin_id"] = flows["origin"].str.split(":").str[0].str.strip()
    flows["dest_id"] = flows["destination"].str.split(":").str[0].str.strip()

    stops["stop_id"] = stops["stop_id"].astype(str).str.strip()
    stop_lookup = stops.set_index("stop_id")

    flows = flows.join(stop_lookup, on="origin_id")
    flows = flows.rename(columns={"stop_lat": "start_lat", "stop_lon": "start_lon"})

    flows = flows.join(stop_lookup, on="dest_id")
    flows = flows.rename(columns={"stop_lat": "end_lat", "stop_lon": "end_lon"})

    initial_count = len(flows)
    flows = flows.dropna(subset=["start_lat", "start_lon", "end_lat", "end_lon"])
    flows["ridership"] = flows["ridership"].astype(int)
    flows = flows[flows["ridership"] > MIN_AVERAGE_DAILY_FLOW]

    print(
        f"Cleaned {len(flows)} OD flows. "
        f"Dropped {initial_count - len(flows)} unmatched or low-flow station pairs."
    )

    return flows[FLOW_COLUMNS].sort_values("ridership", ascending=False)

if __name__ == "__main__":
    cleaned_data = clean_transit_data(DATA_DIR / "rapidrail_2026_daily.csv", DATA_DIR / "stops.csv")
    cleaned_data.to_csv(DATA_DIR / "cleaned_flow_data.csv", index=False)
    print("Success: File saved as 'cleaned_flow_data.csv'")
