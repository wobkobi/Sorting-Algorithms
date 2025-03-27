"""
exit_handlers.py

Handles graceful shutdown of the benchmark application.
This module sets up signal handlers for SIGINT and SIGTERM and registers an atexit
handler to perform final logging. In addition to its existing functionality,
it now saves a runtime log in JSON format (including total elapsed time and per–array size breakdown)
before exiting.
"""

import atexit
import signal
import sys
import datetime
import json
from . import config
from .config import debug


def save_runtime_log_json():
    """
    Save a runtime log as JSON that includes the total run time and a breakdown of processing times
    for each array size. If an array is currently being processed, its elapsed time is computed
    up to exit. The log is saved to "runtime_log.json".
    """
    # If an array is in progress, record its elapsed time.
    if config.CURRENT_ARRAY is not None and config.CURRENT_ARRAY_START is not None:
        current_elapsed = (
            datetime.datetime.now() - config.CURRENT_ARRAY_START
        ).total_seconds()
        config.ARRAY_TIME_LOG.append((config.CURRENT_ARRAY, current_elapsed))
        debug(
            f"Recorded in-progress array {config.CURRENT_ARRAY} time: {current_elapsed:.2f} seconds."
        )
    if config.RUN_START_TIME is None:
        total_time = 0
    else:
        total_time = (datetime.datetime.now() - config.RUN_START_TIME).total_seconds()

    def format_duration(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{int(h)}h {int(m)}m {s:.2f}s"

    runtime_info = {
        "total_run_time_seconds": total_time,
        "formatted_total_run_time": format_duration(total_time),
        "array_times": [
            {
                "array_size": size,
                "elapsed_seconds": elapsed,
                "formatted_elapsed": format_duration(elapsed),
            }
            for size, elapsed in config.ARRAY_TIME_LOG
        ],
    }

    try:
        with open("runtime_log.json", "w") as f:
            json.dump(runtime_info, f, indent=4)
        debug("Saved runtime log to runtime_log.json.")
    except Exception as e:
        debug(f"Error saving runtime log: {e}")


def graceful_exit(code=0):
    """
    Exit the program gracefully by first saving the runtime log and then terminating.

    Parameters:
      code (int): Exit status code (default is 0).
    """
    debug("Exiting program gracefully via graceful_exit().")
    save_runtime_log_json()
    sys.exit(code)


def signal_handler(signum, frame):
    """
    Handle termination signals (SIGINT, SIGTERM) by saving runtime stats and then exiting.

    Parameters:
      signum (int): Signal number.
      frame: Current stack frame.
    """
    debug(f"Received signal {signum}. Saving runtime log before exit.")
    save_runtime_log_json()
    sys.exit(0)


shutdown_requested = False
_shutdown_message_printed = False

# Register signal handlers.
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def on_exit():
    """
    atexit handler that saves the runtime log in JSON format and prints a final exit message.
    """
    if shutdown_requested:
        print("Exiting due to shutdown request.", flush=True)
    debug("Program exiting. on_exit handler called.")
    save_runtime_log_json()


atexit.register(on_exit)
