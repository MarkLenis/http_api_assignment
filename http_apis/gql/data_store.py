import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_json_data(filename: str) -> list[dict[str, Any]]:
    """Load list-based JSON data from the data directory."""
    file_path = DATA_DIR / filename
    with file_path.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


def save_json_data(filename: str, payload: list[dict[str, Any]]) -> None:
    """Persist list-based JSON data to the data directory."""
    file_path = DATA_DIR / filename
    with file_path.open("w", encoding="utf-8") as json_file:
        json.dump(payload, json_file, indent=2)
