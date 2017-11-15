from .core import WILDCARD

from jsoncrawl import node_visitor


def jsonkeys(d, arrays=True, wildcard=WILDCARD):
    """Return a set of unique keys found in a JSON document."""
    def getkeys(node):
        return node.keys

    keys = node_visitor(d, getkeys, arrays=arrays, element_ch=wildcard)
    return set(map(tuple, keys))
