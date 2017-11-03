from functools import wraps

from .core import SUPPRESS, get_value, get_item, set_value, del_key
from .parse import parse_keys


def parse_keystr(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        if args[0]:
            args = (args[0], parse_keys(args[1]))
            return func(*args, **kwds)
    return wrapper


@parse_keystr
def jsonget(d, keys, default=None, ignore=SUPPRESS):
    return get_value(d, keys, default=default, ignore=ignore)


@parse_keystr
def jsongetitem(d, keys, default=None, fullpath=False, ignore=SUPPRESS):
    return get_item(d, keys, default=default, fullpath=False, ignore=ignore)


@parse_keystr
def jsonset(d, keys, value, ignore=SUPPRESS):
    set_value(d, keys, value, ignore=ignore)


@parse_keystr
def jsondel(d, keys, ignore=SUPPRESS):
    del_key(d, keys, ignore=SUPPRESS)
