"""
DISCLAIMER: This scenario is COMPLETELY FICTITIOUS and for educational purposes only.
It is a technical metaphor designed to illustrate Python memory management.

STORY: The Triumph of the Optimized Pipeline
---------------------------------------------
This scenario demonstrates a perfectly managed workflow where every resource
is reclaimed, leading to a "SECURE" audit verdict.

1. THE START: The worker wakes up and loads the Enterprise Ecosystem (+400MB).
   The aircraft is heavy, but stable.

2. THE EXTRACTION: 5,000 product records are pulled from Oracle.
   RAM peaks, but the data is kept strictly within the function's local scope.

3. THE SMART CHECK: The worker queries ElasticSearch.
   --> THE SUCCESS: The developer used '_source' filtering to only pull IDs,
       reducing the payload. Most importantly, the temporary cache is
       explicitly cleared once the validation is done.

4. THE EFFICIENT DISPATCH: Tasks are enqueued to Faktory. Local variables
   are deleted as soon as they are no longer needed, allowing the
   Garbage Collector to work during the slow loop.

5. THE FINAL FLAG: Oracle connection is closed, and buffers are flushed.

6. THE AUDIT: RAM-FLOW confirms the victory: the process has returned
   to its baseline. The aircraft is empty and ready for the next flight.
"""

import time
import logging
from typing import List, Dict, Any
from ramflow import tracker

# --- LOGGER CONFIGURATION ---
logger = logging.getLogger("ramflow")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("RAM-FLOW: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.propagate = False

# --- ENGINE CONFIGURATION ---
tracker.env = "PRODUCTION"
tracker.threshold = 100

# Simulated cache that we WILL clear this time
SEARCH_CACHE: Dict[str, Any] = {}


def simulate_enterprise_infrastructure_load() -> List[bytearray]:
    """Simulates the baseline load of a large enterprise project."""
    infra_bloat = [bytearray(1024 * 1024) for _ in range(400)]
    tracker.log_django_bootstrap()
    return infra_bloat


@tracker.track("Oracle: Data Extraction")
def oracledb_extraction() -> List[bytearray]:
    """Extracts data and ensures it stays local to the caller."""
    data = [bytearray(1024 * 512) for _ in range(300)]
    time.sleep(1.0)
    return data


@tracker.track("Elastic: Optimized Check")
def elastic_integrity_check(erp_data: List[bytearray]) -> List[str]:
    """Queries ES with proper filtering and temporary caching.

    The results are stored globally but will be cleared by the orchestrator.
    """
    # Optimized result set (only IDs and small flags)
    es_results = {f"sku_{i}": "valid" for i in range(5000)}

    # Store for immediate use
    SEARCH_CACHE["current_session"] = es_results

    time.sleep(0.5)
    return list(es_results.keys())


@tracker.track("Faktory: Efficient Dispatch")
def slow_dispatch(skus: List[str]) -> None:
    """Enqueues tasks while other resources are being freed."""
    for i in range(min(len(skus), 10)):
        time.sleep(0.1)
    logger.info(f"Faktory: {len(skus)} items successfully dispatched.")


@tracker.track("Oracle: Connection Closure")
def oracledb_finalize() -> None:
    """Finalizes DB operations and flushes driver buffers."""
    time.sleep(0.5)
    logger.info("Oracle DB: Resources successfully released.")


def run_clean_story() -> None:
    """Orchestrates a successful, leak-free execution scenario."""

    # --- 1. PROLOGUE ---
    tracker.log_bootstrap()
    _infra = simulate_enterprise_infrastructure_load()

    # --- 2. THE JOURNEY ---
    try:
        # Step A: Load and process
        products = oracledb_extraction()

        # Step B: Check and validate
        valid_skus = elastic_integrity_check(products)

        # --- THE CLEANUP PHASE (The difference-maker) ---
        logger.info("Success: Clearing temporary session caches...")
        SEARCH_CACHE.clear()  # Explicitly release the global dict
        del products  # Release the massive Oracle list

        # Step C: Dispatch now runs with a lighter memory footprint
        slow_dispatch(valid_skus)

        # Step D: Finalize
        oracledb_finalize()

    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    # --- 3. THE REVELATION ---
    logger.info("Final Audit: Inspecting process reclamation state...")
    tracker.check_final_release(kill_on_leak=False)

    # 4. REPORTING
    report_path = tracker.generate_report(suffix="optimized_success_story")

    logger.info("Execution finished. Performance audit generated successfully.")
    logger.info(f"Review the GREEN report: {report_path}")


if __name__ == "__main__":
    run_clean_story()
