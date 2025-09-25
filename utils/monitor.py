"""
Monitoring utilities for controlling agent output verbosity.
"""

import json
import pprint
from enum import Enum
from typing import List
from utils.logger import logger, ch, pretty_print
import logging

class LoggerLevel(Enum):
    ERROR = "error" # shows up, only when some errors appear
    INFO = "info"
    DEBUG = "debug" # the most detailed one


class OutputMode(Enum):
    DEFAULT = "default"    # Only last agent message
    GENERAL = "general"    # LangChain message.pretty_print()
    DETAILED = "detailed"  # Custom pretty_print for full agent results

def set_logger_level(level: LoggerLevel):
    """Configure console handler logging verbosity."""

    logging.getLogger("httpx").setLevel(logging.WARNING)

    if level == LoggerLevel.ERROR:
        ch.setLevel(logging.ERROR)
    elif level == LoggerLevel.INFO:
        ch.setLevel(logging.INFO)
    elif level == LoggerLevel.DEBUG:
        ch.setLevel(logging.DEBUG)
    
    logger.info(f"Logger display set to {logging.getLevelName(ch.level)}")



def output_results(result, mode: OutputMode):
    """
    Display monitoring output based on selected modes.

    Args:
        result: The agent invoke() result dict.
        modes: List of MonitorMode values to activate.
    """
    # Always show final user-facing output

    if mode == OutputMode.GENERAL:
        for msg in result["messages"]:
            msg.pretty_print()

    elif mode == OutputMode.DETAILED:
        print("=== Full result JSON ===")
        # Leave older pretty-print variants as reminders
        # print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        # pp = pprint.PrettyPrinter(indent=2, width=120, compact=False)
        # pp.pprint(result)
        pretty_print(result)

    # DEFAULT, GENERAL, DETAILED all show final message
    print("\n=== Final Output ===")
    print(result["messages"][-1].content)
    print("\n=== End ===")