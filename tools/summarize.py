import logging
from pathlib import Path
from utils.file_io import read_file
from utils.llm_loader import load_llm
from langchain.prompts import PromptTemplate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def summarize_tool(file_path: str) -> str:
    """Summarize the content of a file using LLM and prompt template."""
    try:
        logger.info(f"Starting summarization for file: {file_path}")

        # Load input file
        logger.info("Loading input file")
        file_content = read_file(file_path)

        # Load prompt template from prompts/summary_prompt.txt
        logger.info("Loading prompt template")
        prompt_text = Path("prompts/summary_prompt.txt").read_text(encoding="utf-8")
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