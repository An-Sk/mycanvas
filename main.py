from agent import get_agent
import json
import pprint
import logging
from utils.logger import logger, pretty_print



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
    #print(f"Full result:\n{result}")
    print("=== Full result:===")
    #print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    #pp = pprint.PrettyPrinter(indent=2, width=120, compact=False)
    #print("=== Full result (pretty):===")
    #pp.pprint(result)
    pretty_print(result)
    print("\n=== Summary Output ===")
    print(result["messages"][-1].content)
    print("\n=== Summary Output Ended ===")

    # Ask the agent to generate a canvas
    inputs = {"messages": [("user", "Generate canvas from Gemini4JSONCanvas.MD")]}
    result = agent.invoke(inputs)
    #print(f"Full result:\n{result.pretty}")
    for message in result["messages"]:
        message.pretty_print()
    pretty_print(result)
    print("\n=== Canvas Output ===")
    print(result["messages"][-1].content)
    print("\n=== Canvas Output Ended===")

if __name__ == "__main__":
    run()