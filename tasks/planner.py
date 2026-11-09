# Purpose: generate a dynamic plan when no predefined task exists.
# Uses the LLM to turn the user’s free-form request into a list of sequential step descriptions.
# Each step is again in plain English, like:
# “Step 1: Search for files matching query.”
# “Step 2: Summarize the first file found.”
# Provides:
# plan_task(request) → returns this human-readable plan (a list of step descriptions).
# execute_plan(plan) → executes the plan and returns the results.
# Connects to:
# utils.llm_instance to call the LLM.
# tasks.handler to provide a plan back.

from utils.llm_loader import llm_instance

PLAN_PROMPT = """
You are a task planner.
Break the request into clear steps using available tools: search_files, summarize, generate_canvas.
Output in JSON with:
- id (step number)
- tool
- args
- description (human readable)

Example:
[
  {"id": 1, "tool": "search_files", "args": {"query": "Gemini4*"}, "description": "Find matching notes"},
  {"id": 2, "tool": "summarize", "args": {"file_paths": ["Gemini4JSONCanvas.MD"]}, "description": "Summarize the note"}
]
"""

def plan_task(request):
    # Format the prompt with the user’s request
    prompt = PLAN_PROMPT + f"\n\nUser request: {request}"
    # Call the LLM to generate a plan
    plan = llm_instance.invoke(prompt)
    # Parse the result into a list of steps
    steps = plan.split('\n')
    # Return the human-readable plan
    return steps

def execute_plan(plan, resume_from=1, max_retries=2):
    results = {}
    for step in plan:
        if step["id"] < resume_from:
            continue

        tool = step["tool"]
        args = step["args"]
        desc = step["description"]

        print(f"Step {step['id']}: {desc}")
        for attempt in range(max_retries):
            try:
                # Dynamically call the tool
                from agent import summarize, generate_canvas, search_files
                tools = {"summarize": summarize, "generate_canvas": generate_canvas, "search_files": search_files}
                results[step["id"]] = tools[tool].run(args)
                break
            except Exception as e:
                print(f"  Error on attempt {attempt+1}: {e}")
        else:
            print(f"  Failed step {step['id']} after {max_retries} retries")
            break
    return results