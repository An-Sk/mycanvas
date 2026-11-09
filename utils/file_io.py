"""
File I/O utilities for the canvas agent.
"""

import re, json
from pathlib import Path

def read_file(path: str) -> str:
    """Read file content as UTF-8 string."""
    return Path(path).read_text(encoding="utf-8")

def save_json(data: dict, path: str):
    """Save dictionary as JSON file, UTF-8, with indent=2."""
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_md(data: dict, path: str):
    """Save dictionary as JSON file, UTF-8, with indent=2."""
    Path(path).write_text(data, encoding="utf-8")



def extract_json(text: str) -> dict:
    """Extract first valid JSON object from text."""
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found")
    return json.loads(match.group(0))

def ensure_folder(path: str):
    """Ensure the parent folder for a file exists."""
    folder = Path(path).parent
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
        return True
    return False