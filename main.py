import argparse
from agent import get_agent
from utils.monitor import set_logger_level, output_results, LoggerLevel, OutputMode
from utils.logger import logger




def parse_args():
    parser = argparse.ArgumentParser(description="Run the agent with monitoring options.")
    
    parser.add_argument(
        "-l", "--log",
        type=str,
        default="info",
        choices=["error", "info", "debug"],
        help=(
            "Set logger verbosity level (default: info).\n"
            "  error = Only log errors\n"
            "  info  = General run info + important messages\n"
            "  debug = Most detailed logging (good for debugging)"
        ),
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="default",
        choices=["default", "general", "detailed"],
        help=(
            "Set result output mode (default: general).\n"
            "  default = Only final agent message\n"
            "  general = LangChain-style message.pretty_print()\n"
            "  detailed = Full agent result (custom pretty print + final message)"
        ),
    )
    return parser.parse_args()



def run():

    args = parse_args()

    # Map CLI strings → enums
    log_level_map = {
        "error": LoggerLevel.ERROR,
        "info": LoggerLevel.INFO,
        "debug": LoggerLevel.DEBUG,
    }
    output_mode_map = {
        "default": OutputMode.DEFAULT,
        "general": OutputMode.GENERAL,
        "detailed": OutputMode.DETAILED,
    }

    log_level = log_level_map[args.log]
    output_mode = output_mode_map[args.output]


    set_logger_level(log_level)
    logger.info("Agent started.")
    agent = get_agent()


    # Ask the agent to summarize a file
    inputs = {"messages": [("user", "Summarize Gemini4JSONCanvas.MD")]}
    result = agent.invoke(inputs)
    output_results(result, output_mode)

    # Ask the agent to generate a canvas
    inputs = {"messages": [("user", "Generate canvas from Gemini4JSONCanvas.MD")]}
    result = agent.invoke(inputs)
    output_results(result, output_mode)



if __name__ == "__main__":
    run()