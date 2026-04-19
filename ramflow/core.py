"""Core tracking logic for RAM-FLOW.

This module provides the main instrumentation engine to monitor memory flux,
calculate net self-consumption of functions, and handle framework overhead.
"""

import os
import time
import psutil
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from .config import HARD_LIMIT, THRESHOLD
from .utils import force_release, kill_process


class RamFlow:
    """Main memory tracker engine for instrumentation and auditing.

    This class provides the core logic to monitor memory consumption, distinguish
    between framework overhead and business logic, and generate detailed reports.

    Attributes:
        proc (psutil.Process): Reference to the current OS process.
        ref_mem (float): Initial memory baseline captured at initialization (MB).
        django_overhead (float): Captured memory delta of the Django framework (MB).
        threshold (int): Memory delta limit for task highlighting in reports.
        hard_limit (int): Absolute safety ceiling for process termination (MB).
        history (List[Dict[str, Any]]): Sequential log of all monitored tasks.
    """

    def __init__(
        self,
        threshold: int = THRESHOLD,
        hard_limit_mb: int = HARD_LIMIT,
    ):
        """Initializes the RamFlow engine and captures the starting baseline.

        Args:
            threshold (int): Memory delta in MB before highlighting a task.
            hard_limit_mb (int): Limit in MB before triggering the safety kill switch.
        """
        self.proc = psutil.Process(os.getpid())
        # ref_mem is the absolute Python bootstrap (Core libs)
        self.ref_mem: float = self.proc.memory_info().rss / 1024**2
        self.django_overhead: float = 0.0
        self.threshold: int = threshold
        self.hard_limit: int = hard_limit_mb
        self.history: List[Dict[str, Any]] = []

    @property
    def env(self) -> str:
        """Determines the execution environment from system variables.

        Returns:
            str: The current environment name (e.g., 'PRODUCTION', 'DEVELOPMENT').
        """
        from .config import ENV as DEFAULT_ENV

        return os.getenv("APP_ENV", DEFAULT_ENV).upper()

    @env.setter
    def env(self, value: str) -> None:
        """Overrides the execution environment at runtime.

        Args:
            value (str): Target environment name.
        """
        os.environ["APP_ENV"] = value.upper()

    def log_bootstrap(self) -> None:
        """Internal marker for the end of standard library imports.

        This method is kept for API consistency. The actual baseline is
        captured during class initialization.
        """
        pass

    def log_django_bootstrap(self) -> None:
        """Records the memory overhead of the Django framework initialization.

        Informs the engine that a framework is being used and adjusts the final
        leak calculation by deducting this ecosystem load from the baseline.
        """
        current_rss = self.proc.memory_info().rss / 1024**2
        self.django_overhead = round(current_rss - self.ref_mem, 2)

        self.history.append(
            {
                "label": "Django Ecosystem Load",
                "extra": "All INSTALLED_APPS",
                "diff": self.django_overhead,
                "duration": 0.0,
                "time": datetime.now().strftime("%H:%M:%S"),
                "type": "system",
            }
        )

    def track(self, label: Optional[Union[str, Callable]] = None) -> Callable:
        """Decorator to monitor the net memory consumption of a function.

        Calculates 'Net Self' memory by subtracting the consumption of any
        nested functions tracked by RAM-FLOW.

        Args:
            label (Optional[Union[str, Callable]]): Custom name for the task.
                If None, uses the function name.

        Returns:
            Callable: The wrapped function with memory monitoring.
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                name = (
                    label
                    if isinstance(label, str)
                    else func.__name__.replace("_", " ").upper()
                )
                extra = (
                    f"batch:{kwargs.get('batch_id')}" if "batch_id" in kwargs else ""
                )

                m_start = self.proc.memory_info().rss / 1024**2
                t_start = time.perf_counter()
                history_index_before = len(self.history)

                try:
                    return func(*args, **kwargs)
                finally:
                    m_end = self.proc.memory_info().rss / 1024**2
                    dur = time.perf_counter() - t_start

                    # Net Self-Memory Calculation
                    gross_diff = m_end - m_start
                    children_sum = sum(
                        item["diff"]
                        for item in self.history[history_index_before:]
                        if item.get("type") != "system"
                    )
                    net_diff = max(0.0, gross_diff - children_sum)

                    self.history.append(
                        {
                            "label": name,
                            "extra": extra,
                            "diff": round(net_diff, 2),
                            "duration": round(dur, 3),
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "type": "logic",
                        }
                    )

            return wrapper

        return decorator(label) if callable(label) else decorator

    def check_final_release(self, kill_on_leak: bool = False) -> float:
        """Audits memory reclamation against the final infrastructure baseline.

        Compares current RSS to the total baseline (Core Python + optional Django).
        Handles stabilization of negative values due to aggressive GC.

        Args:
            kill_on_leak (bool): If True, terminates the process if net leak
                exceeds the hard safety limit.

        Returns:
            float: The net residual memory leak in MB.
        """
        force_release()
        current_rss = self.proc.memory_info().rss / 1024**2

        # Baseline = Python Start + Framework (0.0 if not used)
        total_baseline = self.ref_mem + self.django_overhead
        leak = max(0.0, round(current_rss - total_baseline, 2))

        # Check for negative deltas
        if leak < -1.0:
            # A negative leak indicates that the process ended up lighter than its baseline.
            # I stabilize this to 0.00 MB for report consistency.
            leak = 0.0
        elif leak < 0:
            leak = 0.0

        # Security kill-switch remains active only for positive growth
        if kill_on_leak and leak > self.hard_limit:
            kill_process(os.getpid())

        return leak

    def generate_report(
        self, folder: Optional[str] = None, suffix: str = "audit"
    ) -> str:
        """Generates the Premium HTML report with automated smart naming.

        Triggers a final release audit, instantiates the reporter, and saves
        a standalone dashboard to the specified directory.

        Args:
            folder (Optional[str]): Target directory. Defaults to '.memory_audits'.
            suffix (str): Description suffix for the filename.

        Returns:
            str: The absolute path to the generated HTML report.
        """
        from .reporting import Reporter
        from .config import REPORTS_DIR

        target_dir = Path.cwd() / (folder or REPORTS_DIR)
        target_dir.mkdir(parents=True, exist_ok=True)

        now = datetime.now()
        filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{self.env}_{suffix}.html".lower()
        full_path = target_dir / filename

        residual = self.check_final_release()

        reporter = Reporter(
            history=self.history,
            start_mem=self.ref_mem,
            env=self.env,
            threshold=self.threshold,
            django_overhead=self.django_overhead,
        )

        reporter.render(str(full_path), residual_leak=residual)
        return str(full_path.absolute())


tracker = RamFlow()
