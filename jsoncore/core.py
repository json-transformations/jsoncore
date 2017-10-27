"""
EXPIRIMENTAL ... UNDER CONSTRUCTION!!!
"""
from collections import defaultdict
from operator import getitem

from ._compat import suppress, reduce_ as reduce
from .crawl import node_visitor
from .types import IDENTITY, get_min_max


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


def jsonvalues(d, ignore=('object', 'array')):
    """Return the value of each node in a JSON document."""
    return (v for k, v, t in node_visitor(d, lambda x: x) if t not in ignore)


def jsonkeys(d):
    """Return a set of unique keys found in a JSON document."""
    return set(node_visitor(d, lambda x: x.keys, element_ch='*'))


def jsonitems(d, ignore=('object', 'array')):
    """Return a (key, value) pair for each node in a JSON document."""
    nodes = node_visitor(d, lambda x: x)
    return ((k, v) for k, v, t in nodes if t not in ignore)


def jsontypes(d):
    """List data type, min & max values for each node in JSON document."""
    return reduce(get_min_max, node_visitor(d, IDENTITY), defaultdict(dict))


def jsoncounts(d):
    """List the length of each array in a JSON document."""
    return (('.'.join(n.keys), len(n.val)) for n in node_visitor(d, IDENTITY)
            if n.dtype == 'array')
