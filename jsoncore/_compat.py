import sys

PY3 = sys.version_info.major == 3

if PY3:
    from contextlib import suppress
    from io import StringIO
    from itertools import filterfalse
    from functools import reduce
    string_type, text_type = (str, str)
else:
    from contextlib2 import suppress
    from itertools import ifilter as filter
    from itertools import ifilterfalse as filterfalse
    from itertools import imap as map
    from StringIO import StringIO
    string_type, text_type = (str, unicode)

map, filter, reduce = map, filter, reduce
