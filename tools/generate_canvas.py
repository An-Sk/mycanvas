from pathlib import Path
from utils.file_io import read_file, save_json
from utils.llm_loader import load_llm
from langchain.prompts import PromptTemplate
import json

def generate_canvas_tool(file_path: str, output_path: str) -> str:
    """Generate canvas JSON from notes using LLM and save to disk."""

    # Load input file
    file_content = read_file(file_path)

    # Load prompt template
    prompt_text = Path("prompts/generate_prompt.txt").read_text(encoding="utf-8")
    prompt = PromptTemplate.from_template(prompt_text)

    # Load model
    llm = load_llm()

    # Run chain
    chain = prompt | llm
    result = chain.invoke({"args": file_content})

    # Parse JSON
    try:
        canvas_json = json.loads(result.content)
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON")

    # Save JSON
    save_json(canvas_json, output_path)

    return output_path