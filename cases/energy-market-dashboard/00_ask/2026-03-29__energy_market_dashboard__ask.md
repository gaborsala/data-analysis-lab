1. Case Metadata
Project Name: Energy Market Dashboard
Case ID: 2026-EMD-001
Type: Dashboard / Visualization Project
Status: ASK Phase
Author: Gábor Sala
Date: 2026
2. Objective

Develop an interactive dashboard that provides a structured overview of the energy market by combining:

Commodity price behavior
Energy sector equity performance
Relative strength vs benchmark
Volatility and drawdown characteristics

The goal is to transform raw market data into a clear, interpretable visual system suitable for analytical monitoring.

3. Business Question

How can energy market conditions be monitored through a compact dashboard that integrates:

Oil and gas price dynamics
Energy equity performance
Relative strength vs the broad market
Risk characteristics (volatility, drawdowns)
4. Analytical Scope (V1 — Strict Boundary)
Included
Crude oil (WTI, Brent)
Natural gas
Energy ETF (XLE)
Benchmark ETF (SPY)
Derived Metrics
Returns (1D, 1M, 3M)
Relative performance (XLE / SPY)
Rolling volatility (e.g., 20D, 60D)
Drawdown
Dashboard Components
Market overview (KPIs)
Trend visualization
Relative strength comparison
Volatility / risk view
Excluded (V1)

To maintain clarity and avoid scope drift:

No macroeconomic overlays (rates, inflation)
No forecasting models
No machine learning
No sentiment analysis
No excessive asset expansion

Future ideas must be logged, not implemented.

5. Target Users
Entry-level data analyst recruiters
Hiring managers in finance / analytics
Self-directed learning (portfolio development)
6. Analytical Approach

The project follows a structured pipeline:

Data Acquisition
Download commodity and ETF data (e.g., via yfinance)
Data Preparation
Clean missing values
Align time indices
Normalize formats
Feature Engineering
Compute returns
Compute rolling volatility
Compute drawdowns
Compute relative strength (XLE/SPY)
Visualization Layer
Interactive dashboard using Streamlit
Clear separation of panels (overview, trends, risk)
7. Key Metrics Definition
Return (%)
Percentage price change over selected period
Relative Strength
Ratio of XLE to SPY
Rolling Volatility
Standard deviation of returns over a rolling window
Drawdown
Decline from previous peak
8. Expected Outputs
Primary Output
Interactive dashboard (app.py)
Supporting Outputs
Clean dataset (processed)
Feature dataset (returns, volatility, drawdown)
Visual charts (optional saved outputs)
9. Success Criteria

The project is successful if:

The dashboard runs locally without errors
Data pipeline is reproducible
Visualizations are clear and interpretable
Codebase is structured and readable
README clearly explains the system
10. Constraints
Use only Python-based tools (pandas, Streamlit, matplotlib/plotly)
Maintain clean repository structure
Avoid unnecessary complexity
Prioritize clarity over feature quantity
11. Risks & Mitigations
Risk	Mitigation
Data source instability	Add fallback or validation checks
Overcomplication	Strict V1 scope boundary
Inconsistent data alignment	Enforce unified date index
Visual clutter	Limit number of charts
12. Deliverables
GitHub repository:
energy-market-dashboard

Containing:

Streamlit dashboard (app.py)
Data pipeline scripts
Clean dataset
README.md (recruiter-focused)
13. Phase Transition

Next phase:

➡️ PREPARE

Focus:

Data sourcing
Schema definition
Data validation
Initial dataset audit