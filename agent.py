from utils.llm_loader import load_llm
from utils.files_interactions import validate_file_path
from tools.summarize import summarize_tool
from tools.generate_canvas import generate_canvas_tool
from tools.file_search import find_files
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from typing import List


# Wrap tools
@tool("summarize", description="Summarize notes from a file")
def summarize(file_path: str) -> str:
    """Summarize the content of a file using LLM and prompt template.

    Args:
        file_path: Path to the file to summarize.

    Returns:
        str: Summary of the file content.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read due to permission issues.
    """
    try:
        validated_path = validate_file_path(file_path)
        return summarize_tool(validated_path)
    except (FileNotFoundError, PermissionError) as e:
        return f"Error: {str(e)}"

@tool("generate_canvas", description="Generate a JSON canvas from notes")
def generate_canvas(file_path: str, output_path: str = "10.Canvas/output.canvas") -> str:
    """Generate canvas JSON from notes using LLM and save to disk.

    Args:
        file_path: Path to the file to generate canvas from.
        output_path: Path to save the generated canvas JSON.

    Returns:
        str: Path to the saved canvas JSON.

    Raises:
        FileNotFoundError: If the file or prompt file does not exist.
        ValueError: If the LLM does not return valid JSON.
        PermissionError: If the file cannot be read or written due to permission issues.
    """
    try:
        validated_path = validate_file_path(file_path)
        return generate_canvas_tool(validated_path, output_path)
    except (FileNotFoundError, ValueError, PermissionError) as e:
        return f"Error: {str(e)}"
    

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






def get_agent():
    llm = load_llm()
    agent = create_react_agent(
        llm,
        tools=[summarize, generate_canvas, search_files],
        prompt="You are a canvas assistant"
    )
    return agent
