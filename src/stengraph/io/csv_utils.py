import csv
from pathlib import Path


def load_csv_rows(path: str | Path) -> list[dict[str, str]]:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Results CSV not found: {path}")
    with path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    if not rows:
        raise ValueError(f"Results CSV is empty: {path}")
    return rows
