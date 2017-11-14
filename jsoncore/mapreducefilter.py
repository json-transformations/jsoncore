"""Apply a function to selected keys.

Includes support across nested multiple dimensional arrays.
"""
from collections import namedtuple
from copy import deepcopy
from functools import partial
from itertools import groupby
from operator import eq

from jsoncrawl import node_visitor

from ._compat import map, reduce, filter, filterfalse, suppress
from .core import WILDCARD, del_key, get_value, set_value

JSON_TYPES = {
    dict: 'object',
    list: 'array',
    str: 'string',
    int: 'number (int)',
    float: 'number (real)',
    bool: 'boolean',
    type(None): 'null'
}
SUPPRESS = Exception

ArrayKeys = namedtuple('ArrayKeys', ['arrays', 'keys'])


def get_key(keys, fullpath=False):
    return '.'.join(keys) if fullpath else keys[-1]


def get_type(value):
    return JSON_TYPES[type(value)]


def splitlist(s, sep=WILDCARD):
    """Break a list into lists split at separators."""
    return [list(g) for k, g in groupby(s, partial(eq, sep)) if not k]


def group_array_keys(keys):
    """Groups JSON selectors into arrays & keys.

    ArrayKeys tuple:
        1: Split key list into arrays
        2: Group keys by array

    Sorts ArrayKeys by number of arrays; descending order.

    Example:
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

    def array_count(group):
        return len(group.arrays)

    def key_list(group):
        return tuple(g[-1] for g in group)

    arrays = map(splitlist, keys)
    groups = groupby(arrays, all_but_last)
    array_keys = (ArrayKeys(k, key_list(g)) for k, g in groups)
    return sorted(array_keys, key=array_count, reverse=True)


def do_funct(funct, keys, d, ignore=(Exception,)):
    with suppress(*ignore):
        return funct(keys, d)
    return d


def key_funct(funct, arrays_to_crawl, last_array, keys, d, ignore=SUPPRESS):
    """Apply a function to a JSON Selector.

    Applies a function to a given list of selectors throuhout a JSON
    document; supports nested arrays & objects.
    """
    if arrays_to_crawl:
        this_array = arrays_to_crawl[0]
        to_crawl = arrays_to_crawl[1:]
        items = [key_funct(funct, to_crawl, last_array, keys, i)
                 for i in get_value(this_array, d)]
        return set_value(this_array, items, d)

    if last_array:
        items = do_funct(funct, keys, get_value(last_array, d))
        return set_value(last_array, items, d)

    # it's not an array; just keys
    return do_funct(funct, keys, d)


def apply_funct(keys, funct, d, ignore=SUPPRESS):
    """Apply a function to one or more JSON Selectors."""
    data = deepcopy(d)
    for group in group_array_keys(keys):
        arrays = list(group.arrays)
        last_array = arrays.pop() if arrays else None
        data = key_funct(funct, arrays, last_array, group.keys, data, ignore)
    return data


def map_item(keys, funct, item):
    """Apply function to items in a JSON document given a set of keys."""
    for key in keys:
        seq = map(partial(funct, key), item)
    return list(seq)


def map_values(keys, funct, seq):
    """Apply function to values in a JSON document."""
    def set_item(key, funct, d):
        return set_value(key, funct(get_value(key, d)), d)

    def valmap(keys, seq):
        # if not keys:
        #    import pdb; pdb.set_trace()
        for key in keys or node_visitor(seq, lambda x: x.keys, arrays=True):
            seq = map(partial(set_item, key, funct), seq)
        return list(seq)

    return apply_funct(keys, valmap, seq)


def map_keys(keys, funct, seq):
    """Apply function to specified keys in a JSON document."""
    def apply_funct(key, d):
        del_key(key, d)
        return set_value(funct(key), get_value(key, d))

    return map_items(keys, apply_funct, seq)


def filter_items(keys, funct, seq, on_false=False):
    """Apply function to items in a JSON document."""
    filter = filterfalse if on_false else filter
    for key in keys:
        seq = filter(partial(funct, key), seq)
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
    for key in keys:
        seq = reduce(partial(funct, key), seq)
    return list(seq)


def reduce_values(keys, funct, seq):
    def apply_funct(key, d):
        return funct(get_value(key, d))

    return reduce_items(keys, apply_funct, seq)


def reduce_keys(keys, funct, seq):
    def apply_funct(key, d):
        return funct(key)

    return reduce_items(keys, apply_funct, seq)
