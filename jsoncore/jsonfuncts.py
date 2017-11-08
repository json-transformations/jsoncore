from functools import wraps

from toolz import curry

from jsoncrawl import node_visitor

from .core import WILDCARD, del_key, get_value, get_item, set_value
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


@curry
@parse_keystr
def jsonget(keys, *args, **kwds):
    return get_value(keys, *args, **kwds)


@curry
@parse_keystr
def jsongetitem(keys, *args, **kwds):
    return get_item(keys, *args, **kwds)


@curry
@parse_keystr
def jsonset(keys, *args, **kwds):
    set_value(keys, *args, **kwds)


def jsonitems(d, arrays=True, ignore=('object', 'array')):
    """Return a (key, value) pair for each node in a JSON document."""
    nodes = node_visitor(d, lambda x: x, arrays=arrays)
    return ((k, v) for k, v, t in nodes if t not in ignore)


def jsonvalues(d, arrays=True, ignore=('object', 'array')):
    """Return the value of each node in a JSON document."""
    nodes = node_visitor(d, lambda x: x, arrays=arrays)
    return (v for k, v, t in nodes if t not in ignore)


'''
jsonvalmap
jsonitemmap
jsonkeymap
jsonvalfilter
jsonkeyfilter
jsonitemfilter
jsonvalreduce
jsonkeyreduce
jsonitemreduce

def jsontypes(d, all_=True):
    """List data type, min & max values for each node in JSON document."""
    visitor = node_visitor(d, IDENTITY, arrays=all_, element_ch=WILDCARD)
    return reduce(get_min_max, visitor, defaultdict(dict))


def jsoncounts(d):
    """List the length of each array in a JSON document."""
    return (('.'.join(n.keys), len(n.val)) for n in node_visitor(d, IDENTITY)
            if n.dtype == 'array')
'''
