"""
Various data handling utilities
"""

import json


def sanitize_boolean(val) -> bool:

    if type(val) is bool:
        return val

    if val:
        if val.lower() == "no" or val.lower() == "none" or val.lower() == "false":
            val = False
        elif val.lower() == "yes" or val.lower == "true":
            val = True

    return val


def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(i) for i in obj]
    elif hasattr(obj, "__dict__"):
        return {k: to_dict(v) for k, v in obj.__dict__.items()}
    else:
        return obj


def from_dict(cls, dict_obj):
    obj = cls.__new__(cls)
    for k, v in dict_obj.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    return obj


class Serializable:
    def to_json(self):
        return json.dumps(to_dict(self), indent=2)

    @classmethod
    def from_json(cls, json_str):
        return from_dict(cls, json.loads(json_str))
