"""
main.py

Entry point for the Sorting Algorithms Benchmark application.
This script:
  - Prompts the user for benchmark parameters.
  - Checks for command-line flags ("slow", "fast", "verbose", "v", "debug").
  - Initiates the benchmark run via run_sorting_tests().
"""

import sys
import os
from benchmark import run_sorting_tests, config


def get_user_input(prompt, default):
    """
    Prompt the user for an integer input, returning the default if none is provided.

    Parameters:
      prompt (str): The prompt message.
      default (int): The default value if the user provides no input.

    Returns:
      int: The user-supplied integer or the default.
    """
    try:
        user_input = input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting as requested.")
        sys.exit(0)
    if user_input.strip().lower() in ("q", "quit"):
        print("Exiting as requested.")
        sys.exit(0)
    if user_input.strip() == "":
        return default
    try:
        return int(user_input)
    except ValueError:
        print("Invalid input. Using default value.")
        return default


def get_yes_no_input(prompt, default="n"):
    """
    Prompt the user for a yes/no answer.

    Parameters:
      prompt (str): The prompt message.
      default (str): Default answer ("y" for yes, "n" for no).

    Returns:
      bool: True if the answer is affirmative, False otherwise.
    """
    try:
        user_input = input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting as requested.")
        sys.exit(0)
    if user_input.strip() == "":
        return default.lower() == "y"
    return user_input.strip().lower() in ("y", "yes")


def main():
    """
    Main function to set up parameters and start the benchmark tests.
    """
    config.debug("Starting main() function.")
    # Use default parameters from config.
    iterations_default = config.DEFAULT_ITERATIONS
    threshold_default = config.DEFAULT_THRESHOLD

    # Check for "slow" mode.
    if any(arg.lower() == "slow" for arg in sys.argv):
        os.environ["SLOW_MODE"] = "true"
        print("Slow mode enabled: Using half the workers.")
        config.debug("Slow mode enabled via command line.")
    else:
        os.environ["SLOW_MODE"] = "false"

    # Check for "fast" mode.
    if any(arg.lower() == "fast" for arg in sys.argv):
        os.environ["FAST_MODE"] = "true"
        os.environ["SLOW_MODE"] = "false"
        print("Fast mode enabled: Using all available cores minus 2.")
        config.debug("Fast mode enabled via command line.")
    else:
        os.environ["FAST_MODE"] = "false"

    # Enable verbose debugging if requested.
    if any(arg.lower() in ("verbose", "v", "debug") for arg in sys.argv):
        config.VERBOSE = True
        print("Verbose mode enabled: Extra debugging output will be printed.")
        config.debug("Verbose mode activated.")

    iterations = get_user_input(
        f"Enter number of iterations (default {iterations_default}, or 'q' to quit): ",
        iterations_default,
    )
    threshold = get_user_input(
        f"Enter time threshold in seconds (default {threshold_default}, or 'q' to quit): ",
        threshold_default,
    )
    enable_timeout = get_yes_no_input(
        "Enable per-run timeouts (cancel iteration if it exceeds the threshold)? (y/n, default n): ",
        "n",
    )
    config.debug(
        f"User inputs: iterations={iterations}, threshold={threshold}, timeout={enable_timeout}"
    )
    run_sorting_tests(
        iterations=iterations, threshold=threshold, per_run_timeout=enable_timeout
    )
    config.debug("Finished run_sorting_tests call. Exiting main().")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting due to keyboard interrupt.")
        sys.exit(0)
