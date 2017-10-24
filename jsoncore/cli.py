import click
from click import argument, command, option, pass_context version_option


@command()
@argument('jsonfile', type=click.Path(readable=True), required=False)
@option('-r', '--root', help='Select a JSON branch to process')
@option('-l', '--list', 'list_', is_flag=True, help="List keys")
@option('-a', '--all', is_flag=True, help='List all keys; include arrays')
@option('-t', '--types', is_flag=True, help='List node types')
@option('-c', '--compact', is_flag=True, help='Compact the JSON output')
@option('-R', '--result', help='Select JSON branch to output after processing')
@version_option(prog_name='jsoncore')
@pass_context
def main(ctx, **kwds):
    ctx.color = False if kwds['nocolor'] else True


if __name__ == '__main__':
    main()
