"""
main.py

Entry point for the Sorting Algorithms Benchmark application.
It interacts with the user to obtain:
  - Number of iterations.
  - Time threshold for each iteration.
  - Whether to enable per-run timeouts.

It also checks for an optional "slow" command-line argument to adjust worker settings.
Finally, it initiates the benchmark run.
"""

import sys
import os
from benchmark import run_sorting_tests


def get_user_input(prompt, default):
    """
    Prompt the user for integer input with a default option.

    If the user enters 'q' or 'quit', the program exits.
    If no input is provided, returns the default.

    Parameters:
        prompt (str): Message shown to the user.
        default (int): Default value if input is empty.

    Returns:
        int: The user's input as an integer, or the default value.
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

    Returns True for affirmative responses ('y' or 'yes'), False otherwise.
    If no input is provided, uses the provided default.

    Parameters:
        prompt (str): Question to ask the user.
        default (str): Default answer ("y" for yes, "n" for no).

    Returns:
        bool: True if affirmative, False otherwise.
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
    Main function to start the benchmark.

    Prompts the user for configuration parameters, checks for the "slow" mode,
    and then starts the benchmark using run_sorting_tests().
    """
    ITERATIONS_DEFAULT = 500
    THRESHOLD_DEFAULT = 300

    # Check for "slow" command-line argument to enable slow mode.
    if len(sys.argv) > 1 and sys.argv[1].lower() == "slow":
        os.environ["SLOW_MODE"] = "true"
        print("Slow mode enabled: Using half the workers.")
    else:
        os.environ["SLOW_MODE"] = "false"

    iterations = get_user_input(
        f"Enter number of iterations (default {ITERATIONS_DEFAULT}, or 'q' to quit): ",
        ITERATIONS_DEFAULT,
    )
    threshold = get_user_input(
        f"Enter time threshold in seconds (default {THRESHOLD_DEFAULT}, or 'q' to quit): ",
        THRESHOLD_DEFAULT,
    )

    # Ask if per-run timeouts should be enabled (each iteration canceled if exceeding threshold).
    enable_timeout = get_yes_no_input(
        "Enable per-run timeouts (each iteration will be canceled if it exceeds the threshold)? (y/n, default n): ",
        "n",
    )

    run_sorting_tests(
        iterations=iterations, threshold=threshold, per_run_timeout=enable_timeout
    )


if __name__ == "__main__":
    main()
