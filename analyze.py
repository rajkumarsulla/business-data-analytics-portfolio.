"""Compute retail KPIs from synthetic transaction line items."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_sales(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["order_date"])
    required = {"order_id", "order_date", "category", "product", "quantity", "unit_price", "unit_cost"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(df.columns))}")
    if df.empty or df[list(["quantity", "unit_price", "unit_cost"])].isna().any().any():
        raise ValueError("Dataset is empty or has missing numeric values")
    if (df["quantity"] <= 0).any() or (df[["unit_price", "unit_cost"]] < 0).any().any():
        raise ValueError("Invalid quantity, price, or cost")
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["profit"] = df["revenue"] - df["quantity"] * df["unit_cost"]
    return df


def summarize(df: pd.DataFrame):
    revenue = float(df["revenue"].sum())
    profit = float(df["profit"].sum())
    orders = int(df["order_id"].nunique())
    kpis = pd.DataFrame([{
        "total_revenue": revenue,
        "total_profit": profit,
        "total_orders": orders,
        "average_order_value": revenue / orders if orders else 0,
        "profit_margin_pct": profit / revenue * 100 if revenue else 0,
    }])
    categories = df.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    return kpis, categories.sort_values("revenue", ascending=False)


def main():
    df = load_sales(ROOT / "data" / "raw" / "sales.csv")
    kpis, categories = summarize(df)
    out = ROOT / "reports"
    out.mkdir(exist_ok=True)
    kpis.to_csv(out / "kpi_summary.csv", index=False)
    categories.to_csv(out / "category_summary.csv", index=False)
    print(kpis.to_string(index=False))
    print(categories.to_string(index=False))


if __name__ == "__main__":
    main()
