from flask import Flask, jsonify
import pandas as pd
import logging
import os

app = Flask(__name__)

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/node_a.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def load_orders():
    return pd.read_csv(
        "node_a/data/orders.csv"
    )


@app.route("/orders")
def get_orders():

    orders = load_orders()

    logging.info(
        f"Returned {len(orders)} orders"
    )

    return jsonify(
        orders.to_dict(
            orient="records"
        )
    )


@app.route("/order-ids")
def get_order_ids():

    orders = load_orders()

    ids = orders["OrderID"].tolist()

    logging.info(
        f"Returned {len(ids)} order ids"
    )

    return jsonify(ids)

if __name__ == "__main__":

    print("NODE A START")
    print(__file__)

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )