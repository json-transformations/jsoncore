from functools import reduce
from operator import getitem

from ._compat import suppress
from parsekeys import SLICE_RE


def getkey(d, *keys, default=None, ignore=(IndexError, KeyError)):
    """Get a value from a JSON document."""

    def get_(d, key):
        try:
            return getitem(d, key)
        except TypeError:
            if key.isdigit():
                return getitem(d, int(key))
            if SLICE_RE.match(key):
                if ':' not in key:
                    return d[int(key)]
                slice_indexes = (int(i) if i else None for i in key.split(':'))
                return d[slice(*(slice_indexes))]
            return default

    with suppress(*ignore):
        return reduce(get_, keys, d)
    return default


def delkey(d, *keys, ignore=(IndexError, KeyError)):

    def del_(d, key):
        try:
            del key
        except TypeError:
            key = keys[-1]
            if key.isdigit():
                del parent[int(key)]
            elif SLICE_RE.match(key):
                del parent[slice(key.split(':'))]
            else:
                raise

    with suppress(*ignore):
        parent = d if len(keys) == 1 else getkey(d, *keys[:-1])
        del_(parent[keys[-1]])


def setkey(d, *keys, value):
    pass


def get_values(d):
    pass


def get_keys(d):
    pass


def get_items(d):
    pass
