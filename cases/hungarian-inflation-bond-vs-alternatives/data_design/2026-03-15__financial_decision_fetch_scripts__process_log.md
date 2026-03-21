# PROCESS — Raw Data Fetch Script Pack

Date: 2026-03-15  
Topic/Dataset: Financial Decision Dataset Fetch Scripts  
Input snapshot: dataset plan defined from the prior ASK artifacts

## 1. Purpose

This artifact documents the exact Python scripts prepared to fetch the raw datasets for the Hungary bond-vs-equity case study.

The script pack covers four acquisition tasks:

1. Daily ETF and SPY prices
2. Monthly Hungary CPI
3. Monthly Hungary 10-year government bond yield
4. Current PMÁP rates table plus a bond reference template for 2033/I

## 2. Output Files Created

### Python files
- [common_io.py] \src\cases\hungarian-inflation-bond-vs-alternatives\data_design\common_io.py)
- [fetch_etf_prices.py] \src\cases\hungarian-inflation-bond-vs-alternatives\data_design\fetch_etf_prices.py)
- [fetch_hungary_cpi.py] \src\cases\hungarian-inflation-bond-vs-alternatives\data_design\fetch_hungary_cpi.py)
- [fetch_hungary_rates.py] \src\cases\hungarian-inflation-bond-vs-alternatives\data_design\fetch_hungary_rates.py)
- [fetch_bond_reference.py] \src\cases\hungarian-inflation-bond-vs-alternatives\data_design\fetch_bond_reference.py)

## 3. Source Mapping

| Script | Dataset | Source | Output target |
|---|---|---|---|
| `fetch_etf_prices.py` | Daily ETF + SPY prices | Yahoo Finance via `yfinance` | `data/raw/market/etf_prices_daily.csv` |
| `fetch_hungary_cpi.py` | Hungary CPI YoY monthly | FRED CSV endpoint, OECD-backed Hungary CPI series | `data/raw/hungary_cpi_yoy.csv` |
| `fetch_hungary_rates.py` | Hungary 10Y government bond yield monthly | FRED CSV endpoint, OECD-backed yield series | `data/raw/hungary_10y_yield_monthly.csv` |
| `fetch_bond_reference.py` | Current PMÁP rates + bond reference template | Official allampapir.hu PMÁP pages | `data/raw/bond_reference_template.csv` |

## 4. Why these source choices were used

`yfinance` is an established Python wrapper for Yahoo Finance market data. Recent upstream discussion shows that `history/download` parameter behavior around `period` versus `start` and `end` has changed, so the ETF script uses explicit `start` and `end` arguments and avoids mixing them with `period`. :contentReference[oaicite:1]{index=1}

For Hungary CPI and Hungary 10-year yield, the scripts use direct FRED CSV endpoints because FRED exposes the relevant Hungary series and avoids extra API setup. The CPI series used is the monthly Hungary CPI total series, and the yield series used is the monthly Hungary 10-year government bond yield series. :contentReference[oaicite:2]{index=2}

For PMÁP, the script points to official allampapir.hu sources: the current PMÁP rates page, the PMÁP product page, and the 2033/I issuance PDF. The current rates page currently lists 2033/I and its current interest date/rate entry, while the product page confirms PMÁP is inflation-linked and variable-rate. :contentReference[oaicite:3]{index=3}

## 5. Run Instructions

in README.md file 

src\cases\hungarian-inflation-bond-vs-alternatives\data_design\README.md
