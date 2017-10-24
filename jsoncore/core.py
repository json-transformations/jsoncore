"""
EXPIRIMENTAL ... UNDER CONSTRUCTION!!!
"""

from operator import getitem

from treecrawler import node_visitor

from ._compat import suppress, reduce_ as reduce


def get_value(d, keys, default=None, ignore=(IndexError, KeyError)):
    """Get a value from a JSON document given a list of keys."""
    with suppress(*ignore):
        return reduce(getitem, keys, d)
    return default


def get_parent(d, keys):
    return d if len(keys) == 1 else get_value(d, keys[:-1])


def set_value(d, keys, value, ignore=(IndexError, KeyError)):
    """Set a value in a JSON document given a list a keys."""
    with suppress(*ignore):
        get_parent(d, keys)[keys[-1]] = value


def del_key(d, keys, ignore=(IndexError, KeyError)):
    """Delete an item from a JSON document given a list of keys."""
    with suppress(*ignore):
        del get_parent(d, keys)[keys[-1]]


def values(d):
    return node_visitor(d, lambda x: x.value)


def keys(d):
    return set(node_visitor(d, lambda x: x.keys))


def items(d):
    return node_visitor(d, lambda x: (x.keys, x.value))
