"""
Module for saved query commands
"""
import click

from lecli.saved_query import saved_query_api


@click.command()
def get_saved_queries():
    """Get a list of saved queries"""
    saved_query_api.get_saved_query()


@click.command()
@click.argument('queryid', type=click.STRING, default=None)
def get_saved_query(queryid):
    """Get the saved query with the given ID"""
    saved_query_api.get_saved_query(queryid)


@click.command()
@click.argument('name', type=click.STRING)
@click.argument('statement', type=click.STRING)
@click.option('-f', '--timefrom', help='Time to query from (unix epoch)', type=int)
@click.option('-t', '--timeto', help='Time to query to (unix epoch)', type=int)
@click.option('-r', '--relative_range', help='Relative time range (ex: last x :timeunit)',
              type=click.STRING)
@click.option('-l', '--logs', help='Logs(colon delimited if multiple)', type=click.STRING)
def create_saved_query(name, statement, timefrom, timeto, relative_range, logs):
    """Create a saved query with the given arguments"""
    saved_query_api.create_saved_query(name, statement, timefrom, timeto, relative_range, logs)


@click.command()
@click.argument('query_id', type=click.STRING)
@click.option('-n', '--name', help='Name of the saved query', type=click.STRING)
@click.option('-s', '--statement', help='LEQL statement', type=click.STRING)
@click.option('-f', '--timefrom', help='Time to query from (unix epoch)', type=int)
@click.option('-t', '--timeto', help='Time to query to (unix epoch)', type=int)
@click.option('-r', '--relative_range', help='Relative time range (ex: last x :timeunit)',
              type=click.STRING)
@click.option('-l', '--logs', help='Logs(colon delimited if multiple)', type=click.STRING)
def update_saved_query(query_id, name, statement, timefrom, timeto, relative_range, logs):
    """Update the saved query with the given arguments"""
    saved_query_api.update_saved_query(query_id, name, statement, timefrom, timeto, relative_range,
                                       logs)


@click.command()
@click.argument('query_id', type=click.STRING)
def delete_saved_query(query_id):
    """Delete the saved query with given ID"""
    saved_query_api.delete_saved_query(query_id)
