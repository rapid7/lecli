"""
Module for log commands
"""
import sys
import json
import click

from lecli.log import api

@click.command()
@click.option('-n', '--name', type=click.STRING, help="Name of new log")
@click.option('-f', '--filename', type=click.Path(exists=True, dir_okay=False),
              help="Full or relative path to file containing JSON log object")
def createlog(name, filename):
    """
    Create a log with the provided name and details.
    This method will use the JSON file first if both name and file are provided
    """
    if filename is not None:
        with open(filename) as json_data:
            try:
                params = json.load(json_data)
                api.create_log(None, params)
            except ValueError as error:
                sys.stderr.write(error.message + '\n')
                sys.exit(1)
    elif name is not None:
        api.create_log(name, None)
    else:
        click.echo('Example usage: lecli create log -n new_log_name')
        click.echo('Example usage: lecli create log -f path_to_file.json')


@click.command()
@click.argument('logid', type=click.STRING)
def deletelog(logid):
    """
    Delete a log with the provided id
    """
    api.delete_log(logid)


@click.command()
def getlogs():
    """
    Get all logs for this account
    """
    api.get_logs()


@click.command()
@click.argument('logid', type=click.STRING)
def getlog(logid):
    """
    Get a log with the given id
    """
    api.get_log(logid)


@click.command()
@click.argument('logid', type=click.STRING)
@click.argument('name', type=click.STRING)
def renamelog(logid, name):
    """
    Rename a log with the name provided
    """
    api.rename_log(logid, name)


@click.command()
@click.argument('logid', type=click.STRING)
@click.argument('filename', type=click.Path(exists=True, dir_okay=False))
def replacelog(logid, filename):
    """
    Replace a log of a given id with new details
    """
    with open(filename) as json_data:
        try:
            params = json.load(json_data)
            api.replace_log(logid, params)
        except ValueError as error:
            sys.stderr.write(error.message + '\n')
            sys.exit(1)


@click.command()
@click.argument('logid', type=click.STRING)
@click.argument('filename', type=click.Path(exists=True, dir_okay=False))
def updatelog(logid, filename):
    """
    Update a log of a given id with new details
    """
    with open(filename) as json_data:
        try:
            params = json.load(json_data)
            api.update_log(logid, params)
        except ValueError as error:
            sys.stderr.write(error.message + '\n')
            sys.exit(1)
