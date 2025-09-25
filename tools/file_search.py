"""File search utilities for the canvas agent."""


from pathlib import Path
from typing import List, Optional
from utils.logger import logger

def find_files(
    query: str,
    directory: str = ".",
    recursive: bool = True
) -> List[str]:
    """Find files or folders by query (name fragment or glob pattern).

    Args:
        query: A filename, partial name, or glob pattern (e.g., "Gemini4*", "*.md").
        directory: Directory to search in.
        recursive: Whether to search subdirectories.

    Returns:
        List of matching file paths
    """
    logger.info(f"Starting files checking for query{query}")
    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    # Allow glob-style queries (with * or ?)
    if any(ch in query for ch in ["*", "?"]):
        matches = list(path.rglob(query) if recursive else path.glob(query))
    else:
        # Treat query as "contains substring"
        matches = [
            p for p in (path.rglob("*") if recursive else path.glob("*"))
            if query.lower() in p.name.lower()
        ]

    matches = [str(p) for p in matches]
    logger.debug("find_files found %d matches for '%s' (showing up to 10): %s", len(matches), query, matches[:10])
    
    return matches
    

