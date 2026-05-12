import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Load datasets
rapidrail = pd.read_csv(DATA_DIR / "rapidrail_2026_daily.csv")
brt = pd.read_csv(DATA_DIR / "brt_2026_daily.csv")

# Total ridership
lrt_mrt_total = rapidrail["ridership"].sum()
brt_total = brt["ridership"].sum()

# Split MRT and LRT using line prefixes
mrt_mask = rapidrail["origin"].str.startswith(("KG", "PY"))
lrt_mask = rapidrail["origin"].str.startswith(("KJ", "AG", "SP"))

mrt_total = rapidrail[mrt_mask]["ridership"].sum()
lrt_total = rapidrail[lrt_mask]["ridership"].sum()

# Create summary table
transport_share = pd.DataFrame({
    "transport_type": ["MRT", "LRT", "BRT"],
    "ridership": [mrt_total, lrt_total, brt_total]
})

transport_share.to_csv(DATA_DIR / "transport_share.csv", index=False)

print(transport_share)