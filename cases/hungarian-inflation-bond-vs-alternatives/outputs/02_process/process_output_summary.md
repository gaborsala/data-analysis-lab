# PROCESS Output Summary

Machine-generated summary of PROCESS outputs.

## 1. Raw Snapshot

           dataset_name                   file_name  row_count_raw  column_count_raw                                                           sha256
       etf_prices_daily        etf_prices_daily.csv          44814                 3 ed9eeb3b64a84747c843643794bd3f4b2735da8aa37b5e63bfbc6887ca1b2a0b
        hungary_cpi_yoy         hungary_cpi_yoy.csv            184                 2 518c0fbbc95d37be632f368f32433cfaba62ea2eab1d93078eedf9581f30925c
      hungary_10y_yield       hungary_10y_yield.csv            325                 2 0176713cc0be1ea3884b71dc20a868db867e30dbe8888ed2963b60f5c7456c98
bond_reference_template bond_reference_template.csv              1                 5 8d7a4ad2afb9f34ab4f87ea25382f7accb7163d2913f3d046c10cb98973d4145

## 2. ETF Ticker Coverage

ticker  row_count first_date_all last_date_all first_valid_close_date last_valid_close_date  non_null_close_count  null_close_count  min_close  max_close
   SPY       4074     2010-01-04    2026-03-16             2010-01-04            2026-03-16                  4074                 0  77.359528 695.489990
   XLB       4074     2010-01-04    2026-03-16             2010-01-04            2026-03-16                  4074                 0  10.017522  53.619999
   XLC       4074     2010-01-04    2026-03-16             2018-06-19            2026-03-16                  1945              2129  36.465855 120.080002
   XLE       4074     2010-01-04    2026-03-16             2010-01-04            2026-03-16                  4074                 0   9.305685  57.900002
   XLF       4074     2010-01-04    2026-03-16             2010-01-04            2026-03-16                  4074                 0   7.043540  56.400002
   XLI       4074     2010-01-04    2026-03-16             2010-01-04            2026-03-16                  4074                 0  19.929535 178.899994
   XLK       4074     2010-01-04    2026-03-16             2010-01-04            2026-03-16                  4074                 0   8.243013 151.834702
  XLRE       4074     2010-01-04    2026-03-16             2015-10-08            2026-03-16                  2623              1451  19.299820  45.145287
   XLU       4074     2010-01-04    2026-03-16             2010-01-04            2026-03-16                  4074                 0   8.159366  47.730000
   XLV       4074     2010-01-04    2026-03-16             2010-01-04            2026-03-16                  4074                 0  21.482485 160.199997
   XLY       4074     2010-01-04    2026-03-16             2010-01-04            2026-03-16                  4074                 0  11.753675 124.519997

## 3. ETF Null Window Classification

ticker first_valid_close_date last_valid_close_date  null_close_count  pre_inception_null_count  post_coverage_null_count  internal_active_window_null_count  has_internal_active_nulls
   SPY             2010-01-04            2026-03-16                 0                         0                         0                                  0                      False
   XLB             2010-01-04            2026-03-16                 0                         0                         0                                  0                      False
   XLC             2018-06-19            2026-03-16              2129                      2129                         0                                  0                      False
   XLE             2010-01-04            2026-03-16                 0                         0                         0                                  0                      False
   XLF             2010-01-04            2026-03-16                 0                         0                         0                                  0                      False
   XLI             2010-01-04            2026-03-16                 0                         0                         0                                  0                      False
   XLK             2010-01-04            2026-03-16                 0                         0                         0                                  0                      False
  XLRE             2015-10-08            2026-03-16              1451                      1451                         0                                  0                      False
   XLU             2010-01-04            2026-03-16                 0                         0                         0                                  0                      False
   XLV             2010-01-04            2026-03-16                 0                         0                         0                                  0                      False
   XLY             2010-01-04            2026-03-16                 0                         0                         0                                  0                      False

## 4. Monthly Merged Context Sample

ticker       Date  close_month_end year_month  cpi_yoy  yield_10y
   SPY 2010-01-31        80.571342    2010-01 6.404389   7.620000
   SPY 2010-02-28        83.084763    2010-02 5.748605   7.690000
   SPY 2010-03-31        88.142921    2010-03 5.943610   7.160000
   SPY 2010-04-30        89.506516    2010-04 5.645618   6.570000
   SPY 2010-05-31        82.394821    2010-05 5.081280   7.070000
   SPY 2010-06-30        78.131615    2010-06 5.276552   7.600000
   SPY 2010-07-31        83.468056    2010-07 3.977538   7.390000
   SPY 2010-08-31        79.713608    2010-08 3.687922   7.070000
   SPY 2010-09-30        86.852356    2010-09 3.744782   7.040000
   SPY 2010-10-31        90.170319    2010-10 4.186686   6.870000
   SPY 2010-11-30        90.170319    2010-11 4.186891   7.380000
   SPY 2010-12-31        96.198387    2010-12 4.688137   7.920000
   SPY 2011-01-31        98.439804    2011-01 3.978692   7.700000
   SPY 2011-02-28       101.859383    2011-02 4.073749   7.393000
   SPY 2011-03-31       101.871597    2011-03 4.531994   7.290000
   SPY 2011-04-30       104.821953    2011-04 4.655047   7.050000
   SPY 2011-05-31       103.646408    2011-05 3.939155   7.110000
   SPY 2011-06-30       101.897926    2011-06 3.454614   7.220000
   SPY 2011-07-31        99.859497    2011-07 3.087853   7.351905
   SPY 2011-08-31        94.369675    2011-08 3.584647   7.490000

## 5. Cleaning Rules Applied

- ETF rows with null close outside active valid window are removed.
- Internal active-window nulls are preserved for audit visibility and counted in summaries.
- Bond percent strings are normalized into numeric percentage-point columns.
- ETF daily prices are resampled to month-end last valid close by ticker.
- CPI and 10Y yield are aligned by `year_month`.
