from datetime import datetime


def dict_to_json(dct):
    for k, v in dct.items():
        if isinstance(v, datetime):
            dct[k] = str(dct[k])

    return dct
