from __future__ import annotations

from pathlib import Path

CANONICAL_TICKERS = [
    "XLB",
    "XLE",
    "XLF",
    "XLI",
    "XLK",
    "XLP",
    "XLU",
    "XLV",
    "XLY",
    "XLC",
    "XLRE",
    "SPY",
]

REQUIRED_COLUMNS = [
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
]

DEFAULT_START_DATE = "2010-01-01"


def get_repo_root() -> Path:
    """
    Expected file location:
    repo_root/src/cases/market-structure-consistency/config.py
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "src":
            return parent.parent
    raise RuntimeError("Could not resolve repo root.")


def get_case_root() -> Path:
    return get_repo_root() / "cases" / "market-structure-consistency"


def get_raw_data_dir() -> Path:
    return get_repo_root() / "data" / "raw"