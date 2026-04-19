"""Configuration module for RAM-FLOW.

Defines environment variables, thresholds, and file paths.
"""

import os

THRESHOLD: int = int(os.getenv("RAMFLOW_THRESHOLD", 100))
HARD_LIMIT: int = int(os.getenv("RAMFLOW_HARD_LIMIT", 500))
ENV: str = os.getenv("APP_ENV", "DEVELOPMENT").upper()
REPORTS_DIR: str = os.getenv("RAMFLOW_REPORTS_DIR", ".memory_audits")
DEFAULT_NAMING_SCHEME: str = "{date}_{time}_{env}_{suffix}"
LEAK_MEDIUM_LIMIT: int = int(os.getenv("RAMFLOW_LEAK_MEDIUM", 5))
LEAK_HIGH_LIMIT: int = int(os.getenv("RAMFLOW_LEAK_HIGH", 20))
