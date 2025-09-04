from agent import get_agent

def run():
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