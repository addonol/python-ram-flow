"""Utility functions for system operations and data synchronization."""

import gc
import os
import signal


def force_release() -> None:
    """Triggers the Python Garbage Collector to free unreachable memory."""
    gc.collect()


def kill_process(pid: int) -> None:
    """Sends a SIGTERM signal to terminate a specific process.

    Args:
        pid (int): The process ID to terminate.
    """
    os.kill(pid, signal.SIGTERM)
