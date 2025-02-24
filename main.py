"""
main.py

Entry point for the Sorting Algorithms Benchmark.

This script prompts the user for the number of iterations and threshold parameters.
Users may exit at any prompt by typing "q" or "quit" or by pressing Ctrl+C.
If no input is provided, the default values (250 iterations and 300 seconds threshold) are used.
The specified parameters are then passed to the benchmark process.
"""

import sys
from benchmark import run_sorting_tests


def get_user_input(prompt, default):
    """
    Prompt the user for an integer input.

    - If the user types 'q' or 'quit', or triggers a KeyboardInterrupt/EOFError,
      the program exits gracefully.
    - If the input is empty or invalid, the default value is used.

    Parameters:
        prompt (str): The message displayed to the user.
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


if __name__ == "__main__":
    iterations = get_user_input(
        "Enter number of iterations (default 250, or 'q' to quit): ", 250
    )
    threshold = get_user_input(
        "Enter threshold in seconds (default 300, or 'q' to quit): ", 300
    )
    run_sorting_tests(iterations=iterations, threshold=threshold)
