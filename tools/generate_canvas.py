import logging
from pathlib import Path
from utils.file_io import read_file, save_json
from utils.llm_loader import load_llm
from langchain.prompts import PromptTemplate
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_canvas_tool(file_path: str, output_path: str) -> str:
    """Generate canvas JSON from notes using LLM and save to disk."""
    try:
        logger.info(f"Starting canvas generation for file: {file_path}")

        # Load input file
        logger.info("Loading input file")
        file_content = read_file(file_path)

        # Load prompt template
        logger.info("Loading prompt template")
        prompt_text = Path("prompts/generate_prompt.txt").read_text(encoding="utf-8")
        prompt = PromptTemplate.from_template(prompt_text)

        # Load model
        logger.info("Loading LLM model")
        llm = load_llm()

        # Run chain
        logger.info("Running canvas generation chain")
        chain = prompt | llm
        result = chain.invoke({"args": file_content})

        # Parse JSON
        logger.info("Parsing JSON response")
        try:
            canvas_json = json.loads(result.content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise ValueError("LLM did not return valid JSON")

        # Save JSON
        logger.info(f"Saving canvas JSON to: {output_path}")
        save_json(canvas_json, output_path)

        logger.info("Canvas generation completed successfully")
        return output_path

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during canvas generation: {e}")
        raise