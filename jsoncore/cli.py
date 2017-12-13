import click

from .core import get_keys, get_value
from .parse import parse_keys

from jsoncat import JSONFile


def get_root(ctx, param, value):
    data = ctx.params.get('jsonfile')
    if data and value:
        keys = [tuple(i) for i in parse_keys(value, keys=get_keys(data))]
        if keys:
            return get_value(keys[0], data)
    return data


jsonfile = click.argument(
    'jsonfile', type=JSONFile(), default='-'
)
optional_jsonfile = click.argument(
    'jsonfile', type=JSONFile(), required=False
)
rootkey = click.option(
    '-r', '--root', callback=get_root, help='Set the root of the JSON document'
)
result = click.option(
    '-R', '--result',
    help='Select the result of the JSON document after processing'
)
