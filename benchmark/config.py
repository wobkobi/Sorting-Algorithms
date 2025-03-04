# config.py

"""
Global configuration for the Sorting Algorithms Benchmark application.

This module defines:
  - Global flags (e.g. VERBOSE, SLOW_MODE).
  - Default benchmark parameters.
  - A debug function for printing verbose messages.
"""

# Global flags.
VERBOSE = False  # Set to True for extra debugging output.
SLOW_MODE = False  # Set to True to reduce worker count in slow mode.

# Default benchmark parameters.
DEFAULT_ITERATIONS = 500
DEFAULT_THRESHOLD = 300


def debug(msg):
    """
    Print a debug message if verbose mode is enabled.

    Parameters:
      msg (str): Debug message to print.
    """
    if VERBOSE:
        print("[DEBUG]", msg)
