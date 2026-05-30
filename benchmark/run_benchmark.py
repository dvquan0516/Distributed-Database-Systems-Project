import requests
import time
import pandas as pd
import numpy as np
import json
import os
import logging

from benchmark.scenarios import SCENARIOS
from benchmark.metrics import calculate_stats
from data_generator.generate import generate_dataset

# =====================================
# CONFIG
# =====================================

RUNS_PER_SCENARIO = 10

NODE_A = "http://localhost:5001"
NODE_B = "http://localhost:5002"

os.makedirs("results", exist_ok=True)
os.makedirs("results/raw", exist_ok=True)
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/benchmark.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# =====================================
# SHIP WHOLE TABLE JOIN
# =====================================

def ship_whole_table_join():

    start = time.perf_counter()

    # Orders tồn tại tại Site A
    orders_resp = requests.get(
        f"{NODE_A}/orders"
    )

    orders = orders_resp.json()

    # Chỉ OrderItems được ship từ Site B
    items_resp = requests.get(
        f"{NODE_B}/order-items"
    )

    items = items_resp.json()

    communication_bytes = len(
        items_resp.content
    )

    df_orders = pd.DataFrame(
        orders
    )

    df_items = pd.DataFrame(
        items
    )

    result = df_orders.merge(
        df_items,
        on="OrderID"
    )

    elapsed = (
        time.perf_counter() - start
    )

    return {
        "time": elapsed,
        "bytes": communication_bytes,
        "rows": len(result)
    }


# =====================================
# SEMI JOIN
# =====================================

def semi_join():

    start = time.perf_counter()

    # Orders local tại Site A
    orders_resp = requests.get(
        f"{NODE_A}/orders"
    )

    orders = orders_resp.json()

    df_orders = pd.DataFrame(
        orders
    )

    order_ids = (
        df_orders["OrderID"]
        .unique()
        .tolist()
    )

    payload = {
        "order_ids": order_ids
    }

    ids_sent_bytes = len(
        json.dumps(payload).encode("utf-8")
    )

    try:

        filtered_resp = requests.post(
            f"{NODE_B}/filtered-items",
            json=payload,
            timeout=10
        )

        filtered = filtered_resp.json()

    except Exception as e:

        logging.error(
            f"Semi Join failed: {e}"
        )

        return None

    rows_returned_bytes = len(
        filtered_resp.content
    )

    total_bytes = (
        ids_sent_bytes
        + rows_returned_bytes
    )

    df_filtered = pd.DataFrame(
        filtered
    )

    result = df_orders.merge(
        df_filtered,
        on="OrderID"
    )

    elapsed = (
        time.perf_counter() - start
    )

    return {
        "time": elapsed,
        "ids_sent_bytes": ids_sent_bytes,
        "rows_returned_bytes": rows_returned_bytes,
        "bytes": total_bytes,
        "rows": len(result)
    }


# =====================================
# MAIN BENCHMARK
# =====================================

results = []
raw_results = []

for scenario in SCENARIOS:

    print(
        f"\nScenario {scenario}"
    )

    logging.info(
        f"Scenario={scenario}"
    )

    generate_dataset(
        selectivity=scenario
    )

    ship_times = []
    semi_times = []

    ship_bytes = []
    semi_bytes = []

    semi_ids_bytes = []
    semi_return_bytes = []

    failed_runs = 0

    for run in range(
        RUNS_PER_SCENARIO
    ):

        print(
            f"Run {run+1}/{RUNS_PER_SCENARIO}"
        )

        # -------------------
        # Ship Whole Table
        # -------------------

        ship = ship_whole_table_join()

        ship_times.append(
            ship["time"]
        )

        ship_bytes.append(
            ship["bytes"]
        )

        raw_results.append({
            "scenario": scenario,
            "run": run + 1,
            "strategy": "ship_whole_table",
            "time": ship["time"],
            "bytes": ship["bytes"],
            "rows": ship["rows"]
        })

        # -------------------
        # Semi Join
        # -------------------

        semi = semi_join()

        if semi is None:

            failed_runs += 1

            continue

        semi_times.append(
            semi["time"]
        )

        semi_bytes.append(
            semi["bytes"]
        )

        semi_ids_bytes.append(
            semi["ids_sent_bytes"]
        )

        semi_return_bytes.append(
            semi["rows_returned_bytes"]
        )

        raw_results.append({
            "scenario": scenario,
            "run": run + 1,
            "strategy": "semi_join",
            "time": semi["time"],
            "bytes": semi["bytes"],
            "ids_sent_bytes":
                semi["ids_sent_bytes"],
            "rows_returned_bytes":
                semi["rows_returned_bytes"],
            "rows": semi["rows"]
        })

    ship_stats = calculate_stats(
        ship_times
    )

    semi_stats = calculate_stats(
        semi_times
    )

    results.append({

        "selectivity":
            scenario,

        # ----------------
        # Ship
        # ----------------

        "ship_mean":
            ship_stats["mean"],

        "ship_median":
            ship_stats["median"],

        "ship_p99":
            ship_stats["p99"],

        "ship_std":
            ship_stats["std"],

        "ship_bytes":
            float(
                np.mean(
                    ship_bytes
                )
            ),

        # ----------------
        # Semi
        # ----------------

        "semi_mean":
            semi_stats["mean"],

        "semi_median":
            semi_stats["median"],

        "semi_p99":
            semi_stats["p99"],

        "semi_std":
            semi_stats["std"],

        "semi_bytes":
            float(
                np.mean(
                    semi_bytes
                )
            ),

        "semi_ids_sent_bytes":
            float(
                np.mean(
                    semi_ids_bytes
                )
            ),

        "semi_rows_returned_bytes":
            float(
                np.mean(
                    semi_return_bytes
                )
            ),

        # ----------------

        "failure_count":
            failed_runs
    })

# =====================================
# SAVE SUMMARY
# =====================================

with open(
    "results/benchmark_results.json",
    "w"
) as f:

    json.dump(
        results,
        f,
        indent=4
    )

pd.DataFrame(
    results
).to_csv(
    "results/benchmark_results.csv",
    index=False
)

# =====================================
# SAVE RAW RUNS
# =====================================

with open(
    "results/raw/raw_runs.json",
    "w"
) as f:

    json.dump(
        raw_results,
        f,
        indent=4
    )

pd.DataFrame(
    raw_results
).to_csv(
    "results/raw/raw_runs.csv",
    index=False
)

logging.info(
    "Benchmark finished."
)

print(
    "\nBenchmark completed."
)