"""
Shared utility functions for the Autonomy Loop backend.

This module provides helper routines to read and write JSONL and JSON files
used by the system. Keeping common logic here keeps the other modules
focused on their primary responsibilities.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Generator, Dict, Any, Iterable


BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOOP_DATA_DIR = BASE_DIR / "loop_data"


def read_jsonl(path: str | Path) -> Generator[Dict[str, Any], None, None]:
    """Yield dictionaries from a JSON Lines file.

    Each line in a JSONL file should be a valid JSON object.

    Args:
        path: The path to the JSONL file.

    Yields:
        Parsed JSON objects from each line.
    """
    file_path = Path(path)
    if not file_path.exists():
        return
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def write_json(path: str | Path, data: Dict[str, Any]) -> None:
    """Write a dictionary to a JSON file.

    Args:
        path: The path to the file to create.
        data: The dictionary to serialize.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json(path: str | Path) -> Dict[str, Any]:
    """Read a dictionary from a JSON file.

    Args:
        path: The path to the JSON file.

    Returns:
        The parsed dictionary, or an empty dict if the file does not exist.
    """
    file_path = Path(path)
    if not file_path.exists():
        return {}
    with file_path.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def get_latest_market_topic() -> str | None:
    """Return the latest trending topic from the market scan file.

    This function inspects the JSONL file produced by the market agent and returns
    the most recent topic string. If no topics have been scanned yet, None is
    returned.
    """
    scan_path = LOOP_DATA_DIR / "market_scan.jsonl"
    last_entry = None
    for entry in read_jsonl(scan_path):
        last_entry = entry
    return last_entry.get("topic") if last_entry else None


def get_offer_data() -> Dict[str, Any]:
    """Return the latest offer data from the loop data directory.

    Offers are stored as JSON files in the loop_data directory. This helper
    reads the offer.json if it exists and returns the parsed dictionary.
    """
    offer_path = LOOP_DATA_DIR / "offer.json"
    return read_json(offer_path)
