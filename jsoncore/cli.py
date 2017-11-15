import json
import sys

import click
import click._termui_impl


class JSONFile(click.File):
    name = 'JSON.load'

    def __init__(self, **kwds):
        super(JSONFile, self).__init__(**kwds)

    def convert(self, value, param, ctx):
        f = super(JSONFile, self).convert(value, param, ctx)
        if click._termui_impl.isatty(sys.stdin):
            click.echo(ctx.get_usage())
            click.echo("Try `jsonclick --help' for more information.")
            return ''
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
        return ''
