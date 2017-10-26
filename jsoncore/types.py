"""List node types and min/max values in JSON document."""
from collections import defaultdict, namedtuple

import click

from ._compat import reduce_ as reduce
from .crawl import node_visitor

MinMax = namedtuple('MinMax', ['min', 'max'])
TRUE = lambda x: True
IDENTITY = lambda x: x
JSON_TYPES = {
    'null': ('', TRUE),
    'boolean': ('value', IDENTITY),
    'object': ('keys', len),
    'array': ('count', len),
    'string': ('length', len),
    'number (int)': ('value', IDENTITY),
    'number (real)': ('value', IDENTITY)
}


def get_min_max(keys, node):
    """Determine the JSON value type."""
    types = keys.get(node.keys, {})
    values = types.get(node.dtype)
    result = JSON_TYPES[node.dtype][-1](node.val)
    if values is None or True in values:
        min_ = max_ = result
    else:
        min_, max_ = min(values.min, result), max(values.max, result)
    keys[node.keys][node.dtype] = MinMax(min_, max_)
    return keys


def jsontypes(d, ):
    return reduce(get_min_max, node_visitor(d, IDENTITY), defaultdict(dict))


def format_result(d, colors=('white', 'cyan')):
    """Format & colorize the node type info."""
    def fmt_type(dtype, values):
        """Format the JSON type."""
        if dtype == 'null':
            return dtype

        fn_type = JSON_TYPES(dtype)[0]
        if values.min == values.max:
            mesg = '{dtype}({ftype}={val})'
            return mesg.format(dtype=dtype, ftype=fn_type, val=values.min)

        mesg = '{dtype}(min{ftype}={values.min}, max{ftype}={values.max})'
        return mesg.format(dtype=dtype, ftype=fn_type, values=values)

    d = sorted(d.items())
    keys, values = ['.'.join(k) for k, v in d], [v for k, v in d]
    padding = len(max(keys(), key=len))
    keys = (i.ljust(padding) for i in keys)
    values = (' | '.join(fmt_type(*i) for i in d.items()) for d in values)
    if colors:
        keys = (click.style(i, fg=colors[0]) for i in keys)
        values = (click.style(i, fg=colors[1]) for i in values)
    for key, val in zip(keys, values):
        yield key + ' :' + val


'''
def format_counts(d, nocolor=False, keys_fg='cyan', vals_fg='white'):
    """Format & colorize the inspection results."""
    padding = len(max(d.keys(), key=len))
    fmt_keys = [i.ljust(padding) for i in d.keys()]
    fmt_vals = [str(i) for i in d.values()]
    if not nocolor:
        fmt_keys = [click.style(i, fg=keys_fg) for i in fmt_keys]
        fmt_vals = [click.style(i, fg=vals_fg) for i in fmt_vals]
    for key, val in zip(fmt_keys, fmt_vals):
        yield key + ' : ' + str(val)


def count_arrays(d):
    is_array = is_sequence_and_not_str
    if is_array(d):
        return [len(d)]
    if isinstance(d, Mapping):
        counts = {k: len(v) for k, v in d.items() if is_array(v)}
        return format_counts(counts) if counts else ''
'''
