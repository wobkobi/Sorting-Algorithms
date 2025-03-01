import sys
import os
from benchmark import run_sorting_tests


def get_user_input(prompt, default):
    """
    Prompt the user for an integer input.

    If the user enters nothing, the default value is returned.
    If the user types 'q' or 'quit', the program exits.

    Parameters:
        prompt (str): The message displayed to the user.
        default (int): The default value if no input is provided.

    Returns:
        int: The user-supplied integer or the default value.
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

    Returns True if the response is affirmative ('y' or 'yes') and False otherwise.
    If no input is provided, the default answer is used.

    Parameters:
        prompt (str): The message displayed to the user.
        default (str): The default answer ("y" for yes, "n" for no).

    Returns:
        bool: True if the answer is yes, False otherwise.
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
    Entry point for the sorting benchmark.

    Prompts the user for:
      - Number of iterations (default: 500)
      - Time threshold in seconds (default: 300)
      - Whether to enable a per-run timeout (yes/no)
      - If timeout is enabled, the per-run timeout in seconds (default: 60)

    Also checks for the "slow" argument to enable SLOW_MODE.
    Then runs the benchmark with the specified parameters.
    """
    ITERATIONS_DEFAULT = 500
    THRESHOLD_DEFAULT = 300
    TIMEOUT_DEFAULT = 60

    # Check for "slow" argument to enable slow mode.
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
        f"Enter threshold in seconds (default {THRESHOLD_DEFAULT}, or 'q' to quit): ",
        THRESHOLD_DEFAULT,
    )

    # Prompt for per-run timeout.
    enable_timeout = get_yes_no_input("Enable per-run timeout? (y/n, default n): ", "n")
    if enable_timeout:
        per_run_timeout = get_user_input(
            f"Enter per-run timeout in seconds (default {TIMEOUT_DEFAULT}, or 'q' to quit): ",
            TIMEOUT_DEFAULT,
        )
    else:
        per_run_timeout = None

    run_sorting_tests(
        iterations=iterations, threshold=threshold, per_run_timeout=per_run_timeout
    )


if __name__ == "__main__":
    main()
