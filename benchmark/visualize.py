import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs(
    "results/charts",
    exist_ok=True
)

df = pd.read_csv(
    "results/benchmark_results.csv"
)

# ==================================
# EXECUTION TIME
# ==================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["selectivity"],
    df["ship_mean"],
    marker="o",
    label="Ship Whole Table"
)

plt.plot(
    df["selectivity"],
    df["semi_mean"],
    marker="o",
    label="Semi Join"
)

plt.xlabel("Selectivity")
plt.ylabel("Mean Time (seconds)")
plt.title(
    "Execution Time vs Selectivity"
)

plt.grid(True)
plt.legend()

plt.savefig(
    "results/charts/execution_time.png"
)

plt.close()

# ==================================
# COMMUNICATION COST
# ==================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["selectivity"],
    df["ship_bytes"],
    marker="o",
    label="Ship Whole Table"
)

plt.plot(
    df["selectivity"],
    df["semi_bytes"],
    marker="o",
    label="Semi Join"
)

plt.xlabel("Selectivity")
plt.ylabel("Bytes Transferred")

plt.title(
    "Communication Cost"
)

plt.grid(True)
plt.legend()

plt.savefig(
    "results/charts/communication_cost.png"
)

plt.close()

# ==================================
# P99 LATENCY
# ==================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["selectivity"],
    df["ship_p99"],
    marker="o",
    label="Ship Whole Table"
)

plt.plot(
    df["selectivity"],
    df["semi_p99"],
    marker="o",
    label="Semi Join"
)

plt.xlabel("Selectivity")

plt.ylabel(
    "P99 Latency (seconds)"
)

plt.title(
    "Tail Latency Comparison"
)

plt.grid(True)
plt.legend()

plt.savefig(
    "results/charts/p99_latency.png"
)

plt.close()

print(
    "Charts generated."
)

# ==================================
# Communication Breakdown
# ==================================
plt.figure(figsize=(8,5))

plt.plot(
    df["selectivity"],
    df["semi_ids_sent_bytes"],
    marker="o",
    label="IDs Sent"
)

plt.plot(
    df["selectivity"],
    df["semi_rows_returned_bytes"],
    marker="o",
    label="Rows Returned"
)

plt.plot(
    df["selectivity"],
    df["semi_bytes"],
    marker="o",
    label="Total Bytes"
)

plt.xlabel("Selectivity")

plt.ylabel("Bytes")

plt.title(
    "Semi Join Communication Breakdown"
)

plt.legend()

plt.grid(True)

plt.savefig(
    "results/charts/semi_breakdown.png"
)

plt.close()