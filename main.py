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

    This function:
      - Displays a prompt message to the user.
      - If the user types 'q' or 'quit', or if a KeyboardInterrupt/EOFError is raised,
        it exits the program gracefully.
      - If the input is empty, the default value is returned.
      - If the input cannot be converted to an integer, it prints a message and returns the default.

    Parameters:
        prompt (str): The message displayed to the user.
        default (int): The default value if no valid input is provided.

    Returns:
        int: The user-supplied value or the default.
    """
    try:
        # Get user input from the console.
        user_input = input(prompt)
    except (KeyboardInterrupt, EOFError):
        # If the user interrupts (e.g., with Ctrl+C), exit gracefully.
        print("\nExiting as requested.")
        sys.exit(0)
    # Check if the user wants to quit.
    if user_input.strip().lower() in ("q", "quit"):
        print("Exiting as requested.")
        sys.exit(0)
    # Return the default value if no input is provided.
    if user_input.strip() == "":
        return default
    try:
        # Try converting the input to an integer.
        return int(user_input)
    except ValueError:
        # If conversion fails, print a message and return the default value.
        print("Invalid input. Using default value.")
        return default


def main():
    """
    Main function to prompt the user for parameters and run the sorting benchmarks.

    This function:
      - Prompts the user for the number of iterations.
      - Prompts the user for the threshold (in seconds).
      - Calls run_sorting_tests() with the user-specified or default parameters.
    """
    iterations = get_user_input(
        "Enter number of iterations (default 250, or 'q' to quit): ", 250
    )
    threshold = get_user_input(
        "Enter threshold in seconds (default 300, or 'q' to quit): ", 300
    )
    run_sorting_tests(iterations=iterations, threshold=threshold)


if __name__ == "__main__":
    # When the script is run directly, call the main function.
    main()
