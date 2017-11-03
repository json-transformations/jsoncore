"""
EXPIRIMENTAL ... UNDER CONSTRUCTION!!!
"""
from operator import getitem

from toolz import identity

from jsoncrawl import node_visitor

from ._compat import suppress, reduce_ as reduce

SUPPRESS = (IndexError, KeyError)
WILDCARD = '*'


def get_value(d, keys, default=None, ignore=SUPPRESS):
    """Get a value from a JSON document given a list of keys."""
    with suppress(*ignore):
        return reduce(getitem, keys, d)
    return default


def get_item(d, keys, default=None, fullpath=False, ignore=SUPPRESS):
    """Get a key/value pari from a JSON document given a list of keys."""
    key = '.'.join(keys) if fullpath else keys[:-1]
    with suppress(*ignore):
        value = get_value(d, keys, default=default, ignore=ignore)
        return key, value
    return key, default


def get_parent(d, keys):
    """Get the parent key."""
    return d if len(keys) == 1 else get_value(d, keys[:-1]) or {}


def set_value(d, keys, value, ignore=SUPPRESS):
    """Set a value in a JSON document given a list a keys."""
    with suppress(*ignore):
        get_parent(d, keys)[keys[-1]] = value


def del_key(d, keys, ignore=SUPPRESS):
    """Delete an item from a JSON document given a list of keys."""
    with suppress(*ignore):
        del get_parent(d, keys)[keys[-1]]


def jsonvalues(d, arrays=True, ignore=('object', 'array')):
    """Return the value of each node in a JSON document."""
    nodes = node_visitor(d, identity, arrays=arrays)
    return (v for k, v, t in nodes if t not in ignore)


def jsonkeys(d, arrays=True):
    """Return a set of unique keys found in a JSON document."""
    def getkeys(node):
        return node.keys

    keys = node_visitor(d, getkeys, arrays=arrays, element_ch=WILDCARD)
    return set(map(tuple, keys))


def jsonitems(d, arrays=True, ignore=('object', 'array')):
    """Return a (key, value) pair for each node in a JSON document."""
    nodes = node_visitor(d, identity, arrays=arrays)
    return ((k, v) for k, v, t in nodes if t not in ignore)


'''
def jsontypes(d, all_=True):
    """List data type, min & max values for each node in JSON document."""
    visitor = node_visitor(d, IDENTITY, arrays=all_, element_ch=WILDCARD)
    return reduce(get_min_max, visitor, defaultdict(dict))


def jsoncounts(d):
    """List the length of each array in a JSON document."""
    return (('.'.join(n.keys), len(n.val)) for n in node_visitor(d, IDENTITY)
            if n.dtype == 'array')
'''
