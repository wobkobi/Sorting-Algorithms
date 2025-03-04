"""
exit_handlers.py

Handles graceful shutdown of the benchmark application.

This module sets up signal handlers for SIGINT and SIGTERM and registers an atexit
handler to print a final shutdown message if a termination was requested.
"""

import atexit
import signal
import sys

# Global flag to indicate if a shutdown has been requested.
shutdown_requested = False
# Internal flag to ensure the shutdown message is printed only once.
_shutdown_message_printed = False


def signal_handler(signum, frame):
    """
    Handle termination signals (SIGINT, SIGTERM).

    Sets the global shutdown flag, prints a shutdown message (once), and exits.
    """
    global shutdown_requested, _shutdown_message_printed
    if not _shutdown_message_printed:
        print(
            "\nShutdown requested. Cancelling pending tasks and exiting gracefully...",
            flush=True,
        )
        _shutdown_message_printed = True
    shutdown_requested = True
    sys.exit(0)


# Register signal_handler for SIGINT and SIGTERM.
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def on_exit():
    """
    atexit handler to print a final exit message if shutdown was requested.
    """
    if shutdown_requested and not _shutdown_message_printed:
        print("Exiting due to shutdown request.", flush=True)


atexit.register(on_exit)
