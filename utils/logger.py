import logging
from langchain_core.callbacks.base import BaseCallbackHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)  # global level

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
ch.setFormatter(formatter)

# Attach handler
if not logger.handlers:  # prevent duplicate logs
    logger.addHandler(ch)


class MyLoggerCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        try:
            logger.debug("LLM start. Prompts (truncated):\n%s", [p[:1000] for p in prompts])
        except Exception:
            logger.exception("Error logging on_llm_start")

    def on_llm_end(self, response, **kwargs):
        try:
            # response.generations may be present depending on version
            logger.debug("LLM end. Response (truncated):\n%s", getattr(response, "generations", str(response))[:2000])
        except Exception:
            logger.exception("Error logging on_llm_end")


    def on_tool_start(self, serialized, input_str, **kwargs):
        # serialized may be dict with 'name'
        name = serialized.get("name") if isinstance(serialized, dict) else str(serialized)
        logger.info("Tool START: %s  input (truncated): %s", name, str(input_str)[:1000])

    def on_tool_end(self, output, **kwargs):
        logger.info("Tool END. Output (truncated): %s", str(output)[:1000])

    def on_tool_error(self, error, **kwargs):
        logger.error("Tool ERROR: %s", error)

    def on_llm_error(self, error, **kwargs):
        logger.error(f"LLM error -> {error}")

