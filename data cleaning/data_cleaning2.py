import pandas as pd

# 1. Load both datasets
old_df = pd.read_csv("PublicTransportUtilisationAveragePublicTransportRidership.csv")   # year, mode, ridership
daily_df = pd.read_csv("ridership_headline.csv") # date, rail columns

# 2. Clean first dataset: keep 2019-2024 MRT/LRT only
old_clean = old_df[
    (old_df["year"].between(2019, 2024)) &
    (old_df["mode"].isin(["MRT", "LRT"]))
].copy()

old_clean["source"] = "Singapore"

# 3. Clean second dataset: combine MRT and LRT columns
daily_df["date"] = pd.to_datetime(daily_df["date"])
daily_df["year"] = daily_df["date"].dt.year

mrt_cols = [col for col in daily_df.columns if "mrt" in col.lower()]
lrt_cols = [col for col in daily_df.columns if "lrt" in col.lower()]

daily_df[mrt_cols + lrt_cols] = daily_df[mrt_cols + lrt_cols].fillna(0)

daily_df["MRT"] = daily_df[mrt_cols].sum(axis=1)
daily_df["LRT"] = daily_df[lrt_cols].sum(axis=1)

# Convert daily data to yearly totals
daily_yearly = daily_df[
    daily_df["year"].between(2019, 2024)
].groupby("year", as_index=False)[["MRT", "LRT"]].sum()

# Convert wide format to long format
daily_clean = daily_yearly.melt(
    id_vars="year",
    value_vars=["MRT", "LRT"],
    var_name="mode",
    value_name="ridership"
)

daily_clean["source"] = "Malaysia"


# 4. Combine both cleaned datasets
combined = pd.concat([old_clean, daily_clean], ignore_index=True)

# Optional: sort nicely
combined = combined.sort_values(["year", "source", "mode"])

# 5. Save cleaned file
combined.to_csv("cleaned_mrt_lrt_2019_2024.csv", index=False)

print(combined)