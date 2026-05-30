import requests


def test_node_b_failure():

    try:

        requests.post(
            "http://localhost:5002/filtered-items",
            json={
                "order_ids": [1, 2, 3]
            },
            timeout=3
        )

        print(
            "Node B is alive."
        )

    except Exception as e:

        print(
            "Node B unavailable."
        )

        print(
            f"Error: {e}"
        )


if __name__ == "__main__":
    test_node_b_failure()