"""
Entry point for the Sorting Algorithms Benchmark.

This script prompts the user for the number of iterations and threshold parameters.
Users can exit at any prompt by typing "q" or "quit" or by pressing Ctrl+C.
If no input is provided, the default values (250 iterations and 300 seconds threshold) are used.
If the word "slow" is provided as a command-line argument (e.g., "python main.py slow"),
the benchmark will run using half the number of workers (as determined by get_num_workers()).
The specified parameters are then passed to the benchmark process.
"""

import sys
import os
from benchmark import run_sorting_tests


def get_user_input(prompt, default):
    """
    Prompt the user for an integer input.

    This function displays a prompt message and reads user input from the console.
    It gracefully handles exit conditions:
    - If the user types 'q' or 'quit', the program exits.
    - If a KeyboardInterrupt or EOFError occurs, the program exits.
    If the input is empty or invalid (i.e., cannot be converted to an integer),
    the default value is returned.

    Parameters:
        prompt (str): The message to display to the user.
        default (int): The default value to return if input is empty or invalid.

    Returns:
        int: The user-supplied value or the default.
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


def main():
    """
    Main function to run the benchmark.

    The function performs the following steps:
    1. Checks for a command-line argument "slow". If present, sets the SLOW_MODE environment variable,
       which causes the benchmark process to use half the normal number of workers.
    2. Prompts the user for the number of iterations and the threshold (in seconds).
    3. Calls run_sorting_tests() with the chosen parameters.
    """
    # Check for the "slow" command-line argument.

    ITERATIONS_DEFAULT = 500
    THRESHOLD_DEFAULT = 300

    if len(sys.argv) > 1 and sys.argv[1].lower() == "slow":
        os.environ["SLOW_MODE"] = "true"
        print("Slow mode enabled: Using half the workers.")
    else:
        os.environ["SLOW_MODE"] = "false"

    # Prompt the user for benchmark parameters.
    iterations = get_user_input(
        f"Enter number of iterations (default {ITERATIONS_DEFAULT}, or 'q' to quit): ",
        ITERATIONS_DEFAULT,
    )
    threshold = get_user_input(
        f"Enter threshold in seconds (default {THRESHOLD_DEFAULT}, or 'q' to quit): ",
        THRESHOLD_DEFAULT,
    )

    # Run the sorting benchmark using the specified parameters.
    run_sorting_tests(iterations=iterations, threshold=threshold)


if __name__ == "__main__":
    main()
