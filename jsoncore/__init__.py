"""jsoncore - Package description."""
from ._compat import suppress
from .core import get_value, get_item, set_value, del_key
from .core import jsonkeys, jsonvalues, jsonitems
from .parse import REGEX

__version__ = '0.5'
