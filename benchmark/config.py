"""
config.py

Global configuration for the Sorting Algorithms Benchmark application.
This module defines global flags, default parameters, and a debug function that logs
messages in a Minecraft–like style to both the console and a file.
Additionally, it defines global variables to track overall runtime and per–array size durations.
"""

import datetime

# Global flags.
VERBOSE = False  # Set to True for extra debugging output.
SLOW_MODE = False  # Set to True to reduce worker count in slow mode.
FAST_MODE = False  # Set to True to use all available cores minus 2.

# Default benchmark parameters.
DEFAULT_ITERATIONS = 500
DEFAULT_THRESHOLD = 300

# File where debug logs will be written.
DEBUG_LOG_FILE = "debug.log"

# Global runtime tracking.
RUN_START_TIME = None  # Will be set when the run begins.
ARRAY_TIME_LOG = []  # List of tuples: (array_size, elapsed_seconds)

# Global tracking for the currently processing array.
CURRENT_ARRAY = None  # The array size currently being processed.
CURRENT_ARRAY_START = None  # Datetime when the current array processing started.

_last_debug_message = None  # Used to suppress duplicate consecutive messages.


def debug(msg):
    """
    Print a debug message if verbose mode is enabled.
    The message is printed in a Minecraft–like log style with a timestamp,
    and is appended to a debug log file. Duplicate consecutive messages are suppressed.

    Parameters:
      msg (str): The debug message to print.
    """
    global _last_debug_message
    if VERBOSE:
        if msg == _last_debug_message:
            return  # Skip duplicate message.
        _last_debug_message = msg
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] [main/DEBUG] {msg}"
        print(log_line)
        with open(DEBUG_LOG_FILE, "a") as f:
            f.write(log_line + "\n")
