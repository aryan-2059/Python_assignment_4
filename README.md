# Weather Analysis Report

## Dataset Overview

- Number of days: 3557
- Temperature: mean=25.40°C, min=6.50°C, max=39.50°C, std=7.32
- Rainfall: mean=2.46 mm, std=10.63 mm

## Key Insights

- Daily temperature trends are shown in `daily_temperature.png`.
- Monthly rainfall totals are summarised in `monthly_rainfall.png`.
- The relationship between humidity and temperature is visualised in `humidity_vs_temperature.png`.
- Combined trends for temperature and rainfall are shown in `combined_temp_rain.png`.

## Grouped Statistics

Monthly statistics are exported to `weather_monthly_summary.csv`, yearly statistics to `weather_yearly_summary.csv`, and seasonal statistics to `weather_season_stats.csv`.

## Features
- **Data Cleaning:** Automatically removes index columns, standardizes headers, and imputes missing values (Mean for Temp, Median for Humidity).
- **Time-Series Analysis:** Resamples daily data into Monthly and Yearly summaries.
- **Seasonal Analysis:** Groups data into seasons (Winter, Summer, Monsoon, Post-Monsoon) for climatic trending.
- **Visualization:** Generates professional plots:
  - Daily Temperature Trends (Line Plot)
  - Monthly Rainfall (Bar Chart)
  - Temperature vs. Humidity (Scatter Plot)
