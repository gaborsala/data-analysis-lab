1. Case Metadata
Project Name: Energy Market Dashboard
Case ID: 2026-EMD-001
Phase: PREPARE
Author: Gábor Sala
Date: 2026-03-29
Project Type: Dashboard / Visualization Project
2. PREPARE Phase Purpose

The PREPARE phase defines the data foundation before any cleaning, transformation, feature engineering, or dashboard development begins.

Its purpose is to:

identify the required datasets
define expected schema
verify source accessibility
document data limitations
establish validation rules
reduce downstream ambiguity in PROCESS and ANALYZE

This phase does not perform cleaning or interpretation.
It establishes a controlled input layer.

3. Data Requirements
3.1 Target Universe (V1)

The dashboard will use the following instruments:

WTI Crude Oil
Brent Crude Oil
Natural Gas
XLE — Energy Select Sector SPDR Fund
SPY — SPDR S&P 500 ETF Trust
3.2 Analytical Role of Each Dataset
Instrument	Role in Project
WTI	Core crude oil benchmark
Brent	Secondary global crude benchmark
Natural Gas	Energy commodity volatility component
XLE	Energy equity proxy
SPY	Broad market benchmark for relative comparison
4. Data Source Plan
4.1 Primary Source

Primary source for V1:

Yahoo Finance via yfinance

Rationale:

accessible in Python
widely used in portfolio projects
sufficient for dashboard demonstration
supports commodity futures proxies and ETFs
4.2 Candidate Tickers for Validation

Initial ticker candidates to verify in implementation:

Asset	Candidate Ticker
WTI Crude Oil	CL=F
Brent Crude Oil	BZ=F
Natural Gas	NG=F
XLE	XLE
SPY	SPY

Note: ticker availability must be confirmed during source validation. If one symbol fails or returns unstable history, the fallback must be logged before PROCESS begins.

4.3 Fallback Principle

If one dataset cannot be reliably fetched:

log the issue explicitly
test an alternative ticker or source
document the substitution
do not silently replace series

This protects reproducibility.

5. Expected Raw Data Schema

Expected raw input schema from yfinance after download and standardization:

Column	Expected Type	Description
date	datetime64	Trading date
ticker	string	Asset identifier
open	float	Session open price
high	float	Session high price
low	float	Session low price
close	float	Session close price
adj_close	float	Adjusted close price
volume	float / int	Trading volume if available
5.1 Standardized Required Schema

After normalization, the dataset must conform to:

date
ticker
open
high
low
close
adj_close
volume

Column naming must be lowercase and snake_case compatible.

5.2 Schema Rules
date must be parseable as datetime
ticker must be non-null
price columns must be numeric
duplicate rows on (date, ticker) are not allowed
rows must be sorted by ticker, date
missingness must be measured before PROCESS
6. Data Window Definition
6.1 Intended Historical Range

For V1, use a range large enough to support:

trend visualization
1M and 3M return metrics
rolling volatility windows
drawdown analysis

Recommended initial window:

5 years of daily data

This gives enough depth without unnecessary expansion.

6.2 Frequency
Daily frequency
No intraday data in V1

Reason:

simpler validation
clearer dashboard presentation
appropriate for portfolio-grade monitoring use case
7. Prepare Validation Checklist

Before entering PROCESS, validate the following:

7.1 Source Validation
all target instruments can be downloaded
data is non-empty
date coverage is acceptable
symbols map correctly to intended assets
7.2 Schema Validation
all required columns exist
column names are standardized
data types are inspectable and convertible
7.3 Integrity Validation
no exact duplicate rows by (date, ticker)
date parsing succeeds
required price fields are populated at acceptable levels
7.4 Coverage Validation
each ticker has sufficient history
major date gaps are identified
overlapping date window across all assets is known
8. Initial Data Risks
Risk	Description	PREPARE Response
Missing history	Some futures proxies may have inconsistent coverage	Measure min/max date per ticker
Schema inconsistency	Download format may differ by symbol/source	Standardize immediately after fetch
Null values	Volume or adjusted fields may be partially missing	Record null counts by column
Duplicate rows	Repeated pull or merge issues may create duplication	Validate on (date, ticker)
Non-overlapping dates	Commodity and ETF histories may not align perfectly	Document common window
9. Common Window Policy

The project must distinguish between:

full raw history per asset
common aligned history across all assets

This is important because commodities and ETFs may not have identical coverage.

Policy:

preserve raw history in raw dataset
compute dashboard-ready aligned dataset separately
document the common window explicitly

This prevents hidden distortions in relative comparisons.

10. Data Storage Plan

Recommended directory structure:

energy-market-dashboard/
├─ data/
│  ├─ raw/
│  │  └─ market_data_raw.csv
│  └─ processed/
│     └─ market_data_aligned.csv

Optional split-by-stage structure:

energy-market-dashboard/
├─ data/
│  ├─ raw/
│  │  ├─ wti_raw.csv
│  │  ├─ brent_raw.csv
│  │ ├─ natgas_raw.csv
│  │ ├─ xle_raw.csv
│  │ └─ spy_raw.csv
│  └─ processed/
│     ├─ market_data_combined.csv
│     └─ market_data_aligned.csv

For portfolio clarity, the second structure is often stronger because it shows source-level control.

11. PREPARE Outputs

The PREPARE phase should produce:

11.1 Raw acquisition output
raw downloaded files or one combined raw file
11.2 Prepare audit output

A summary table including:

ticker
row count
min date
max date
null counts
duplicate count
schema check result
11.3 Prepare documentation
this PREPARE artifact
optional data_dictionary.md
optional prepare_audit.csv
12. Prepare Audit Specification

Recommended audit fields:

Field	Description
ticker	Asset symbol
row_count	Number of rows
min_date	Earliest date
max_date	Latest date
null_open	Null count in open
null_high	Null count in high
null_low	Null count in low
null_close	Null count in close
null_adj_close	Null count in adj_close
null_volume	Null count in volume
duplicate_date_ticker	Duplicate count by (date, ticker)
schema_ok	Yes/No
notes	Validation notes
13. Acceptance Criteria for PREPARE Completion

PREPARE is complete when:

all five target instruments are successfully sourced or substitution is documented
schema is standardized
row counts and date coverage are known
duplicates and nulls are measured
common aligned date window is identified
raw inputs are stored reproducibly

Only after these are complete should PROCESS begin.

14. Out of Scope for PREPARE

The following do not belong in this phase:

return calculations
volatility calculations
drawdown calculations
dashboard UI design
insight interpretation
business conclusions

Those belong later.

15. Transition to PROCESS

Next phase:

PROCESS

Focus:

cleaning
date alignment
null handling rules
adjusted close selection logic
feature-ready structured dataset creation
16. PREPARE Summary

This PREPARE phase establishes a controlled data input layer for the Energy Market Dashboard by:

defining the asset universe
fixing the expected schema
setting source validation rules
documenting integrity risks
preparing the path to aligned downstream analysis

The objective is not complexity.
The objective is clean analytical footing.