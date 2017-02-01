"""
Module for usage commands
"""
import click

from lecli.usage import api


@click.command()
@click.option('-s', '--start', type=click.STRING, default=None)
@click.option('-e', '--end', type=click.STRING, default=None)
def get_usage(start, end):
    """Get account's usage information"""
    if all([start, end]):
        api.get_usage(start, end)
    else:
        click.echo("Example usage: lecli get usage -s '2016-01-01' -e '2016-06-01'")
        click.echo("Note: Start and end dates should be in ISO-8601 format: YYYY-MM-DD")
