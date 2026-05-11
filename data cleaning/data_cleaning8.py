import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# ----------------------------
# 1. Combine 2021–2025 ridership files
# ----------------------------
all_ridership = []

for year in range(2021, 2026):
    df = pd.read_csv(DATA_DIR / f"{year} ridership.csv")

    df["Total Ridership"] = (
        df["Total Ridership"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["date"] = pd.to_datetime(df["Month"] + f" {year}", format="%B %Y")

    all_ridership.append(df[["date", "Total Ridership"]])

ridership = pd.concat(all_ridership, ignore_index=True)
ridership = ridership.rename(columns={"Total Ridership": "ridership"})

# ----------------------------
# 2. Clean fuel price dataset
# ----------------------------
fuel = pd.read_csv(DATA_DIR / "fuelprice.csv")

fuel = fuel[fuel["series_type"] == "level"].copy()
fuel["date"] = pd.to_datetime(fuel["date"])

fuel = fuel[
    (fuel["date"].dt.year >= 2021) &
    (fuel["date"].dt.year <= 2025)
].copy()

fuel["month"] = fuel["date"].dt.to_period("M")

monthly_fuel = (
    fuel.groupby("month", as_index=False)["ron95"]
    .mean()
)

monthly_fuel["date"] = monthly_fuel["month"].dt.to_timestamp()
monthly_fuel = monthly_fuel.rename(columns={"ron95": "ron95_price"})
monthly_fuel = monthly_fuel[["date", "ron95_price"]]

# ----------------------------
# 3. Merge ridership + fuel
# ----------------------------
combined = pd.merge(
    ridership,
    monthly_fuel,
    on="date",
    how="inner"
)

combined = combined.sort_values("date")

combined.to_csv(DATA_DIR / "fuel_vs_ridership.csv", index=False)

print(combined)