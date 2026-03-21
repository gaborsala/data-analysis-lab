import zipfile
from pathlib import Path

zip_path = Path("98_DATA/ZIP//2026_03_02/SPDR_SECTOR_ETFS.zip")
extract_path = Path("data/raw/spdr")

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_path)