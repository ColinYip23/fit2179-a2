import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def clean_transit_data(ridership_path, stops_path):
    # 1. Load Datasets
    # Ridership: origin, destination, date, ridership
    # Stops: stop_id, stop_name, stop_lat, stop_lon
    df_ridership = pd.read_csv(ridership_path)
    df_stops = pd.read_csv(stops_path)

    # 2. Filter out Aggregated Totals
    # We remove "A0: All Stations" as it cannot be plotted on a flow map
    mask = (~df_ridership['origin'].str.contains('All Stations', na=False)) & \
           (~df_ridership['destination'].str.contains('All Stations', na=False))
    df_clean = df_ridership[mask].copy()

    # 3. Extract Station Codes
    # Convert "AG01: Sentul Timur" -> "AG01"
    df_clean['origin_id'] = df_clean['origin'].str.split(':').str[0].str.strip()
    df_clean['dest_id'] = df_clean['destination'].str.split(':').str[0].str.strip()

    # 4. Standardize Stop IDs
    # Ensure stops_df IDs match the format in ridership (e.g., ensuring no leading/trailing spaces)
    df_stops['stop_id'] = df_stops['stop_id'].astype(str).str.strip()

    # 5. Merge Coordinates for Origin
    df_clean = pd.merge(
        df_clean, 
        df_stops[['stop_id', 'stop_lat', 'stop_lon']], 
        left_on='origin_id', 
        right_on='stop_id', 
        how='left'
    ).rename(columns={'stop_lat': 'start_lat', 'stop_lon': 'start_lon'}).drop('stop_id', axis=1)

    # 6. Merge Coordinates for Destination
    df_clean = pd.merge(
        df_clean, 
        df_stops[['stop_id', 'stop_lat', 'stop_lon']], 
        left_on='dest_id', 
        right_on='stop_id', 
        how='left'
    ).rename(columns={'stop_lat': 'end_lat', 'stop_lon': 'end_lon'}).drop('stop_id', axis=1)

    # 7. Final Cleanup
    # Drop rows where coordinates couldn't be found (unmatched IDs)
    initial_count = len(df_clean)
    df_clean = df_clean.dropna(subset=['start_lat', 'end_lat'])
    
    print(f"Cleaned {len(df_clean)} rows. Dropped {initial_count - len(df_clean)} unmatched stations.")
    
    return df_clean

if __name__ == "__main__":
    cleaned_data = clean_transit_data(DATA_DIR / "rapidrail_2026_daily.csv", DATA_DIR / "stops.csv")
    cleaned_data.to_csv(DATA_DIR / "cleaned_flow_data.csv", index=False)
    print("Success: File saved as 'cleaned_flow_data.csv'")
