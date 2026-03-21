.\How to run:

python src\cases\spdr_sector_etfs\prepare\run_prepare_phase.py data\raw\SPDR_SECTOR_ETFS.zip --extract-dir cases\spdr-sector-etfs\outputs\02_prepare --output-dir cases\spdr-sector-etfs\outputs\02_prepare 

What each file does:

prepare_schema_checks.py
Core validation logic: schema inference, duplicate checks, date checks, OHLC checks, zero/negative scans.

prepare_dataset_audit.py
Main audit engine: reads ZIP or CSV, finds the canonical dataset, profiles structure, and saves a JSON summary.

run_prepare_phase.py
Convenience wrapper: runs the audit and writes both JSON and markdown support outputs for your PREPARE artifact.