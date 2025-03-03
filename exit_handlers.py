"""
exit_handlers.py

This module handles graceful shutdown and exit of the benchmark application.
It registers signal handlers to catch SIGINT and SIGTERM, sets a global shutdown flag,
and ensures a final exit message is printed when the program terminates.
"""

import atexit
import signal
import sys

# Global flag indicating whether a shutdown has been requested.
shutdown_requested = False


def signal_handler(signum, frame):
    """
    Handle incoming termination signals (SIGINT, SIGTERM).

    Sets the global shutdown flag and exits the program immediately.

    Parameters:
        signum (int): Signal number.
        frame (FrameType): Current stack frame.
    """
    global shutdown_requested
    shutdown_requested = True
    print("\nShutdown requested. Cancelling pending tasks and exiting gracefully...")
    sys.exit(0)


# Register the signal_handler for SIGINT and SIGTERM.
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def on_exit():
    """
    atexit handler to output a final message upon program termination.

    Indicates whether the exit was due to a shutdown request or was normal.
    """
    if shutdown_requested:
        print("Exiting due to shutdown request.")
    else:
        print("Exiting normally.")


atexit.register(on_exit)
