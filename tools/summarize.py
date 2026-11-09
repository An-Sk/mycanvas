from pathlib import Path
from utils.file_io import read_file, save_md, ensure_folder
from utils.llm_loader import llm_instance
from langchain.prompts import PromptTemplate
from utils.logger import logger
import toml
import traceback


def summarize_tool(file_paths: list[str], output_path: str) -> str:
    """Summarize the content of a file using LLM and prompt template."""
    try:
        logger.info(f"Starting summarization for files(as of now only 1st one): {file_paths}")

        # Get the base directory of the project
        base_dir = Path(__file__).parent.parent
        

        # Load input file
        logger.info("Loading input file")
        file_path = file_paths[0]  # only first for now
        file_content = read_file(file_path)
        if ensure_folder(output_path):
            logger.info(f"Created missing folder for output: {Path(output_path).parent}")

        # Load prompt template from prompts/summary_prompt.txt
        logger.info("Loading prompt template")
        #prompt_path = base_dir / "prompts" / "summary_prompt.txt"
        #prompt_text = prompt_path.read_text(encoding="utf-8")
        config = toml.load(base_dir / "prompts" / "summary_prompt.toml")
        prompt = PromptTemplate.from_template(config["prompt"])

        # Load model
        logger.info("Loading LLM model")
        llm = llm_instance

        # Run chain
        logger.info("Running summarization chain")
        chain = prompt | llm
        result = chain.invoke({"args": file_content})
        #print(file_content)
        #return result.content
        summary = result.content
        save_md(summary, output_path)
        logger.info(f"Summary generation for {Path(file_path).name} completed successfully -> {output_path}")
        return output_path

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except Exception as e:
        full_error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        logger.error("Error during summarization:\n%s", full_error)
        raise