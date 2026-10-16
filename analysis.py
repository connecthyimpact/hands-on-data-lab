"""Hands-on data lab: cleaning, analysis, and visualisation."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(DATA_PATH)
    print("--- Initial inspection ---")
    print(df.head())
    print("\\nShape:", df.shape)
    print("\\nData types:\\n", df.dtypes)
    print("\\nMissing values:\\n", df.isna().sum())

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(df["units_sold"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.drop_duplicates()
    df = df.dropna(subset=["date", "region", "product", "units_sold", "unit_price"])
    df = df[(df["units_sold"] >= 0) & (df["unit_price"] >= 0)]
    df["revenue"] = df["units_sold"] * df["unit_price"]

    by_region = df.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    by_product = df.groupby("product", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    by_region.to_csv(OUTPUT_DIR / "revenue_by_region.csv", index=False)
    by_product.to_csv(OUTPUT_DIR / "revenue_by_product.csv", index=False)
    df.to_csv(OUTPUT_DIR / "cleaned_sales_data.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.bar(by_region["region"], by_region["revenue"])
    plt.title("Revenue by Region (Fictional Practice Data)")
    plt.xlabel("Region")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "revenue_by_region.png", dpi=150)
    plt.close()

    print("\\nTotal revenue:", round(df["revenue"].sum(), 2))
    print("\\nRevenue by region:\\n", by_region.to_string(index=False))
    print("\\nRevenue by product:\\n", by_product.to_string(index=False))
    print("\\nSaved results in:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
