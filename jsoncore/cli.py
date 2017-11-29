import json
import sys

import click
import click._termui_impl

from .core import get_value
from .parse import parse_keys


class JSONFile(click.File):
    name = 'JSON.load'

    def __init__(self, **kwds):
        super(JSONFile, self).__init__(**kwds)

    def convert(self, value, param, ctx):
        if value == '-' and click._termui_impl.isatty(sys.stdin):
            click.echo(ctx.get_usage())
            help_mesg = "Try `{cmd_name} --help' for more information."
            click.echo(help_mesg.format(cmd_name=ctx.command.name))
            return
        f = super(JSONFile, self).convert(value, param, ctx)
        try:
            return json.load(f)
        except (json.JSONDecodeError, TypeError) as e:
            self.fail('%s does not contain valid JSON: %s' % (
                click._compat.filename_to_ui(value),
                click._compat.get_streerror(e),
            ), param, ctx)
        except UnicodeError as e:
            self.fail('%s: %s' % (
                click._compat.filename_to_ui(value),
                click._compat.get_streerror(e)
            ), param, ctx)
        return


def get_root(ctx, param, value):
    data = ctx.params.get('jsonfile')
    if data and value:
        keys = [tuple(i) for i in parse_keys(value, keys=get_keys(data))]
        if keys:
            return get_value(keys[0], data)
    return data


jsonfile = argument(
    'jsonfile', type=JSONFile(), default='-', is_eager=True
)
optional_jsonfile = argument(
    'jsonfile', type=JSONFile(), default='-', required=False, is_eager=True
)
rootkey = option(
    '-r', '--root', callback=get_root, help='Set the root of the JSON document'
)
result = click.option(
    '-R', '--result',
    help='Select the result of the JSON document after processing'
)
