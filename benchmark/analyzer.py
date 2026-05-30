import pandas as pd
import numpy as np
import os

RESULT_FILE = "results/benchmark_results.csv"

os.makedirs("results", exist_ok=True)


# =====================================
# INTERPOLATION BREAKEVEN
# =====================================

def interpolate_breakeven(df):

    for i in range(len(df) - 1):

        x1 = df.iloc[i]["selectivity"]
        x2 = df.iloc[i + 1]["selectivity"]

        y1 = (
            df.iloc[i]["semi_mean"]
            - df.iloc[i]["ship_mean"]
        )

        y2 = (
            df.iloc[i + 1]["semi_mean"]
            - df.iloc[i + 1]["ship_mean"]
        )

        # đổi dấu => giao điểm

        if y1 * y2 < 0:

            return (
                x1
                - y1 * (x2 - x1)
                / (y2 - y1)
            )

    return None


# =====================================
# BEST SAVING
# =====================================

def find_best_saving(df):

    savings = []

    for _, row in df.iterrows():

        ship = row["ship_mean"]
        semi = row["semi_mean"]

        saving = (
            (ship - semi)
            / ship
        ) * 100

        savings.append(saving)

    df["saving_percent"] = savings

    idx = df["saving_percent"].idxmax()

    return df.loc[idx]


# =====================================
# MAIN
# =====================================

df = pd.read_csv(
    RESULT_FILE
)

breakeven = interpolate_breakeven(df)

best = find_best_saving(df)

print("=" * 60)

if breakeven:

    print(
        f"Breakeven Selectivity ≈ {breakeven:.4f}"
    )

else:

    print(
        "No breakeven point detected."
    )

print()

print(
    f"Maximum Saving = "
    f"{best['saving_percent']:.2f}% "
    f"at Selectivity={best['selectivity']}"
)

print("=" * 60)


# =====================================
# GENERATE REPORT
# =====================================

report_lines = []

report_lines.append(
    "DISTRIBUTED JOIN ANALYSIS REPORT\n"
)

report_lines.append(
    "=" * 50 + "\n"
)

if breakeven:

    report_lines.append(
        f"Breakeven Selectivity: "
        f"{breakeven:.4f}\n"
    )

else:

    report_lines.append(
        "No Breakeven Point Found\n"
    )

report_lines.append(
    "\n"
)

report_lines.append(
    f"Best Semi Join Saving: "
    f"{best['saving_percent']:.2f}%\n"
)

report_lines.append(
    f"Occurred at Selectivity: "
    f"{best['selectivity']}\n"
)

report_lines.append("\n")

report_lines.append(
    "Per Scenario Summary\n"
)

report_lines.append(
    "-" * 50 + "\n"
)

for _, row in df.iterrows():

    report_lines.append(

        f"Selectivity={row['selectivity']:.2f} | "

        f"Ship Mean={row['ship_mean']:.4f}s | "

        f"Semi Mean={row['semi_mean']:.4f}s | "

        f"Ship Bytes={row['ship_bytes']:.0f} | "

        f"Semi Bytes={row['semi_bytes']:.0f}\n"
    )

with open(
    "results/report.txt",
    "w",
    encoding="utf-8"
) as f:

    f.writelines(report_lines)

print(
    "Report generated:"
)

print(
    "results/report.txt"
)