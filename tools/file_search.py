"""File search utilities for the canvas agent."""


from pathlib import Path
from typing import List, Optional
from utils.logger import logger

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
        matches = [str(p) for p in path.rglob(pattern)]
    else:
        matches = [str(p) for p in path.glob(pattern)]

    
    logger.info("find_files found %d matches (showing up to 10): %s", len(matches), matches[:10])

    return matches

