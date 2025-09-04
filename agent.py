from utils.llm_loader import load_llm
from tools.summarize import summarize_tool
from tools.generate_canvas import generate_canvas_tool
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

# Wrap tools
@tool("summarize", description="Summarize notes from a file")
def summarize(file_path: str) -> str:
    return summarize_tool(file_path)

@tool("generate_canvas", description="Generate a JSON canvas from notes")
def generate_canvas(file_path: str, output_path: str = "10.Canvas/output.canvas") -> str:
    return generate_canvas_tool(file_path, output_path)

# Load model
llm = load_llm()

# Create agent
agent = create_react_agent(
    llm,
    tools=[summarize, generate_canvas],
    prompt="You are a canvas assistant"
)