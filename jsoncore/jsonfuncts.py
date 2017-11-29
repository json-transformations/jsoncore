from functools import wraps

from toolz import curry

from jsoncrawl import node_visitor

from .core import (
    WILDCARD, SUPPRESS, del_key, get_item, get_keys, get_nodes,
    get_value, set_value
)
from .parse import parse_keys
from .sequence import is_seq_and_not_str


def key_parser(func):
    @wraps(func)
    def wrapper(keys, *args, **kwds):
        if not is_seq_and_not_str(keys):
            keys = parse_keys(keys)
        return func(keys, *args, **kwds)
    return wrapper


@curry
@key_parser
def jsonget(keylist, d, default=None, ignore=SUPPRESS):
    return get_value(keylist, d, default=default, ignore=ignore)


@curry
@key_parser
def jsongetitem(keylist, d, default=None, fullpath=False, ignore=SUPPRESS):
    return get_item(keylist, d, default=None, fullpath=False, ignore=SUPPRESS)


@curry
@key_parser
def jsonset(keylist, value, d, ignore=SUPPRESS):
    return set_value(keylist, value, d, ignore=ignore)


@curry
@key_parser
def jsondel(keylist, d, ignore=SUPPRESS):
    return del_key(keylist, d, ignore=ignore)


def jsonnodes(d, wildcard=WILDCARD):
    """Given JSON data; yield each node."""
    for node in node_visitor(d, arrays=True, element_ch=wildcard):
        if node.keys is not None:
            yield node


def jsonitems(d, wildcard=WILDCARD):
    """Given JSON data; yield each keystring/value pair."""
    for node in get_nodes(d, wildcard=wildcard):
        yield node.keys, node.value


def jsonkeys(d, wildcard=WILDCARD):
    """Given JSON data; yield each keystring in sort order."""
    for key in get_keys(d, wildcard=WILDCARD):
        yield key


def jsonvalues(d, arrays=True, wildcard=WILDCARD):
    """Given JSON data; yield each value."""
    for node in jsonnodes(d, wildcard=wildcard):
        if node.dtype not in ('array', 'object'):
            yield node.val
