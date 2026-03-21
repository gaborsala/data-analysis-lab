# PREPARE SUPPORT OUTPUT

## Canonical dataset
- Source kind: zip_archive
- Source path: `C:\Users\Lazarus\Github\data-analysis-lab\data\raw\SPDR_SECTOR_ETFS.zip`
- Canonical dataset: `C:\Users\Lazarus\Github\data-analysis-lab\cases\spdr-sector-etfs\outputs\02_prepare\all_sectors.csv`

## Dataset size
- Rows: 61448
- Columns: 8
- Date range: 1998-12-22 00:00:00 → 2024-06-24 00:00:00
- Unique tickers: 11
- Unique sectors: 11

## File inventory
- all_sectors.csv | columns=8 | ticker, sector, date, open, high, low, close, volume
- individual_data/XLB.csv | columns=7 | ticker, date, open, high, low, close, volume
- individual_data/XLC.csv | columns=7 | ticker, date, open, high, low, close, volume
- individual_data/XLE.csv | columns=7 | ticker, date, open, high, low, close, volume
- individual_data/XLF.csv | columns=7 | ticker, date, open, high, low, close, volume
- individual_data/XLI.csv | columns=7 | ticker, date, open, high, low, close, volume
- individual_data/XLK.csv | columns=7 | ticker, date, open, high, low, close, volume
- individual_data/XLP.csv | columns=7 | ticker, date, open, high, low, close, volume
- individual_data/XLRE.csv | columns=7 | ticker, date, open, high, low, close, volume
- individual_data/XLU.csv | columns=7 | ticker, date, open, high, low, close, volume
- individual_data/XLV.csv | columns=7 | ticker, date, open, high, low, close, volume
- individual_data/XLY.csv | columns=7 | ticker, date, open, high, low, close, volume

## Integrity checks
- row_count: 61448 [info] 
- column_count: 8 [info] 
- duplicate_ticker_date_rows: 0 [pass] Composite key candidate: ticker + date
- date_parse_failures: 0 [pass] 
- weekend_dated_rows: 0 [pass] 
- negative_open: 0 [pass] 
- zero_open: 0 [pass] 
- negative_high: 0 [pass] 
- zero_high: 0 [pass] 
- negative_low: 0 [pass] 
- zero_low: 0 [pass] 
- negative_close: 0 [pass] 
- zero_close: 0 [pass] 
- negative_volume: 0 [pass] 
- zero_volume: 6 [info] 
- high_lt_open: 0 [pass] 
- high_lt_close: 0 [pass] 
- low_gt_open: 0 [pass] 
- low_gt_close: 0 [pass] 
- high_lt_low: 0 [pass] 

## Missing by column
- ticker: 0
- sector: 0
- date: 0
- open: 0
- high: 0
- low: 0
- close: 0
- volume: 0

## Ticker coverage
- XLB: 1998-12-22 00:00:00 → 2024-06-24 00:00:00 | rows=6416
- XLC: 2018-06-19 00:00:00 → 2024-06-24 00:00:00 | rows=1513
- XLE: 1998-12-22 00:00:00 → 2024-06-24 00:00:00 | rows=6416
- XLF: 1998-12-22 00:00:00 → 2024-06-24 00:00:00 | rows=6416
- XLI: 1998-12-22 00:00:00 → 2024-06-24 00:00:00 | rows=6416
- XLK: 1998-12-22 00:00:00 → 2024-06-24 00:00:00 | rows=6416
- XLP: 1998-12-22 00:00:00 → 2024-06-24 00:00:00 | rows=6416
- XLRE: 2015-10-08 00:00:00 → 2024-06-24 00:00:00 | rows=2191
- XLU: 1998-12-22 00:00:00 → 2024-06-24 00:00:00 | rows=6416
- XLV: 1998-12-22 00:00:00 → 2024-06-24 00:00:00 | rows=6416
- XLY: 1998-12-22 00:00:00 → 2024-06-24 00:00:00 | rows=6416
