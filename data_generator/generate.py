import pandas as pd
import numpy as np
import os
import json

from pathlib import Path

ORDERS = 10000
ITEMS = 100000

RANDOM_SEED = 42

BASE_DIR = Path(__file__).resolve().parent.parent

ORDERS_PATH = BASE_DIR / "node_a" / "data" / "orders.csv"

ITEMS_PATH = BASE_DIR / "node_b" / "data" / "order_items.csv"

METADATA_PATH = BASE_DIR / "data_generator" / "metadata.json"


def generate_dataset(selectivity):

    np.random.seed(RANDOM_SEED)

    os.makedirs("node_a/data", exist_ok=True)
    os.makedirs("node_b/data", exist_ok=True)

    # =====================================
    # ORDERS (SITE A)
    # =====================================

    orders = pd.DataFrame({
        "OrderID": range(1, ORDERS + 1),
        "CustomerID": np.random.randint(
            1,
            3000,
            ORDERS
        )
    })

    orders.to_csv(
        ORDERS_PATH,
        index=False
    )

    # =====================================
    # SELECTIVITY CONTROL
    # =====================================

    matching_count = int(
        ITEMS * selectivity
    )

    non_matching_count = (
        ITEMS - matching_count
    )

    # rows that CAN join

    matching_order_ids = np.random.choice(
        orders["OrderID"],
        matching_count,
        replace=True
    )

    # rows that CANNOT join

    invalid_order_ids = np.arange(
        ORDERS + 1,
        ORDERS + non_matching_count + 1000
    )

    non_matching_order_ids = np.random.choice(
        invalid_order_ids,
        non_matching_count,
        replace=True
    )

    all_order_ids = np.concatenate([
        matching_order_ids,
        non_matching_order_ids
    ])

    np.random.shuffle(
        all_order_ids
    )

    # =====================================
    # ORDER ITEMS (SITE B)
    # =====================================

    order_items = pd.DataFrame({
        "ItemID": range(
            1,
            ITEMS + 1
        ),
        "OrderID": all_order_ids,
        "ProductID": np.random.randint(
            1,
            5000,
            ITEMS
        ),
        "Qty": np.random.randint(
            1,
            10,
            ITEMS
        )
    })

    order_items.to_csv(
        ITEMS_PATH,
        index=False
    )

    # =====================================
    # METADATA
    # =====================================

    actual_selectivity = (
        matching_count / ITEMS
    )

    metadata = {
        "orders": ORDERS,
        "order_items": ITEMS,
        "selectivity": actual_selectivity,
        "matching_rows": matching_count,
        "non_matching_rows": non_matching_count,
        "random_seed": RANDOM_SEED
    }

    with open(
        "data_generator/metadata.json",
        "w"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )

    # =====================================
    # SUMMARY
    # =====================================

    print("\n===================================")
    print(" DATASET GENERATED")
    print("===================================")
    print(f"Orders             : {ORDERS}")
    print(f"OrderItems         : {ITEMS}")
    print(f"Selectivity        : {actual_selectivity:.2f}")
    print(f"Matching Rows      : {matching_count}")
    print(f"Non-Matching Rows  : {non_matching_count}")
    print(f"Seed               : {RANDOM_SEED}")
    print("===================================\n")

if __name__ == "__main__":

    generate_dataset(
        selectivity=0.50
    )