"""
Various data handling utilities
"""


def sanitize_boolean(val) -> bool:

    if type(val) is bool:
        return val

    if val:
        if val.lower() == "no" or val.lower() == "none" or val.lower() == "false":
            val = False
        elif val.lower() == "yes" or val.lower == "true":
            val = True

    return val
