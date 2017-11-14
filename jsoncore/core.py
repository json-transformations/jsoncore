"""
EXPIRIMENTAL ... UNDER CONSTRUCTION!!!
"""
from operator import getitem

from ._compat import suppress, reduce

SUPPRESS = (IndexError, KeyError, TypeError)
WILDCARD = '*'


def get_value(keys, d, default=None, ignore=SUPPRESS):
    """Get a value from a JSON document given a list of keys."""
    with suppress(*ignore):
        return reduce(getitem, keys, d)
    return default


def get_item(keys, d, default=None, fullpath=False, ignore=SUPPRESS):
    """Get a key/value pari from a JSON document given a list of keys."""
    key = '.'.join(map(str, keys)) if fullpath else keys[-1]
    with suppress(*ignore):
        value = get_value(keys, d, default=default, ignore=ignore)
        return key, value
    return key, default


def get_parent(keys, d):
    """Get the parent key."""
    return d if len(keys) == 1 else get_value(keys[:-1], d) or {}


def set_value(keys, value, d, ignore=SUPPRESS):
    """Set a value in a JSON document given a list a keys."""
    with suppress(*ignore):
        get_parent(keys, d)[keys[-1]] = value
    return d


def del_key(keys, d, ignore=SUPPRESS):
    """Delete an item from a JSON document given a list of keys."""
    with suppress(*ignore):
        del get_parent(keys, d)[keys[-1]]
    return d
