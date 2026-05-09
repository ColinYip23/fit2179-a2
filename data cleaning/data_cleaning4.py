import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Load dataset
df = pd.read_csv(DATA_DIR / "fuelprice.csv")

# Keep only actual fuel price levels
df = df[df["series_type"] == "level"].copy()

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Keep only 2021-2025
df = df[
    (df["date"].dt.year >= 2021) &
    (df["date"].dt.year <= 2025)
].copy()

# Create year-month column
df["month"] = df["date"].dt.to_period("M").astype(str)

# Compute monthly average RON95 price
monthly_ron95 = (
    df.groupby("month", as_index=False)["ron95"]
      .mean()
)

# Optional rounding
monthly_ron95["ron95"] = monthly_ron95["ron95"].round(2)

# Save cleaned dataset
monthly_ron95.to_csv(DATA_DIR / "monthly_ron95_2021_2025.csv", index=False)

print(monthly_ron95)
