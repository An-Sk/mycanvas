# Purpose: the dispatcher.
# Decides whether to use the registry or the planner:
# First, check if the task name exists in the registry.
# If yes → return that plan.
# If no → generate one via planner.
# Passes the plan to the agent.
# Provides:
# run_task(request) → returns results after the agent executes the steps.
# Connects to:
# tasks.registry
# tasks.planner
# agent (to execute the steps).

from tasks.registry import get_task_plan
from tasks.planner import plan_task, execute_plan

def run_task(request):
    """Run a task by either using a predefined plan from the registry or generating a new plan.

    Args:
        request: The task request, either a predefined task name or a free-form description.

    Returns:
        The result of the task execution.

    Raises:
        ValueError: If the task could not be planned.
    """
    try:
        # First try to get a predefined plan from the registry
        task_plan = get_task_plan(request)

        if task_plan:
            # Normalize the plan format
            if isinstance(task_plan, dict) and "description" in task_plan and "steps" in task_plan:
                return execute_plan(task_plan)
            else:
                # If the plan is not in the expected format, treat it as raw text and plan again
                task_plan = plan_task(request)
                return execute_plan({"description": "Generated plan", "steps": task_plan.split('\n')})

        # If no predefined plan exists, generate a new one
        raw_plan = plan_task(request)
        return execute_plan({"description": "Generated plan", "steps": raw_plan.split('\n')})

    except Exception as e:
        # Return a standardized error message
        return {"description": "Task could not be planned", "steps": [], "error": str(e)}