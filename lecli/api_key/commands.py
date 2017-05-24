"""
Api Keys commands module.
"""
import json
import sys

import click

from lecli.api_key import api


@click.command()
@click.argument('api_key', type=click.STRING)
def get_api_key(api_key):
    """
    Get a specific api key
    """
    api.get(api_key)


@click.command()
@click.option('--owner/--no-owner', default=False)
def get_api_keys(owner):
    """
    Get all api keys
    """
    api.get_all(owner)


@click.command()
@click.argument('filename', type=click.Path(exists=True, dir_okay=False))
def create_api_key(filename):
    """
    Create an api key with the provided file.
    """
    if filename is not None:
        with open(filename) as json_data:
            try:
                params = json.load(json_data)
            except ValueError as error:
                sys.stderr.write(error.message + '\n')
                sys.exit(1)

            api.create(params)
    else:
        click.echo('Example usage: lecli create apikey path_to_file.json')


@click.command()
@click.argument('api_key', type=click.STRING)
def delete_api_key(api_key):
    """
    Delete a specific api key
    """
    api.delete(api_key)


@click.command()
@click.argument('api_key', type=click.STRING)
@click.option('--enable/--disable', default=None)
def update_api_key(api_key, enable):
    """
    Enable or disable an api key
    """
    if enable is not None:
        api.update(api_key, enable)
    else:
        click.echo("Example usage: lecli update apikey 12345678-aaaa-bbbb-1234-1234cb123456 "
                   "--enable")
        click.echo("Example usage: lecli update apikey 12345678-aaaa-bbbb-1234-1234cb123456 "
                   "--disable")
