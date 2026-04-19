"""
DISCLAIMER: This scenario is COMPLETELY FICTITIOUS and for educational purposes only.
It is a technical metaphor designed to illustrate Python memory management.

STORY: The Case of the Forgotten Search Cache
---------------------------------------------
Meet "The Sync Engine", a critical worker responsible for keeping our
Web Store in sync with our massive Oracle ERP.

1. THE START: The worker wakes up. It loads the heavy Enterprise Ecosystem
   (spaCy, Pandas, Scikit-Learn). Our "Truck" is already nearly full (+400MB).

2. THE EXTRACTION: The worker connects to Oracle and pulls product records.
   RAM climbs as descriptions and metadata fill the memory.

3. THE SMART CHECK: To be efficient, the worker queries ElasticSearch.
   --> THE FAILURE: Because '_source' filtering was forgotten, ES returns
       full documents. The results are stored in a global 'SEARCH_CACHE'
       variable that is never cleared.

4. THE SLOW DISPATCH: The worker enqueues tasks to Faktory one by one.
   This slow loop keeps the Oracle data AND the heavy ES cache locked in RAM.

5. THE FINAL FLAG: A heavy Bulk Update is performed in Oracle to wrap up.

6. THE AUDIT: RAM-FLOW reveals the truth: the "Forgotten Cache" created
   a massive footprint. On a server running this repeatedly, a crash is inevitable.
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
tracker.threshold = 100  # Threshold in MB for task highlighting

# Persistent storage simulation (The "Hidden Culprit")
SEARCH_CACHE: Dict[str, Any] = {}


def simulate_enterprise_infrastructure_load() -> List[bytearray]:
    """Simulates a heavy infrastructure load (spaCy, Pandas, Models).

    This helper function forces a memory allocation to simulate the resident
    size of an enterprise project with large ML dependencies.

    Returns:
        List[bytearray]: Simulated memory objects representing loaded libraries.
    """
    # Force ~400MB of resident memory to simulate heavy ecosystem imports
    infra_bloat = [bytearray(1024 * 1024) for _ in range(400)]
    tracker.log_django_bootstrap()
    return infra_bloat


@tracker.track("Oracle: Data Extraction ERP")
def oracledb_extraction() -> List[bytearray]:
    """Simulates pulling heavy product data from a legacy ERP database.

    Returns:
        List[bytearray]: List of binary-like objects representing raw data.
    """
    # Allocate ~150MB of simulated product data
    data = [bytearray(1024 * 512) for _ in range(300)]
    time.sleep(1.2)
    return data


@tracker.track("Elastic: Integrity Check")
def elastic_integrity_check(erp_data: List[bytearray]) -> List[str]:
    """Queries ElasticSearch to validate documents before dispatching.

    This function intentionally omits '_source' filtering to simulate
    heavy result sets and stores them in a global variable to create a leak.

    Args:
        erp_data (List[bytearray]): Current working set from the ERP.

    Returns:
        List[str]: List of valid document IDs ready for enqueuing.
    """
    # Simulate a heavy dicitonary (Full text + metadata fragments)
    # This creates a ~120MB memory impact
    es_results = {
        f"sku_{i}": f"full_source_content_{'x' * 4000}_metadata_v2" for i in range(5000)
    }

    # THE SILENT LEAK: Reference is kept in the global SEARCH_CACHE
    SEARCH_CACHE["current_session"] = es_results

    time.sleep(0.8)
    return list(es_results.keys())


@tracker.track("Faktory: Slow Queue Dispatch")
def slow_dispatch(skus: List[str]) -> None:
    """Enqueues tasks one by one to the background worker server.

    This slow loop mimics network latency, keeping all previously allocated
    memory locked in the process for a long duration.

    Args:
        skus (List[str]): List of document IDs to process.
    """
    for i in range(min(len(skus), 15)):
        time.sleep(0.2)  # Simulate network Round Trip Time (RTT)
    logger.info(f"Faktory Queue: {len(skus)} items successfully dispatched.")


@tracker.track("Oracle: Heavy Bulk Update")
def oracledb_bulk_sync_flag() -> None:
    """Performs final SQL bulk updates and simulates connection closure.

    Note: While closing the connection releases driver-level buffers,
    local variables holding results must still be manually cleared or scoped.
    """
    # Simulate driver-level buffer allocation during bulk write
    temp_driver_buffer = [bytearray(1024 * 1024) for _ in range(40)]
    time.sleep(0.9)
    del temp_driver_buffer
    logger.info("Oracle DB: Connection closed. Connection buffers released.")


def run_story_demo() -> None:
    """Orchestrates the end-to-end story-based performance scenario.

    Initializes the system, runs the heavy workflow, and performs the
    final memory audit to generate the audit report.
    """
    # --- 1. PROLOGUE: Wake up the engine ---
    tracker.log_bootstrap()

    # Boarding the heavy dependencies (+400MB)
    _enterprise_infra = simulate_enterprise_infrastructure_load()

    # --- 2. THE JOURNEY: Execute the logic ---
    try:
        # Step A: Load cargo from the ERP
        products = oracledb_extraction()

        # Step B: The efficiency trap (ES Unfiltered results)
        valid_skus = elastic_integrity_check(products)

        # Step C: The long wait during the slow enqueue
        slow_dispatch(valid_skus)

        # Step D: Final administrative paperwork
        oracledb_bulk_sync_flag()

    except Exception as e:
        logger.error(f"Process terminated due to unexpected error: {e}")

    # --- 3. THE REVELATION: Post-mortem audit ---
    logger.info("Final Audit: Inspecting process reclamation state...")
    tracker.check_final_release(kill_on_leak=False)

    # 4. REPORTING: Save and notify
    report_path = tracker.generate_report(suffix="enterprise_forgotten_cache")

    # Explicitly log the final report name as requested
    logger.info("Execution finished. Performance audit generated successfully.")
    logger.info(f"Review the report: {report_path}")


if __name__ == "__main__":
    run_story_demo()
