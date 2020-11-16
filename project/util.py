from functools import wraps
from flask import abort, request
from collections.abc import Iterable
from sqlalchemy.orm.collections import InstrumentedList


def serialize_data(data, schema):
    serialized_data = []
    if not data:
        return data
    if not schema:
        RuntimeWarning("No schema supplied to serialize data")
        return data
    if not isinstance(data, InstrumentedList) and not isinstance(data, list):
        return {k: v for (k, v) in data.__dict__.items() if k in schema.__fields__}
    else:
        for obj in data:
            serialized_data.append({k: v for (k, v) in obj.__dict__.items() if k in schema.__fields__})
    return serialized_data
