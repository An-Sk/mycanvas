from pathlib import Path
from utils.file_io import read_file, save_json, extract_json, ensure_folder
from utils.llm_instance import llm_instance
from utils.logger import logger
from langchain.prompts import PromptTemplate
import json
import toml

"""# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)"""

def generate_canvas_tool(file_paths: list[str], output_path: str, max_retries: int = 2) -> str:
    """Generate canvas JSON from notes using LLM and save to disk."""
    try:
        logger.info(f"Starting canvas generation for files(for now 1st only): {file_paths}")

        # Get the base directory of the project
        base_dir = Path(__file__).parent.parent

        # Load input file
        logger.info("Loading input file")
        file_path = file_paths[0]  # only first for now
        file_content = read_file(file_path)
        if ensure_folder(output_path):
            logger.info(f"Created missing folder for output: {Path(output_path).parent}")

        # Load prompt template
        logger.info("Loading prompt template")
        #prompt_path = base_dir / "prompts" / "generate_prompt.txt"
        #prompt_text = prompt_path.read_text(encoding="utf-8")
        config = toml.load(base_dir / "prompts" / "generate_prompt.toml")
        prompt = PromptTemplate.from_template(config["prompt"])

        # Load model
        logger.info("Loading LLM model")
        llm = llm_instance
        chain = prompt | llm

        last_error = None
        result = None

        for attempt in range(max_retries):
            try:
                logger.info(f"[Attempt {attempt+1}] Running canvas generation chain")
                result = chain.invoke({"args": file_content})
                #logger.debug("Raw LLM output:\n%s", result.content)

                logger.info("Parsing JSON response")
                
                canvas_json = extract_json(result.content)

                save_json(canvas_json, output_path)
                logger.info(f"Canvas generation completed successfully -> {output_path}")
                return output_path

            except json.JSONDecodeError as e:
                logger.error(f"[Attempt {attempt+1}] JSON decode error: {e}")
                #logger.debug("Sending prompt to LLM:\n%s", prompt.format(args=file_content)[:1000])
                #logger.error("JSON Raw LLM output:\n%s", result.content if result else "<no result>")
                last_error = e

            except Exception as e:
                logger.error(f"[Attempt {attempt+1}] Unexpected error: {e}")
                last_error = e

        raise ValueError(f"Canvas generation failed after {max_retries} attempts. Last error: {last_error}")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during canvas generation: {e}")
        raise

