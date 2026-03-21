# Run Guide

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Prepare raw data

Place raw files inside the expected data directory structure.

## 3. Run audit

```bash
python src/common/prepare_dataset_audit.py --input data/raw/example.csv --date_col date --ticker_col ticker --out_dir audit_output
```

## Notes

- Run commands from the repository root.
- Keep raw data out of Git unless explicitly intended.
- Treat markdown lifecycle files as first-class analytical outputs.
