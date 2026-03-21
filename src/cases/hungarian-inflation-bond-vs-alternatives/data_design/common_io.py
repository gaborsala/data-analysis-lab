from __future__ import annotations

import hashlib
import json
from pathlib import Path


def save_csv_with_metadata(df, output_dir: str | Path, filename: str) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    csv_path = output_path / filename
    df.to_csv(csv_path, index=False)

    sha = hashlib.sha256(csv_path.read_bytes()).hexdigest()

    meta = {
        "file": str(csv_path),
        "rows": len(df),
        "columns": list(df.columns),
        "sha256": sha
    }

    meta_path = csv_path.with_suffix(csv_path.suffix + ".meta.json")
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return csv_path