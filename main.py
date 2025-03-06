"""
main.py

Entry point for the Sorting Algorithms Benchmark application.

This script:
  - Prompts the user for benchmark parameters.
  - Checks for command-line flags ("slow", "verbose", "debug").
  - Initiates the benchmark run via run_sorting_tests().

Usage:
  Run the script with optional arguments:
    - "slow" to enable slow mode (fewer workers).
    - "verbose", "v", or "debug" for extra debugging output.
"""

import sys
import os
from benchmark import run_sorting_tests
import benchmark as config


def get_user_input(prompt, default):
    """
    Prompt the user for an integer input, using a default value if none is provided.

    Special behavior:
      - If the user inputs 'q' or 'quit', the program exits.
      - If the input cannot be converted to an integer, the default is used.

    Parameters:
      prompt (str): Message displayed to the user.
      default (int): Default value to use if no input is provided.

    Returns:
      int: The user-provided integer or the default value.
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

    Returns True for "y" or "yes" (case-insensitive); otherwise, returns False.
    If no input is provided, the default is used.

    Parameters:
      prompt (str): The question to ask the user.
      default (str): Default answer ("y" for yes, "n" for no).

    Returns:
      bool: True for affirmative, False otherwise.
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
    Main function to start the benchmark process.

    It sets up benchmark parameters (iterations, time threshold, per-run timeout),
    checks for optional command-line flags, and then calls run_sorting_tests().
    """
    # Use default parameters from config.py.
    iterations_default = config.DEFAULT_ITERATIONS
    threshold_default = config.DEFAULT_THRESHOLD

    # Check for "slow" mode to adjust the worker count.
    if len(sys.argv) > 1 and sys.argv[1].lower() == "slow":
        os.environ["SLOW_MODE"] = "true"
        print("Slow mode enabled: Using half the workers.")
    else:
        os.environ["SLOW_MODE"] = "false"

    # Enable verbose debugging if requested.
    if any(arg.lower() in ("verbose", "v", "debug") for arg in sys.argv):
        config.VERBOSE = True
        print("Verbose mode enabled: Extra debugging output will be printed.")

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

    run_sorting_tests(
        iterations=iterations, threshold=threshold, per_run_timeout=enable_timeout
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting due to keyboard interrupt.")
        sys.exit(0)
