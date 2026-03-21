Open terminal in that folder.

Then run:

python fetch_etf_prices.py
python fetch_hungary_cpi.py
python fetch_hungary_rates.py
python fetch_bond_reference.py

or:

python src\cases\hungarian-inflation-bond-vs-alternatives\process\run_full_dataset_pipeline.py --output-dir cases\hungarian-inflation-bond-vs-alternatives\outputs\02_process

You will get:

etf_prices_daily.csv
etf_prices_daily.csv.meta.json

hungary_cpi_yoy.csv
hungary_cpi_yoy.csv.meta.json

hungary_10y_yield.csv
hungary_10y_yield.csv.meta.json

bond_reference_template.csv
bond_reference_template.csv.meta.json



