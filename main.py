from agent import get_agent

import logging
from utils.logger import logger



def run():

    # Reduce httpx logging level
    logging.getLogger("httpx").setLevel(logging.WARNING)
    # Set log level dynamically here
    logger.setLevel(logging.INFO)   # show INFO and above
    # logger.setLevel(logging.DEBUG)  # show DEBUG too
    # logger.setLevel(logging.ERROR)  # only show errors

    logger.info("tool starting.")
    agent = get_agent()
    # Ask the agent to summarize a file
    inputs = {"messages": [("user", "Summarize Gemini4JSONCanvas.MD")]}
    result = agent.invoke(inputs)
    print("\n=== Summary Output ===")
    print(result["messages"][-1].content)

    # Ask the agent to generate a canvas
    inputs = {"messages": [("user", "Generate canvas from Gemini4JSONCanvas.MD")]}
    result = agent.invoke(inputs)
    print("\n=== Canvas Output ===")
    print(result["messages"][-1].content)

if __name__ == "__main__":
    run()