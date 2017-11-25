import json
import sys

import click
import click._termui_impl


class JSONFile(click.File):
    name = 'JSON.load'

    def __init__(self, **kwds):
        super(JSONFile, self).__init__(**kwds)

    def convert(self, value, param, ctx):
        if value == '-' and click._termui_impl.isatty(sys.stdin):
            click.echo(ctx.get_usage())
            click.echo("Try `jsonclick --help' for more information.")
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


jsonfile = click.argument(
    'jsonfile', type=JSONFile(), default='-'
)
rootkey = click.option(
    '-r', '--root',
    help='Set the root of the JSON document before processing'
)
result = click.option(
    '-R', '--result',
    help='Select the result of the JSON document after processing'
)
