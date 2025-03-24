"""
exit_handlers.py

Handles graceful shutdown of the benchmark application.
This module sets up signal handlers for SIGINT and SIGTERM and registers an atexit
handler to print a final exit message if a shutdown is requested.
"""

import atexit
import signal
import sys
from .config import debug

shutdown_requested = False
_shutdown_message_printed = False


def signal_handler(signum, frame):
    """
    Handle termination signals (SIGINT, SIGTERM).

    Sets the shutdown flag, prints a shutdown message once, and exits.

    Parameters:
      signum (int): The signal number.
      frame: Current stack frame.
    """
    global shutdown_requested, _shutdown_message_printed
    debug(f"Received signal {signum}. Initiating shutdown.")
    if not _shutdown_message_printed:
        print(
            "\nShutdown requested. Cancelling pending tasks and exiting gracefully...",
            flush=True,
        )
        _shutdown_message_printed = True
    shutdown_requested = True
    sys.exit(0)


# Register signal handlers.
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def on_exit():
    """
    atexit handler to print a final exit message if shutdown was requested.
    """
    if shutdown_requested and not _shutdown_message_printed:
        print("Exiting due to shutdown request.", flush=True)
    debug("Program exiting. on_exit handler called.")


atexit.register(on_exit)
