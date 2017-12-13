from .cli import (
    JSONFile, get_root, jsonfile, optional_jsonfile, rootkey, result
)
from .core import (
    WILDCARD, SEPARATOR, SUPPRESS,
    del_key, get_item, get_keys, get_keystrings, get_nodes, get_parent,
    get_value, join_keys, set_value, uniq_nodes
)
from .jsonfuncts import (
    jsondel, jsonget, jsongetitem, jsonset, jsonnodes, jsonkeys,
    jsonvalues, jsonitems
)
from .errors import RegExError, KeyNumError
from .functional import apply_funct, map_item, map_values
from .parse import parse_keylist, parse_keys

from jsoncat_tool.cli import (
    JSONFile, encoding_option, indent_option, jsonfiles_arg
)

__version__ = '0.6.2'
