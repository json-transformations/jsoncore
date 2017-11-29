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
    hash symbol would be a better choice to eliminate the need to escape wildcard characters in regular expressions.  Note: Regular
    expression syntax for JSON Keys is not currently supported, but
    there is a plan to include it in future versions.

"""
from operator import getitem

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


def join_keys(node, separator=SEPARATOR, wildcard=WILDCARD):
    """Return key names separated by dots; add wildcard tail to arrays.

    Returns a key string separated by the `separator` character;
    appends a wildcard symbol to keys that point to arrays.  This allows
    the location of arrays in the JSON data to be identified by simply
    looking at the resulting key strings.
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
    nodes = filter(lambda x: x.keys is not None, visited)
    keys = map(join_keys, nodes)
    types = ('array' if i.keys.endswith(wildcard) else i.dtype for i in keys)
    return zip(keys, (i.val for i in nodes), types)


def get_uniq_nodes(d, wildcard=WILDCARD):
    """Given JSON data; generate a unique, sorted sequence of nodes.

    Returns namedtuples Node(keys, val, dtype) sorted on keys where ...
        * `keys` are unique keystrings
        * `val` is the node's value
        * `dtype` is the JSON data type.
    """
    nodes = get_nodes(d, wildcard=wildcard)
    uniq = {i[0]: Node(i) for i in nodes}
    return sorted(uniq.values(), key=lambda x: x.keys)


def _get_keylist(node):
    return tuple(node.keys)


def get_keys(d, wildcard=WILDCARD):
    """Return a sorted sequence of unique keys found in the JSON data.

    Returns the key strings in attribute style notation with wildcards
    indicating the location of arrays.
    """
    nodes = get_uniq_nodes(d, wildcard=wildcard)
    return map(_get_keylist, nodes)
