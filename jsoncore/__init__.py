"""jsoncore - Package description."""
from ._compat import suppress
from .core import jsondel, jsonget, jsonset, jsonkeys, jsonvalues, jsonitems
from .parsekeys import REGEX
from .jsoncrawl import node_visitor

__version__ = '0.5'
