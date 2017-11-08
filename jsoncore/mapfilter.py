"""Apply a function to selected keys.

Includes support across nested multiple dimensional arrays.
"""
from contextlib import suppress
from itertools import groupby
from operator import eq, getitem

from toolz import curry, last

from jsoncrawl import node_visitor

from ._compat import map, reduce, filter, filterfalse
from .core import SUPPRESS, WILDCARD, del_key, get_value, set_value

eq = curry(eq)

JSON_TYPES = {
    dict: 'object',
    list: 'array',
    str: 'string',
    int: 'number (int)',
    float: 'number (real)',
    bool: 'boolean',
    type(None): 'null'
}


def get_key(keys, fullpath=False):
    return '.'.join(keys) if fullpath else keys[-1]


def get_type(value):
    return JSON_TYPES[type(value)]


def splitlist(s, sep=WILDCARD):
    """Break a list into lists split at separators."""
    return [list(g) for k, g in groupby(s, eq(sep)) if not k]


def group_arrays(keys):
    """Split a keylist groups of keys for each array.

    Each keylist is split into tuples:
    1st element - A list of keys pointing to arrays in order of depth.
    2nd element - A group of keys referenced by the last array.

    Sorts top-down by number of arrays found.

    >>> keys = [
        ['solar system', 'planets', 'number'],
        ['sun', 'planets', '*', 'moons', '*', 'craters', '*', 'name'],
        ['sun', 'planets', '*', 'moons', '*', 'craters', '*', 'size']]
    >>> group_arrays(keys)
    (['sun', 'planets'], ['moons'], ['craters']), (['name'], ['size'])),
    ((), (['solar system', 'planets', 'number'],))]
    """
    def all_but_last(keys):
        return tuple(keys)[:-1]

    groups = groupby(map(splitlist, keys), all_but_last)
    groups = ((k, tuple(map(last, g))) for k, g in groups)
    return sorted(groups, key=lambda x: len(x[0]), reverse=True)


def apply_funct(funct, groups, array, keys, data):
    """Apply a function to a list of keys inside a JSON document.

    Allows a function to be applied to a given list of selectors
    throuhout a JSON document; supports nested arrays & objects.
    """
    if groups:
        items = [apply_funct(funct, groups[1:], array, keys, i)
                 for i in get_value(groups[0], data)]
        return set_value(groups[0], items, data)

    if array:
        items =  funct(keys, get_value(array, data))
        return set_value(array, items, data)

    return funct(keys, data)

def apply_keys(keys, funct, data):
    groups = group_arrays(keys)
    for group in groups:
        array_groups, array, keys = group[0][:-1], group[0][-1], group[-1:][0]
        data = apply_funct(funct, array_groups, array, keys, data)
    return data


def map_items(keys, funct, seq):
    """Apply function to items in a JSON document given a set of keys."""
    fn = curry(funct)
    for key in keys:
        seq = map(fn(key), seq)
    return list(seq)


def map_values(keys, funct, seq):
    """Apply function to values in a JSON document."""
    def apply_funct(key, d):
        return set_value(key, funct(get_value(key, d)))

    return map_items(keys, apply_funct, seq)


def map_keys(keys, funct, seq):
    """Apply function to specified keys in a JSON document."""
    def apply_funct(key, d):
        del_key(key, d)
        return set_value(funct(key), get_value(key, d))

    return map_items(keys, apply_funct, seq)


def filter_items(keys, funct, seq, on_false=False):
    """Apply function to items in a JSON document."""
    funct = curry(funct)
    filter = filterfalse if on_false else filter
    for key in keys:
        seq = filter(funct(key), seq)
    return list(seq)


def filter_values(keys, funct, seq, on_false=False):
    """Filter items in a JSON document by value."""
    def apply_funct(key, d):
        return funct(get_value(key, d))

    return filter_items(keys, apply_funct, seq, on_false=on_false)


def filter_keys(keys, funct, seq, on_false=False):
    """Filter keys in a JSON document."""
    def apply_funct(key, d):
        for key in node_visitor(d):
            if funct(key) == on_false:
                del_key(key, d)
        return d

    return filter_items(keys, apply_funct, seq, on_false=on_false)


def reduce_items(keys, funct, seq):
    """Reduce key, value pairs in a JSON document."""
    funct = curry(funct)
    for key in keys:
        seq = reduce(funct(key), seq)
    return list(seq)


def reduce_values(keys, funct, seq):
    def apply_funct(key, d):
        return funct(get_value(key, d))

    return reduce_items(keys, apply_funct, seq)


def reduce_keys(keys, funct, seq):
    def apply_funct(key, d):
        return funct(key)

    return reduce_items(keys, apply_funct, seq)
