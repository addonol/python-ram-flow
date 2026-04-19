"""RAM-FLOW: A high-precision memory flow tracker for Python processes.

This package provides tools to monitor RAM consumption per function call,
generate visual execution trees, and audit memory release integrity.
"""

from .core import tracker, RamFlow

__version__: str = "1.0.0"
__all__: list[str] = ["tracker", "RamFlow"]


def get_tracker() -> RamFlow:
    """Returns the global singleton instance of the RamFlow tracker.

    Returns:
        RamFlow: The active memory tracker instance.
    """
    return tracker
