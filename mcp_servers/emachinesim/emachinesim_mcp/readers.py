from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def resolve_path(path: str | Path) -> Path:
    """Resolve a user-supplied path without requiring it to exist."""
    return Path(path).expanduser().resolve()


def require_file(path: str | Path) -> Path:
    p = resolve_path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")
    return p


def require_dir(path: str | Path) -> Path:
    p = resolve_path(path)
    if not p.is_dir():
        raise NotADirectoryError(f"Directory not found: {p}")
    return p


def read_json(path: str | Path) -> dict[str, Any]:
    p = require_file(path)
    with p.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {p}")
    return data


def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    p = require_file(path)
    with p.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_csv_if_exists(directory: str | Path, name: str) -> list[dict[str, str]]:
    p = resolve_path(directory) / name
    if not p.is_file():
        return []
    return read_csv_rows(p)


def to_float(value: Any, default: float | None = None) -> float | None:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if text == "":
        return default
    try:
        return float(text)
    except ValueError:
        return default


def to_int(value: Any, default: int | None = None) -> int | None:
    if value is None:
        return default
    if isinstance(value, int):
        return value
    text = str(value).strip()
    if text == "":
        return default
    try:
        return int(float(text))
    except ValueError:
        return default


def numeric_row(row: dict[str, str], keys: list[str]) -> dict[str, float | None]:
    return {key: to_float(row.get(key)) for key in keys}


def first_row(rows: list[dict[str, str]]) -> dict[str, str]:
    return rows[0] if rows else {}


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


def rows_to_dict(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        row_key = row.get(key, "")
        if row_key:
            result[row_key] = row
    return result

