import json


def get_payload_size(data):
    """
    Tính kích thước payload (bytes)
    """
    return len(
        json.dumps(data).encode("utf-8")
    )