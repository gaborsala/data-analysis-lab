# Data Directory

This folder contains the data structure used by the repository.

## Layout

- `raw/` — original input data, usually excluded from Git
- `interim/` — temporary transformed data
- `processed/` — analysis-ready outputs when appropriate

## Version control policy

Large raw files, private datasets, ZIP archives, and temporary exports are generally excluded from version control.

A `.gitkeep` file may be used to preserve empty directories.