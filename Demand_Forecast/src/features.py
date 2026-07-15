import pandas as pd
import numpy as np


def load_and_merge(train_path, store_path, test_path=None):
    train = pd.read_csv(train_path, parse_dates=["Date"], low_memory=False)
    store = pd.read_csv(store_path)
    train = train.merge(store, on="Store", how="left")
    if test_path:
        test = pd.read_csv(test_path, parse_dates=["Date"], low_memory=False)
        test = test.merge(store, on="Store", how="left")
        return train, test
    return train


def clean(df):
    df = df.copy()
    # Keep only open stores with positive sales (train only)
    if "Sales" in df.columns:
        df = df[(df["Open"] == 1) & (df["Sales"] > 0)]
    # Fill missing CompetitionDistance with a large value
    df["CompetitionDistance"] = df["CompetitionDistance"].fillna(df["CompetitionDistance"].median())
    # Fill missing promo2 date fields
    for col in ["CompetitionOpenSinceMonth", "CompetitionOpenSinceYear",
                "Promo2SinceWeek", "Promo2SinceYear"]:
        df[col] = df[col].fillna(0)
    df["PromoInterval"] = df["PromoInterval"].fillna("None")
    return df


def add_date_features(df):
    df = df.copy()
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)
    df["DayOfWeek"] = df["Date"].dt.dayofweek  # 0=Monday
    df["Quarter"] = df["Date"].dt.quarter
    df["IsWeekend"] = (df["DayOfWeek"] >= 5).astype(int)
    # Days since competition opened
    df["CompetitionOpen"] = (
        12 * (df["Year"] - df["CompetitionOpenSinceYear"])
        + (df["Month"] - df["CompetitionOpenSinceMonth"])
    ).clip(lower=0)
    # Weeks since Promo2 started
    df["Promo2Open"] = (
        (df["Year"] - df["Promo2SinceYear"]) * 52
        + (df["WeekOfYear"] - df["Promo2SinceWeek"])
    ).clip(lower=0) * df["Promo2"]
    return df


def add_lag_features(df, lags=(7, 14, 21, 28)):
    df = df.sort_values(["Store", "Date"]).copy()
    for lag in lags:
        df[f"Sales_lag_{lag}"] = (
            df.groupby("Store")["Sales"].shift(lag)
        )
    return df


def add_rolling_features(df, windows=(7, 14, 28)):
    df = df.sort_values(["Store", "Date"]).copy()
    for w in windows:
        df[f"Sales_roll_mean_{w}"] = (
            df.groupby("Store")["Sales"]
            .transform(lambda x: x.shift(1).rolling(w).mean())
        )
        df[f"Sales_roll_std_{w}"] = (
            df.groupby("Store")["Sales"]
            .transform(lambda x: x.shift(1).rolling(w).std())
        )
    return df


def encode_categoricals(df):
    df = df.copy()
    df["StoreType"] = df["StoreType"].map({"a": 0, "b": 1, "c": 2, "d": 3})
    df["Assortment"] = df["Assortment"].map({"a": 0, "b": 1, "c": 2})
    df["StateHoliday"] = df["StateHoliday"].map({"0": 0, 0: 0, "a": 1, "b": 2, "c": 3})
    return df


FEATURE_COLS = [
    "Store", "DayOfWeek", "Promo", "StateHoliday",
    "SchoolHoliday", "StoreType", "Assortment",
    "CompetitionDistance", "CompetitionOpen", "Promo2", "Promo2Open",
    "Year", "Month", "Day", "WeekOfYear", "Quarter", "IsWeekend",
    "Sales_lag_7", "Sales_lag_14", "Sales_lag_21", "Sales_lag_28",
    "Sales_roll_mean_7", "Sales_roll_mean_14", "Sales_roll_mean_28",
    "Sales_roll_std_7", "Sales_roll_std_14", "Sales_roll_std_28",
]
