import sys
import os
from benchmark import run_sorting_tests


def get_user_input(prompt, default):
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
    try:
        user_input = input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting as requested.")
        sys.exit(0)
    if user_input.strip() == "":
        return default.lower() == "y"
    return user_input.strip().lower() in ("y", "yes")


def main():
    ITERATIONS_DEFAULT = 500
    THRESHOLD_DEFAULT = 300
    TIMEOUT_DEFAULT = 60

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

    # === New third prompt for per-run timeout ===
    enable_timeout = get_yes_no_input("Enable per-run timeout? (y/n, default n): ", "n")
    if enable_timeout:
        per_run_timeout = get_user_input(
            f"Enter per-run timeout in seconds (default {TIMEOUT_DEFAULT}, or 'q' to quit): ",
            TIMEOUT_DEFAULT,
        )
    else:
        per_run_timeout = None

    # Pass the per_run_timeout value to the benchmark
    run_sorting_tests(
        iterations=iterations, threshold=threshold, per_run_timeout=per_run_timeout
    )


if __name__ == "__main__":
    main()
