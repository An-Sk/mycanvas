from pathlib import Path
from utils.file_io import read_file
from utils.llm_loader import load_llm
from langchain.prompts import PromptTemplate

def summarize_tool(file_path: str) -> str:
    """Summarize the content of a file using LLM and prompt template."""

    # Load input file
    file_content = read_file(file_path)

    # Load prompt template from prompts/summary_prompt.txt
    prompt_text = Path("prompts/summary_prompt.txt").read_text(encoding="utf-8")
    prompt = PromptTemplate.from_template(prompt_text)

    # Load model
    llm = load_llm()

    # Run chain
    chain = prompt | llm
    result = chain.invoke({"args": file_content})

    return result.content