"""JSON Transformations Core Module.

Terminology
-----------

JSON data
    A Python object typically decoded from a JSON file or string or
    any Python object that is composed solely of dictionaries, lists,
    booleans, floats, integers, strings and None.

JSON key
    A _keylist_ or _keystring_, see below.

keylist
    A sequence of key names (strings), indexes (integers) and/or slice
    objects pointing to a JSON data location.  This is the preferred
    representation of the location specifiers when working inside of
    Python.

keystring
    Similar to a keylist except the sequence elelments are joined
    together by _separator_ characters and represented as strings.
    This is the representation is more suitable for user interfaces
    such as the command-line, the calculator interface, etc.

suppress
    Sometimes it is desirable to suppress exceptions and fall back to a
    default behavior rather than interrupting processing and throwing an
    error.  This is configurable for many of the functions in this
    module.  To select the exceptions to suppress set the `ignore`
    option to a list or tuple of valid Python Exception classes.

wildcard
    The wildcard character is used in JSON Keys to designate the
    location of arrays in JSON data.  If the `wildcard` character is
    set to None then each array element is returned. By default it is
    the splat character, but it's configurable since in regular
    expressions the character has special meaning. In these instances a
    hash symbol would be a better choice to eliminate the need to escape
    wildcard characters in regular expressions.  Note: Regular
    expression syntax for JSON Keys is not currently supported, but
    there is a plan to include it in future versions.

"""
from operator import getitem

from toolz import curry

from jsoncrawl.core import Node, node_visitor

from ._compat import suppress, reduce

WILDCARD = '*'
SEPARATOR = '.'
SUPPRESS = (IndexError, KeyError, TypeError)


def get_value(keylist, d, default=None, ignore=SUPPRESS):
    """Given a sequence of keys & JSON data; return the value.

    `ignore` is an optional tuple of suppressed exceptions.  If an
    exception occurs and is suppressed the `default` value is returned.
    """
    with suppress(*ignore):
        return reduce(getitem, keylist, d)
    return default


def get_parent(keylist, d):
    """Given a sequence of keys & JSON data; return the parent value.

    If the specififed key has no parent then return original JSON data.
    """
    return d if len(keylist) == 1 else get_value(keylist[:-1], d) or {}


def set_value(keylist, value, d, ignore=SUPPRESS):
    """Given a sequence of keys, a value & JSON data; set the value.

    Returns the modified JSON data after the key's new value is set.

    `ignore` is an optional tuple of suppressed exceptions.  If an
    exception occurs and is suppressed the original JSON data is
    returned.
    """
    with suppress(*ignore):
        get_parent(keylist, d)[keylist[-1]] = value
    return d


def del_key(keylist, d, ignore=SUPPRESS):
    """Given a sequence of keys & JSON data; remove the specified key.

    `ignore` is an optional tuple of suppressed exceptions.  If an
    exception occurs and is suppressed the original JSON data is
    returned. Otherwise, returns the modified JSON data after the key is
    dropped.
    """
    with suppress(*ignore):
        del get_parent(keylist, d)[keylist[-1]]
    return d


def get_item(keylist, d, default=None, fullpath=False, ignore=SUPPRESS):
    """Given a sequence of keys & JSON data; return the key/value pair.

    `ignore` is an optional tuple of suppressed exceptions.  If an
    exception occurs and is suppressed the `default` value is returned.

    Returns a two element tuple (key, value) where ...
    `key` is a string.  If the `fullpath` option is set, then the `key`
    is set to the keys in the `keylist` joined and separated by dots.
    Otherwise, the `key` is set to the last key in the `keylist`.
    """
    key = '.'.join(map(str, keylist)) if fullpath else keylist[-1]
    with suppress(*ignore):
        value = get_value(keylist, d, default=default, ignore=ignore)
        return key, value
    return key, default


@curry
def wildcard_to_array(node, wildcard='*'):
    if node.keys[-1:] == wildcard:
        return 'array'
    return node.dtype


@curry
def join_keys(node, separator=SEPARATOR, wildcard=WILDCARD):
    """Return key names separated by dots; tail a wildcard for arrays.

    Returns a keystring composed of keys in the keylist separated by the
    `separator` characters; also appends a `wildcard` character to any
    keystring that point to an array.  This allows the location of
    arrays in the JSON data to be identified by looking solely at the
    keystrings.
    """
    keys = node.keys
    if node.dtype == 'array':
        keys.append(wildcard)
    return separator.join(map(str, keys))


def get_nodes(d, wildcard=WILDCARD):
    """Given JSON data; generate a sequence of nodes.

    Returns namedtuples Node(keys, val, dtype) sorted on keys where ...
        * `keys` are unique keystrings
        * `val` is the node's value
        * `dtype` is the JSON data type.
    """
    visited = node_visitor(d, arrays=True, element_ch=wildcard)
    nodes = (i for i in visited if i.keys is not None)
    result = (Node(tuple(i.keys), i.val, i.dtype) for i in nodes)
    return result


def uniq_nodes(d, wildcard=WILDCARD):
    uniq = {i.keys: i for i in get_nodes(d, wildcard=wildcard)}
    return uniq.values()


def get_keys(d, wildcard=WILDCARD):
    """Given JSON data; return a unique, sorted list of keys.

    Returns Node(keys, val, dtype) namedtuples
    sorted on keys where ...
        * `keys` are unique keystrings
        * `val` is the node's value
        * `dtype` is the JSON data type.
    """
    nodes = uniq_nodes(d, wildcard=wildcard)
    keys = sorted({i.keys for i in nodes})
    return keys


def get_keystrings(d, separator=SEPARATOR, wildcard=WILDCARD):
    """Given JSON data; generate a unique, sorted list of keystrings."""
    keys = get_keys(d, wildcard=wildcard)
    return map(join_keys(separator=SEPARATOR), keys)
