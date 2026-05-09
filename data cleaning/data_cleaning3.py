import pandas as pd

df = pd.read_csv("komuter_2026.csv")

# Combine ridership for the same time regardless of origin/destination
hourly = (
    df.groupby("time", as_index=False)["ridership"]
      .sum()
      .sort_values("time")
)

hourly.to_csv("hourly_ridership.csv", index=False)

print(hourly)