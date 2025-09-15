from pathlib import Path
from utils.file_io import read_file
from utils.llm_loader import load_llm
from langchain.prompts import PromptTemplate
from utils.logger import logger


def summarize_tool(file_path: str) -> str:
    """Summarize the content of a file using LLM and prompt template."""
    try:
        logger.info(f"Starting summarization for file: {file_path}")

        # Get the base directory of the project
        base_dir = Path(__file__).parent.parent

        # Load input file
        logger.info("Loading input file")
        file_content = read_file(file_path)

        # Load prompt template from prompts/summary_prompt.txt
        logger.info("Loading prompt template")
        prompt_path = base_dir / "prompts" / "summary_prompt.txt"
        prompt_text = prompt_path.read_text(encoding="utf-8")
        prompt = PromptTemplate.from_template(prompt_text)

        # Load model
        logger.info("Loading LLM model")
        llm = load_llm()

        # Run chain
        logger.info("Running summarization chain")
        chain = prompt | llm
        result = chain.invoke({"args": file_content})

        logger.info("Summarization completed successfully")
        return result.content

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        raise