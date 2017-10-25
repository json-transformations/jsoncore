"""
EXPIRIMENTAL ... UNDER CONSTRUCTION!!!
"""
from operator import getitem

from .jsoncrawl import node_visitor

from ._compat import suppress, reduce_ as reduce


def jsonget(d, keys, default=None, ignore=(IndexError, KeyError)):
    """Get a value from a JSON document given a list of keys."""
    with suppress(*ignore):
        return reduce(getitem, keys, d)
    return default


def get_parent(d, keys):
    """Get the parent key."""
    return d if len(keys) == 1 else jsonget(d, keys[:-1]) or {}


def jsonset(d, keys, value, ignore=(IndexError, KeyError)):
    """Set a value in a JSON document given a list a keys."""
    with suppress(*ignore):
        get_parent(d, keys)[keys[-1]] = value


def jsondel(d, keys, ignore=(IndexError, KeyError)):
    """Delete an item from a JSON document given a list of keys."""
    with suppress(*ignore):
        del get_parent(d, keys)[keys[-1]]


def jsonvalues(d):
    """Return the value of each node in a JSON document."""
    return node_visitor(d, lambda x: x.val)


def jsonkeys(d):
    """Return a set of unique keys found in a JSON document."""
    return set(node_visitor(d, lambda x: x.keys, element_ch='*'))


def jsonitems(d):
    """Return a (key, value) pair for each node in a JSON document."""
    return node_visitor(d, lambda x: (x.keys, x.val))
