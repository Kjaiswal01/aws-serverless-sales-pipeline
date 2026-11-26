import pandas as pd
import os

RAW_FILE = "data/raw/sales_day1.csv"
PROCESSED_FILE = "data/processed/cleaned_sales_day1.csv"
FAILED_FILE = "data/failed/failed_sales_day1.csv"

def run_etl():
    df = pd.read_csv(RAW_FILE)

    # Validation rules: quantity > 0 and price is not null/positive
    valid_mask = (df["quantity"] > 0) & (df["price"].notna()) & (df["price"] > 0)

    valid_df = df[valid_mask].copy()
    failed_df = df[~valid_mask].copy()

    # Transformation: add total_amount column & standardize city names
    valid_df["total_amount"] = valid_df["quantity"] * valid_df["price"]
    valid_df["city"] = valid_df["city"].str.strip().str.title()

    valid_df.to_csv(PROCESSED_FILE, index=False)
    failed_df.to_csv(FAILED_FILE, index=False)

    print(f"ETL Complete! Valid rows: {len(valid_df)} | Failed rows: {len(failed_df)}")

if __name__ == "__main__":
    run_etl()
