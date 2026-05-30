from flask import Flask, request, jsonify
import pandas as pd
import logging
import time
import os

app = Flask(__name__)

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/node_b.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def load_items():

    path = os.path.abspath(
        "node_b/data/order_items.csv"
    )

    print("READING:", path)

    df = pd.read_csv(path)

    print(
        "MATCHING:",
        len(df[df["OrderID"] <= 10000])
    )

    return df

@app.route("/order-items")
def get_items():

    items = load_items()

    logging.info(
        f"Returned {len(items)} items"
    )

    return jsonify(
        items.to_dict(
            orient="records"
        )
    )


@app.route(
    "/filtered-items",
    methods=["POST"]
)
def filtered_items():

    # simulate WAN latency

    time.sleep(0.05)

    items = load_items()

    order_ids = request.json[
        "order_ids"
    ]

    filtered = items[
        items["OrderID"].isin(
            order_ids
        )
    ]

    print(
        "TOTAL ITEMS:",
        len(items)
    )

    print(
        "FILTERED:",
        len(filtered)
    )


    logging.info(
        f"Received {len(order_ids)} ids, returned {len(filtered)} rows"
    )

    return jsonify(
        filtered.to_dict(
            orient="records"
        )
    )


if __name__ == "__main__":

    print("NODE B START")
    print(__file__)

    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True
    )