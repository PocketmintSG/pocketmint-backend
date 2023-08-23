from datetime import datetime
from enum import Enum
import json
from bson import ObjectId, json_util


def dict_to_json(dct):
    for k, v in dct.items():
        if isinstance(v, datetime) or isinstance(v, ObjectId):
            dct[k] = str(dct[k])
    return dct


def model_to_dict(model):
    return json.loads(json.dumps(model.dict(), default=json_util.default))


def get_chunks(items, chunk_size):
    """
    Split a list of items into chunks of the specified size.

    Args:
        items (list): The list of items to be split into chunks.
        chunk_size (int): The size of each chunk.

    Returns:
        list: A list of lists, each containing chunk_size number of items.
    """
    if chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer.")

    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]
