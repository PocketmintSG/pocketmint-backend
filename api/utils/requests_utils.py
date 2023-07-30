from datetime import datetime
from enum import Enum
import json
from bson import json_util


def dict_to_json(dct):
    for k, v in dct.items():
        if isinstance(v, datetime):
            dct[k] = str(dct[k])

    return dct


def model_to_dict(model):
    return json.loads(json.dumps(model.dict(), default=json_util.default))
