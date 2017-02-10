"""
Logset commands module
"""
import sys
import json
import click

from lecli.logset import api


@click.command()
@click.option('-n', '--name', type=click.STRING, help="Name of new log")
@click.option('-f', '--filename', type=click.Path(exists=True, dir_okay=False),
              help="Full or relative path to file containing JSON log object")
def createlogset(name=None, filename=None):
    """
    Create a logset with the provided name and details.
    This method will use the JSON file first if both name and file are provided
    """
    if filename is not None:
        with open(filename) as json_data:
            try:
                params = json.load(json_data)
                api.create_logset(None, params)
            except ValueError as error:
                sys.stderr.write(error.message + '\n')
                sys.exit(1)
    elif name is not None:
        api.create_logset(name, None)
    else:
        click.echo('Example usage: lecli create logset -n new_log_name')
        click.echo('Example usage: lecli create logset -f path_to_file.json')


@click.command()
def getlogsets():
    """
    Get all logsets for this account
    """
    api.get_logsets()


@click.command()
@click.argument('logset_id', type=click.STRING)
def getlogset(logset_id):
    """
    Get a logset with the provided ID
    """
    api.get_logset(logset_id)


@click.command()
@click.argument('logset_id', type=click.STRING)
@click.argument('new_name', type=click.STRING)
def renamelogset(logset_id, new_name):
    """
    Rename a given logset with the name provided
    """
    api.rename_logset(logset_id, new_name)


@click.command(help='Available commands are:\n\t"delete_log"\n\t"add_log"')
@click.argument('command', type=click.STRING, default=None)
@click.argument('logset_id', type=click.STRING, default=None)
@click.argument('log_id', type=click.STRING, default=None)
def updatelogset(command, logset_id, log_id):
    """Update a logset by adding or deleting a log."""
    if command == 'add_log':
        api.add_log(logset_id, log_id)
    elif command == 'delete_log':
        api.delete_log(logset_id, log_id)


@click.command()
@click.argument('logset_id', type=click.STRING)
def deletelogset(logset_id):
    """
    Delete a logset
    """
    api.delete_logset(logset_id)

@click.command()
@click.argument('logset_id', type=click.STRING)
@click.argument('filename', type=click.Path(exists=True, dir_okay=False))
def replacelogset(logset_id, filename):
    """
    Replace a logset of a given id with new details
    """
    api.replace_logset_from_file(logset_id, filename)
