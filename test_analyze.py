from pathlib import Path
import pytest
from src.analyze import load_sales, summarize


def test_sample_kpis():
    data = load_sales(Path(__file__).resolve().parents[1] / "data/raw/sales.csv")
    kpis, categories = summarize(data)
    assert kpis.loc[0, "total_orders"] == 6
    assert kpis.loc[0, "total_revenue"] == 353
    assert len(categories) == 3


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_sales(Path("nonexistent.csv"))
