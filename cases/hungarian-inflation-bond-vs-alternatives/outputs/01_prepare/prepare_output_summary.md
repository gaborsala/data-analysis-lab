# PREPARE Output Summary

This file is machine-generated from PREPARE profiling outputs.

## 1. File-Level Profile

| file_name                   | file_path                            | sha256                                                           |   row_count |   column_count | columns                                                     |   duplicate_full_rows | dataset_name            | meta_found   |
|:----------------------------|:-------------------------------------|:-----------------------------------------------------------------|------------:|---------------:|:------------------------------------------------------------|----------------------:|:------------------------|:-------------|
| etf_prices_daily.csv        | data\raw\etf_prices_daily.csv        | ed9eeb3b64a84747c843643794bd3f4b2735da8aa37b5e63bfbc6887ca1b2a0b |       44814 |              3 | ['Date', 'ticker', 'close']                                 |                     0 | etf_prices_daily        | True         |
| hungary_cpi_yoy.csv         | data\raw\hungary_cpi_yoy.csv         | 518c0fbbc95d37be632f368f32433cfaba62ea2eab1d93078eedf9581f30925c |         184 |              2 | ['date', 'cpi_yoy']                                         |                     0 | hungary_cpi_yoy         | True         |
| hungary_10y_yield.csv       | data\raw\hungary_10y_yield.csv       | 0176713cc0be1ea3884b71dc20a868db867e30dbe8888ed2963b60f5c7456c98 |         325 |              2 | ['date', 'yield_10y']                                       |                     0 | hungary_10y_yield       | True         |
| bond_reference_template.csv | data\raw\bond_reference_template.csv | 8d7a4ad2afb9f34ab4f87ea25382f7accb7163d2913f3d046c10cb98973d4145 |           1 |              5 | ['bond_id', 'country', 'type', 'premium', 'redemption_fee'] |                     0 | bond_reference_template | True         |

## 2. Dataset Summary

| dataset_name            | file_name                   |   rows |   cols | date_columns_detected   |   total_missing_values |   duplicate_full_rows | meta_found   |
|:------------------------|:----------------------------|-------:|-------:|:------------------------|-----------------------:|----------------------:|:-------------|
| etf_prices_daily        | etf_prices_daily.csv        |  44814 |      3 | Date                    |                   3580 |                     0 | True         |
| hungary_cpi_yoy         | hungary_cpi_yoy.csv         |    184 |      2 | date                    |                      0 |                     0 | True         |
| hungary_10y_yield       | hungary_10y_yield.csv       |    325 |      2 | date                    |                      0 |                     0 | True         |
| bond_reference_template | bond_reference_template.csv |      1 |      5 | nan                     |                      0 |                     0 | True         |

## 3. Key Validation Summary

| key_columns        | missing_key_columns   |   key_duplicate_count |   null_in_key_count |   unique_key_count | valid   | dataset_name            | file_name                   |
|:-------------------|:----------------------|----------------------:|--------------------:|-------------------:|:--------|:------------------------|:----------------------------|
| ['Date', 'ticker'] | []                    |                     0 |                   0 |              44814 | True    | etf_prices_daily        | etf_prices_daily.csv        |
| ['date']           | []                    |                     0 |                   0 |                184 | True    | hungary_cpi_yoy         | hungary_cpi_yoy.csv         |
| ['date']           | []                    |                     0 |                   0 |                325 | True    | hungary_10y_yield       | hungary_10y_yield.csv       |
| ['bond_id']        | []                    |                     0 |                   0 |                  1 | True    | bond_reference_template | bond_reference_template.csv |

## 4. Validation Notes

- Row and column counts captured for each file.
- Full-row duplicates checked.
- Candidate primary keys evaluated.
- Column-level null counts profiled.
- Date parsing should still be verified during PROCESS.

## 5. Recommended Next Checks

- Review any duplicate-key extracts.
- Confirm ticker universe and date coverage by ticker.
- Confirm monthly continuity for CPI and 10Y yield.
- Normalize percentage strings in bond template during PROCESS.
