"""
Data Preparation - Electric Vehicle Market Performance & Insights
-----------------------------------------------------------------
Source: Kaggle - "Electric Vehicle Market Classification Dataset" (tharishreddy22, MIT)
        https://www.kaggle.com/datasets/tharishreddy22/electric-vehicle-market-classification-dataset

Usage:
    python data_preparation.py data/ev_market_train.csv data/ev_market_test.csv
Output:
    data/ev_market_clean.csv   (single, Tableau-ready file)

Steps:
 1. Combine train + test splits (they share the same 37 columns).
 2. Remove duplicate vehicle_ids and trim text fields.
 3. Handle the ~1-3% injected nulls:
      battery_cycle_life       -> median by battery_type
      resale_value_pct_3yr     -> median by category
      infotainment_screen_inch -> median by category
      annual_sales_units       -> median by category + manufacturer (fallback: category)
      customer_rating          -> median by category
    A flag column records which rows were imputed for sales/rating.
 4. Add analysis-friendly derived columns (bands, segments, ratios).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SEGMENT_MAP = {
    "Micro City Car": "Passenger", "Hatchback": "Passenger", "Sedan": "Passenger",
    "Luxury Sedan": "Passenger", "Compact SUV": "Passenger", "Crossover": "Passenger",
    "Full-size SUV": "Passenger", "Luxury SUV": "Passenger", "Sports Car": "Passenger",
    "Pickup Truck": "Commercial", "Van / MPV": "Commercial",
    "Electric Bus": "Commercial", "Electric Truck": "Commercial",
    "Two-Wheeler Scooter": "Micro-mobility", "Three-Wheeler": "Micro-mobility",
}


def fill_group_median(df, col, by):
    df[col] = df[col].fillna(df.groupby(by)[col].transform("median"))
    return df


def prepare(paths):
    df = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)
    print(f"Loaded {len(df):,} rows x {df.shape[1]} columns")
    print("Nulls before:\n", df.isna().sum()[df.isna().sum() > 0])

    df = df.drop_duplicates(subset="vehicle_id")
    for c in df.select_dtypes(include=["object", "string"]).columns:
        df[c] = df[c].str.strip()

    df["sales_imputed"] = df["annual_sales_units"].isna()
    df["rating_imputed"] = df["customer_rating"].isna()

    fill_group_median(df, "battery_cycle_life", "battery_type")
    fill_group_median(df, "resale_value_pct_3yr", "category")
    fill_group_median(df, "infotainment_screen_inch", "category")
    fill_group_median(df, "annual_sales_units", ["category", "manufacturer"])
    fill_group_median(df, "annual_sales_units", "category")
    fill_group_median(df, "customer_rating", "category")
    df["annual_sales_units"] = df["annual_sales_units"].round().astype("int64")
    df["customer_rating"] = df["customer_rating"].round(2)

    # Derived columns
    df["vehicle_segment"] = df["category"].map(SEGMENT_MAP).fillna("Other")
    df["price_band"] = pd.cut(df["price_usd"],
                              [0, 15000, 35000, 60000, 100000, np.inf],
                              labels=["<15K", "15K-35K", "35K-60K", "60K-100K", "100K+"])
    df["range_band"] = pd.cut(df["range_km"], [0, 150, 300, 450, 600, np.inf],
                              labels=["<150 km", "150-300 km", "300-450 km", "450-600 km", "600+ km"])
    df["rating_band"] = pd.cut(df["customer_rating"], [0, 2, 3, 4, 5.01],
                               labels=["Poor (<2)", "Average (2-3)", "Good (3-4)", "Excellent (4-5)"],
                               right=False)
    df["revenue_usd"] = df["annual_sales_units"] * df["price_usd"]
    df["range_per_kwh"] = (df["range_km"] / df["battery_capacity_kwh"]).round(2)
    df["price_per_km_range"] = (df["price_usd"] / df["range_km"]).round(2)
    df["power_to_weight_kw_per_t"] = (df["motor_power_kw"] / (df["weight_kg"] / 1000)).round(1)

    print("Nulls after:", int(df.isna().sum().sum()))
    return df


if __name__ == "__main__":
    inputs = sys.argv[1:] or ["data/ev_market_train.csv", "data/ev_market_test.csv"]
    out = Path("data/ev_market_clean.csv")
    clean = prepare(inputs)
    out.parent.mkdir(exist_ok=True)
    clean.to_csv(out, index=False)
    print(f"Saved {len(clean):,} rows -> {out}")
