import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8")   # nicer defaults

# 1) Load CSV
df = pd.read_csv("daily_weather.csv")

# Drop the first unnamed index column if present
if df.columns[0].lower().startswith("unnamed") or df.columns[0] == "":
    df = df.drop(columns=[df.columns[0]])

# Basic inspection (printed to console)
print("==== HEAD ====")
print(df.head())
print("\n==== INFO ====")
print(df.info())
print("\n==== DESCRIBE ====")
print(df.describe())

# Rename columns to simpler names used later
df = df.rename(columns={
    "DATE": "date",
    "precip": "rainfall"
})

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Keep only relevant columns
cols = ["date", "temp", "rainfall", "humidity"]
df = df[cols]

# Handle missing values (simple but acceptable for lab)
df["temp"] = df["temp"].fillna(df["temp"].mean())
df["humidity"] = df["humidity"].fillna(df["humidity"].median())
df["rainfall"] = df["rainfall"].fillna(0)

# Sort by date just in case and set index
df = df.sort_values("date").reset_index(drop=True)
df = df.set_index("date")

# 3) Statistical analysis with NumPy and resample
daily_temp = df["temp"].values
temp_mean = np.mean(daily_temp)
temp_min = np.min(daily_temp)
temp_max = np.max(daily_temp)
temp_std = np.std(daily_temp)
print("Daily temp: mean, min, max, std =",
      temp_mean, temp_min, temp_max, temp_std)

# Monthly statistics
monthly = df.resample("M").agg({
    "temp": ["mean", "min", "max", "std"],
    "rainfall": "sum",
    "humidity": "mean"
})
print("\n==== MONTHLY SAMPLE ====")
print(monthly.head())

# Yearly statistics
yearly = df.resample("Y").agg({
    "temp": ["mean", "min", "max", "std"],
    "rainfall": "sum",
    "humidity": "mean"
})
print("\n==== YEARLY ====")
print(yearly)

rain_mean = np.mean(df["rainfall"].values)
rain_std = np.std(df["rainfall"].values)
print("Overall rainfall mean/std:", rain_mean, rain_std)

# 4) Visualisation with Matplotlib
plt.figure(figsize=(10, 4))
plt.plot(df.index, df["temp"], color="tab:red")
plt.title("Daily Temperature")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.savefig("daily_temperature.png", dpi=300)
plt.close()

monthly_rain = df["rainfall"].resample("M").sum()

plt.figure(figsize=(10, 4))
plt.bar(monthly_rain.index.strftime("%Y-%m"), monthly_rain.values, color="tab:blue")
plt.xticks(rotation=45, ha="right")
plt.title("Monthly Rainfall")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.tight_layout()
plt.savefig("monthly_rainfall.png", dpi=300)
plt.close()

plt.figure(figsize=(6, 5))
plt.scatter(df["temp"], df["humidity"], alpha=0.5)
plt.title("Humidity vs Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.savefig("humidity_vs_temperature.png", dpi=300)
plt.close()

fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
axes[0].plot(df.index, df["temp"], color="tab:red")
axes[0].set_title("Daily Temperature")
axes[1].bar(monthly_rain.index, monthly_rain.values, width=20, color="tab:blue")
axes[1].set_title("Monthly Rainfall")
axes[1].set_xlabel("Date")
plt.tight_layout()
plt.savefig("combined_temp_rain.png", dpi=300)
plt.close()

# 5) Grouping and aggregation (month + season)
df["month"] = df.index.month

month_stats = df.groupby("month").agg({
    "temp": ["mean", "max", "min"],
    "rainfall": "sum",
    "humidity": "mean"
})
print("\n==== BY MONTH ====")
print(month_stats)

def get_season(m: int) -> str:
    """Rough Indian-style seasons, adjust if needed for your location."""
    if m in [12, 1, 2]:
        return "Winter"
    if m in [3, 4, 5]:
        return "Summer"
    if m in [6, 7, 8, 9]:
        return "Monsoon"
    return "Post-Monsoon"

df["season"] = df["month"].apply(get_season)

season_stats = df.groupby("season").agg({
    "temp": ["mean", "max", "min"],
    "rainfall": "sum",
    "humidity": "mean"
})
print("\n==== BY SEASON ====")
print(season_stats)

# 6) Export cleaned data and summaries
clean_export = df.drop(columns=["month", "season"])
clean_export.to_csv("weather_cleaned.csv", index=True)
monthly.to_csv("weather_monthly_summary.csv")
yearly.to_csv("weather_yearly_summary.csv")
season_stats.to_csv("weather_season_stats.csv")

# Simple Markdown report for storytelling
with open("weather_report.md", "w", encoding="utf-8") as f:
    f.write("# Weather Analysis Report\n\n")
    f.write("## Dataset Overview\n")
    f.write(f"- Number of days: {len(df)}\n")
    f.write(f"- Temperature: mean={temp_mean:.2f}°C, min={temp_min:.2f}°C, "
            f"max={temp_max:.2f}°C, std={temp_std:.2f}\n")
    f.write(f"- Rainfall: mean={rain_mean:.2f} mm, std={rain_std:.2f} mm\n\n")

    f.write("## Key Insights\n")
    f.write("- Daily temperature trends are shown in `daily_temperature.png`.\n")
    f.write("- Monthly rainfall totals are summarised in `monthly_rainfall.png`.\n")
    f.write("- The relationship between humidity and temperature is visualised in "
            "`humidity_vs_temperature.png`.\n")
    f.write("- Combined trends for temperature and rainfall are shown in "
            "`combined_temp_rain.png`.\n\n")

    f.write("## Grouped Statistics\n")
    f.write("Monthly statistics are exported to `weather_monthly_summary.csv`, "
            "yearly statistics to `weather_yearly_summary.csv`, and seasonal "
            "statistics to `weather_season_stats.csv`.\n")

print("Analysis complete. Outputs saved as CSV, PNG, and Markdown report.")