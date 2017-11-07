"""Apply a function to selected keys.

Includes support across nested multiple dimensional arrays.
"""
from contextlib import suppress
from itertools import groupby
from functools import reduce
from operator import eq, getitem

from toolz import curry, last

from .core import SUPPRESS, WILDCARD

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


@curry
def get_value(keys, d, default=None, ignore=SUPPRESS):
    """Get a value from a JSON document given a list of keys."""
    with suppress(*ignore):
        return reduce(getitem, keys, d)
    return default


def get_item(keys, d, default=None, fullpath=True, ignore=SUPPRESS):
    key = get_key(keys, fullpath)
    value = get_value(keys, d, default, ignore)
    return key, value


def get_items(keylist, d, fullpath=False):
    return [get_item(key, d, fullpath=fullpath) for key in keylist]


def get_parent(keys, d):
    """Get the parent key."""
    return d if len(keys) == 1 else get_value(d, keys[:-1]) or {}


def set_value(keys, value, d, ignore=SUPPRESS):
    """Set a value in a JSON document given a list a keys."""
    with suppress(*ignore):
        get_parent(keys, d)[keys[-1]] = value
        return value


def split_list(sep, seq):
    return [list(g) for k, g in groupby(seq, eq(sep)) if not k]


def map_values(
    keylist, funct, seq, default=None, fullpath=False, ignore=SUPPRESS
):
    with suppress(*ignore):
        for item in seq:
            for keys in keylist:
                value = funct(get_value(keys, item, default, ignore))
                set_value(get_key(keys, fullpath), value)


def filter_keys(
    keylist, funct, seq, default=None, fullpath=False, ignore=(SUPPRESS,)
):
    with suppress(*ignore):
        dtype = seq and get_type(seq[0])

        if dtype == 'object':
            get_value(default=default, ignore=ignore)
            return [{get_key(k): funct(get_value(k, i))
                    for k, v in i.items()} for i in seq]

        if dtype == 'array':
            return list(map(funct, seq))
        return seq


def splitlist(s, sep=WILDCARD):
    return [list(g) for k, g in groupby(s, eq(sep)) if not k]


def group_arrays(keys):
    def all_but_last(keys):
        return tuple(keys)[:-1]

    groups = groupby(map(splitlist, keys), all_but_last)
    groups = ((k, tuple(map(last, g))) for k, g in groups)
    return sorted(groups, key=lambda x: len(x[0]), reverse=True)


def apply_funct(funct, groups, array, keys, data):
    if groups:
        return [apply_funct(funct, groups[1:], array, keys, i)
                for i in get_value(groups[0], data)]
    if array:
        return funct(keys, get_value(array, data))
    return funct(keys, data)


def apply_keys(keys, funct, data):
    groups = group_arrays(keys)
    for group in groups:
        array_groups, array, keys = group[0][:-1], group[0][-1], group[-1:][0]
        value = apply_funct(funct, array_groups, array, keys, data)
        key = array_groups[0] if array_groups else array
        set_value(data, key, value)
    return data
