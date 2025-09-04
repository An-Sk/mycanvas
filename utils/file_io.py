"""
File I/O utilities for the canvas agent.
"""

import json
from pathlib import Path

def read_file(path: str) -> str:
    """Read file content as UTF-8 string."""
    return Path(path).read_text(encoding="utf-8")

def save_json(data: dict, path: str):
    """Save dictionary as JSON file, UTF-8, with indent=2."""
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")