import csv
import re
from collections import namedtuple

from ._compat import StringIO, suppress
from .keys import jsonkeys
from .errors import RegExError, KeyNumError


REGEXES = {
    'unescaped_dot': r'(?<!\\)\.',
    'unescaped_colon': r'(?<!\\):',
    'number_range':  r'[-\d]+$',
    'regex_pattern': r'/.*/$'
}
RegEx = namedtuple('RegEx', REGEXES.keys())
REGEX = RegEx(*map(re.compile, REGEXES.values()))

ESCAPED_CHARS = '.:\\'

csv.register_dialect(
    'Keys',
    delimiter=',',
    strict=False,
    quoting=csv.QUOTE_MINIMAL,
    doublequote=False,
    escapechar='\\',
    skipinitialspace=True
)


def parse_csv(s, quotechar='"'):
    """Parse CSV values in string using specified dialect & quotechar."""
    return next(csv.reader(StringIO(s), 'Keys', quotechar=quotechar))


def is_index(token):
    """Is the token an index?"""
    return token.lstrip('.').isdigit()


def is_slice(token):
    """Is the token a slice?"""
    if ':' in token:
        indexes = REGEX.unescaped_colon.split(token, 2)
        return all(not i or is_index(i) for i in indexes)
    return False


def is_regex(token):
    """Is the token a regular expression pattern?"""
    return bool(REGEX.regex_pattern.match(token))


def parse_name(token):
    """Parse key name; return keylist."""
    for esc_ch in ESCAPED_CHARS:
        token = token.replace('\\' + esc_ch, esc_ch)
    return token


def parse_index(token):
    """Parse element number."""
    with suppress(ValueError):
        return int(token.lstrip('.'))


def parse_slice(token):
    """Parse slice syntax."""
    return slice(*map(parse_index, token.split(':')))


def parse_key(token):
    """Parse a key."""
    for key in REGEX.unescaped_dot.split(token):

        if is_index(key):
            # an integer
            yield parse_index(key)

        elif is_slice(key):
            # a slice object
            yield parse_slice(key)

        else:
            # a string
            yield parse_name(key)

        '''
        elif is_regex(key):
            # a RegEx pattern
            yield parse_regex(key)
        '''


def parse_number(token, items):
    """Parse key item number or range of numbers."""
    try:
        endpts = [parse_index(i) for i in token.split('-', 1)]
        if any(i for i in endpts if not (i is None or 0 < i <= len(items))):
            raise ValueError
    except ValueError:
        raise KeyNumError(token)
    if endpts[0] is not None:
        endpts[0] -= 1
    if len(endpts) == 1:
        endpts = (endpts[0], endpts[0] + 1)
    return [tuple(parse_key(i)) for i in items[slice(*endpts)]]


def parse_keys(tokens, keys=None):
    """Parse the key tokens."""
    for token in tokens:
        if REGEX.number_range.match(token):
            for keylist in parse_number(token, keys):
                yield keylist
        else:
            yield tuple(parse_key(token))


def parse_keylist(s, data=None, quotechar='"', keys=None):
    """Parse a CSV key list.

    The keys option is a preloaded list of keys; bypasses tree crawler.

    >>> parse_keylist('asteroids.0.name,asteroids.2:')
    [('asteroids', 0, 'name'), ('asteroids', slice(2, None))]

    result = parse_keylist('1-3,5', keys=['red', 'blu', 'grn', 'blk', 'yel'])
    >>> [('red',), ('blu',), ('grn',), ('yel',)]
    """
    tokens = parse_csv(s, quotechar)
    if any(REGEX.number_range.match(i) for i in tokens):
        if keys is None:
            keys = sorted(jsonkeys(data))
    return list(parse_keys(tokens, keys=keys))
