import os
from pathlib import Path



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