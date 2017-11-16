from functools import wraps

from toolz import curry
from jsoncrawl import node_visitor

from .core import WILDCARD, del_key

from .parse import parse_keys
from .sequence import is_seq_and_not_str


def jsonkeys(d, arrays=True):
    """Return a set of unique keys found in a JSON document."""
    def getkeys(node):
        return node.keys

    keys = node_visitor(d, getkeys, arrays=arrays, element_ch=WILDCARD)
    return set(map(tuple, keys))


def parse_keystr(func):
    @wraps(func)
    def wrapper(keys, *args, **kwds):
        if not is_seq_and_not_str(keys):
            keys = parse_keys(keys)
        return func(keys, *args, **kwds)
    return wrapper


@curry
@parse_keystr
def jsondel(keys, *args, **kwds):
    del_key(keys, *args, **kwds)


def jsonvalues(d, arrays=True, ignore=('object', 'array')):
    """Return the value of each node in a JSON document."""
    nodes = node_visitor(d, lambda x: x, arrays=arrays)
    return (v for k, v, t in nodes if t not in ignore)
