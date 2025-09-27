import logging
from langchain_core.callbacks.base import BaseCallbackHandler
import io
import sys
from contextlib import redirect_stdout

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)  # global level

# Console handler
ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)

# Format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
ch.setFormatter(formatter)

# Attach handler
if not logger.handlers:  # prevent duplicate logs
    logger.addHandler(ch)


class MyLoggerCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        try:
            pp = capture_pretty_print([p[:1000] for p in prompts])
            logger.debug("LLM start. Prompts (truncated):\n%s", pp)
        except Exception:
            logger.exception("Error logging on_llm_start")

    def on_llm_end(self, response, **kwargs):
        try:
            # response.generations may be present depending on version
            pp = capture_pretty_print(getattr(response, "generations", str(response))[:2000])
            logger.debug("LLM end. Response (truncated):\n%s", pp)
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



from rich.tree import Tree
from rich.console import Console
from rich.text import Text

def add_to_tree(tree: Tree, obj, key: str = None):
    """Recursively add objects (dict, list, dataclass-like, primitives) to the tree."""
    label = f"[bold]{key}[/]" if key else ""

    if isinstance(obj, dict):
        node = tree.add(f"{label} {{dict}}")
        for k, v in obj.items():
            add_to_tree(node, v, str(k))

    elif isinstance(obj, list):
        node = tree.add(f"{label} [list] ({len(obj)})")
        for i, v in enumerate(obj):
            add_to_tree(node, v, f"[{i}]")

    elif hasattr(obj, "__dict__"):  # generic object
        node = tree.add(f"{label} ({obj.__class__.__name__})")
        for k, v in vars(obj).items():
            add_to_tree(node, v, k)

    else:  # primitive
        display = repr(obj)
        if len(display) > 200:  # truncate long content
            display = display[:1000] + "..."
        tree.add(f"{label}: {display}")


def pretty_print(obj, title="Result"):
    """Pretty print any Python object as a tree."""
    console = Console()
    tree = Tree(Text(title, style="bold cyan"))
    add_to_tree(tree, obj)
    console.print(tree)


def capture_pretty_print(obj):
    buf = io.StringIO()
    with redirect_stdout(buf):
        pretty_print(obj)
    return buf.getvalue().strip()