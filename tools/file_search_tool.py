"""File search tool for the canvas agent."""

from typing import List
from langchain.tools import tool
from utils.file_search import find_files

@tool("search_files", description="Search for files in the project directory")
def search_files(
    directory: str = ".",
    pattern: str = "*.md",
    recursive: bool = True
) -> List[str]:
    """Search for files matching pattern in directory.

    Args:
        directory: Directory to search in (default: current directory)
        pattern: File pattern to match (default: "*.md")
        recursive: Whether to search recursively (default: True)

    Returns:
        List of matching file paths
    """
    try:
        return find_files(directory, pattern, recursive)
    except FileNotFoundError as e:
        return [f"Error: {str(e)}"]