from enum import Enum


class NullType(str, Enum):
    NULL = None
    EMPTY = ""
