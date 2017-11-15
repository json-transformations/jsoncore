import sys

PY3 = sys.version_info.major == 3
PY34_PLUS = PY3 and sys.version_info.minor >= 4

if PY3:
    from io import StringIO
    from itertools import filterfalse
    from functools import reduce
    string_type, text_type = (str, str)
else:
    from io import open
    from itertools import ifilter as filter
    from itertools import ifilterfalse as filterfalse
    from itertools import imap as map
    from StringIO import StringIO
    string_type, text_type = (str, unicode)
if PY34_PLUS:
    from contextlib import suppress
else:
    from contextlib2 import suppress

map, filter, reduce = map, filter, reduce
open = open
