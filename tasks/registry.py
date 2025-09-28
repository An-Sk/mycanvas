# Purpose: a lookup table of known tasks.
# Each task is described with:
# A name (e.g. "summarize_file", "generate_canvas").
# A description.
# The ordered list of steps needed to accomplish it.
# Each step is just plain English text, not JSON, describing:
# What needs to be done.
# Which tool is likely needed.
# Why this step is important.
# Provides one function:
# get_task_plan(name) → fetches the task plan from the registry.
# Connects to:
# tasks.handler (the dispatcher).
# Does not directly import tools (it only describes steps).

# Global dictionary of predefined tasks
TASKS = {
    "summarize_file": {
        "description": "Summarize a single note file into concise text.",
        "steps": [
            "Search for the file. (tool: search_files)",
            "Read the file content. (tool: summarize)",
            "Return a concise summary. (why: user needs digestible content)"
        ]
    },
    "generate_canvas": {
        "description": "Generate a canvas from a given prompt.",
        "steps": [
            "Generate a canvas from the given prompt. (tool: generate_canvas)",
            "Return the generated canvas. (why: user needs a canvas)"
        ]
    }
}

def get_task_plan(name):
    # Fetch the task plan from the registry
    return TASKS.get(name)