import click
from click import argument, option

@click.command()
@argument('jsonfile', type=click.Path(readable=True), required=False)
@option('-r', '--root', 'rootkey', help='Set the root of the JSON document')
@option('-l', '--list', 'listkeys', is_flag=True,
        help='numbered JSON keys list')
@option('-i', '--inspect', is_flag=True,
        help='inspect JSON document; all keys, indexes & types')
@option('-C', '--compact', is_flag=True,
        help='compact JSON')
@option('-n', '--nocolor', is_flag=True, help='disable syntax highlighting')
@version_option(prog_name='jsoncore')
@click.pass_context
def main(ctx, **kwds):
    ctx.color = False if kwds['nocolor'] else True

if __name__ == '__main__':
    main()
