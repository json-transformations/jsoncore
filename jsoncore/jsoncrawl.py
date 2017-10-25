"""JSON node visitor.

Yields results of user provided `process_node` funct.

The `process node` function accepts Nodes; Nodes are 3-D named tuples:
    1. The node's path; a list of JSON object keys/indexes.
    2. The node's value.
    3. The node's JSON data type (i.e. object, array, string, number, etc.)

Options:
    * Option to crawl through JSON objects.
    * Option to crawl through JSON arrays.
    * Option to use wildcard characters to substitute for index numbers.
"""
from collections import deque, namedtuple
from itertools import repeat

from ._compat import string_type, text_type

DONT_ITER_TYPES = string_type, text_type
Node = namedtuple('Node', ['keys', 'val', 'dtype'])
JSON_TYPES = {
    dict: 'object',
    list: 'array',
    string_type: 'string',
    text_type: 'string',
    int: 'number (int)',
    float: 'number (real)',
    bool: 'boolean',
    type(None): 'null'
}


def get_type(value):
    return JSON_TYPES[type(value)]


def get_children(node, element_char, objects=True, arrays=False):
    """Return the children of this Node as a list of Nodes."""
    items = []

    if node.dtype == 'object' and objects:
        items = node.val.items()

    if node.dtype == 'array' and (element_char or arrays):
        if element_char:
            items = zip(repeat(element_char), node.val)
        else:
            items = enumerate(node.val)

    return [Node(node.keys + (k,), v, get_type(v)) for k, v in items]


def node_visitor(d, process_node, objects=True, arrays=False, element_ch=None):
    """Call process_node funct for every node in tree and yield results.

    d (obj):
        Data to traverse (the tree)

    process_node (funct):
        Accepts a Node as an arg.
        Example: `lambda node: '.'.join(map(str, node.keys))`

    objects (bool):
        Visit the items in an object?

    arrays (bool):
        Visit the elements in arrays? Automatically set if `element_ch`.

    element_char (str):
        Replaces sequence index numbers with this character when set;
        if not visit_arrays then ignore this option.
    """
    first_node = Node(keys=(), val=d, dtype=get_type(d))
    to_crawl = deque([first_node])
    while to_crawl:
        node = to_crawl.popleft()
        yield process_node(node)
        children = get_children(node, element_ch, objects, arrays)
        to_crawl.extend(children)
