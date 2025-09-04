"""File search utilities for the canvas agent."""

import os
from pathlib import Path
from typing import List, Optional

def find_files(
    directory: str,
    pattern: str = "*.md",
    recursive: bool = True
) -> List[str]:
    """Find files matching pattern in directory.

    Args:
        directory: Directory to search in
        pattern: File pattern to match (e.g., "*.md")
        recursive: Whether to search recursively

    Returns:
        List of matching file paths
    """
    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if recursive:
        return [str(p) for p in path.rglob(pattern)]
    else:
        return [str(p) for p in path.glob(pattern)]

def validate_file_path(file_path: str) -> str:
    """Validate file path exists and is accessible.

    Args:
        file_path: Path to validate

    Returns:
        Validated file path

    Raises:
        FileNotFoundError: If file does not exist
        PermissionError: If file cannot be read
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Cannot read file: {file_path}")
    return str(path)