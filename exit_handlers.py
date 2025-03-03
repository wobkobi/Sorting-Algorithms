import atexit
import signal
import sys

# Global flag to indicate a shutdown has been requested.
shutdown_requested = False


def signal_handler(signum, frame):
    """
    Signal handler for graceful shutdown.
    Sets a global flag and exits immediately.
    """
    global shutdown_requested
    shutdown_requested = True
    print("\nShutdown requested. Cancelling pending tasks and exiting gracefully...")
    sys.exit(0)


# Register signal handlers for SIGINT and SIGTERM.
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def on_exit():
    """
    atexit handler to print a final message upon exiting.
    """
    if shutdown_requested:
        print("Exiting due to shutdown request.")
    else:
        print("Exiting normally.")


atexit.register(on_exit)
