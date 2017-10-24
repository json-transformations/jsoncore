import sys

PY3 = sys.version_info.major == 3

if PY3:
    import functools
    from contextlib import suppress
    from io import StringIO
    from functools import reduce
else:
    from contextlib2 import suppress
    from StringIO import StringIO

reduce_ = reduce
