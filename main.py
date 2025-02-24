"""
main.py

Entry point for the Sorting Algorithms Benchmark.

This script prompts the user for the number of iterations and threshold parameters.
Users may exit at any prompt by typing "q" or "quit" or by pressing Ctrl+C.
If no input is provided, the default values (250 iterations and 300 seconds threshold) are used.
If the word "slow" is provided as a command-line argument (e.g., "python main.py slow"),
the benchmark will run using half of the workers as determined by get_num_workers().
The specified parameters are then passed to the benchmark process.
"""

import sys
import os
from benchmark import run_sorting_tests


def get_user_input(prompt, default):
    """
    Prompt the user for an integer input.

    - Displays a prompt message.
    - If the user types 'q' or 'quit', or if a KeyboardInterrupt/EOFError occurs,
      exits the program gracefully.
    - If the input is empty or invalid, returns the default value.

    Parameters:
        prompt (str): The message to display.
        default (int): The default value if no valid input is provided.

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
    Main function:
      - Checks if the "slow" argument was provided.
      - Prompts the user for iterations and threshold.
      - Calls run_sorting_tests() with the chosen parameters.
    """
    # Check command-line arguments for "slow"
    if len(sys.argv) > 1 and sys.argv[1].lower() == "slow":
        # Set an environment variable that get_num_workers() will use to reduce worker count.
        os.environ["SLOW_MODE"] = "true"
        print("Slow mode enabled: Using half the workers.")
    else:
        os.environ["SLOW_MODE"] = "false"

    # Prompt for benchmark parameters.
    iterations = get_user_input(
        "Enter number of iterations (default 250, or 'q' to quit): ", 250
    )
    threshold = get_user_input(
        "Enter threshold in seconds (default 300, or 'q' to quit): ", 300
    )

    # Run the benchmark with the specified parameters.
    run_sorting_tests(iterations=iterations, threshold=threshold)


if __name__ == "__main__":
    main()
