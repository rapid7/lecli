"""
Saved Query API module.
"""
import sys
import click
import requests

from lecli import api_utils
from lecli import response_utils


def _url():
    """
    Get rest query url of account resource id.
    """
    return 'https://rest.logentries.com/query/saved_queries'


def _pretty_print_saved_query(query):
    """
    Pretty print saved query object
    :param query:
    """
    click.echo("Name: \t%s" % query['name'])
    click.echo("Logs: \t%s" % ",".join(query['logs']))
    click.echo("ID: \t%s" % query['id'])
    click.echo("LEQL \tStatement: \t%s" % query['leql']['statement'])
    click.echo("\tTime range: \t%s" % query['leql']['during'].get('time_range'))
    click.echo("\tFrom: \t\t%s" % query['leql']['during'].get('from'))
    click.echo("\tTo: \t\t%s" % query['leql']['during'].get('to'))
    click.echo("**********************************************")


def _pretty_print_saved_query_error(response):
    """
    Pretty print saved query error
    """
    try:
        error_body = response.json()
        if 'fields' in error_body:
            click.echo('Invalid field: %s' % ",".join(response.json()['fields']))
        if 'messages' in error_body:
            click.echo('Message: %s' % ",".join(response.json()['messages']))
    except ValueError:
        sys.exit(1)


def _handle_saved_query_response(response):
    """
    Handle saved query response, check whether there are multiple entities in the response or not
    :param response:
    """
    if response.json().get('saved_queries'):
        queries = response.json()['saved_queries']
        for query in queries:
            _pretty_print_saved_query(query)
    elif response.json().get('saved_query'):
        query = response.json()['saved_query']
        _pretty_print_saved_query(query)


def get_saved_query(query_id=None):
    """
    If query id is provided, get this specific saved query or get them all
    :param query_id: uuid of saved query to be retrieved(optional)
    """
    endpoint_url = _url()
    if query_id:
        endpoint_url = _url() + "/" + query_id
    headers = api_utils.generate_headers('rw')
    try:
        response = requests.get(endpoint_url, headers=headers)
        if response_utils.response_error(response):
            if query_id:
                sys.stderr.write("Unable to retrieve saved query with id %s" % query_id)
            else:
                sys.stderr.write("Unable to retrieve saved queries.")
        elif response.status_code == 200:
            _handle_saved_query_response(response)
    except requests.exceptions.RequestException as error:
        click.echo(error)
        sys.exit(1)


def delete_saved_query(query_id):
    """
    Delete a specific saved query
    :param query_id: uuid of saved query to be deleted
    """
    headers = api_utils.generate_headers('rw')
    try:
        response = requests.delete(_url() + "/" + query_id, headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Delete saved query failed, status code: %d' % response.status_code)
        elif response.status_code == 204:
            click.echo('Deleted saved query with id: %s' % query_id)
    except requests.exceptions.RequestException as error:
        click.echo(error)
        sys.exit(1)


def create_saved_query(name, statement, from_ts=None, to_ts=None, time_range=None, logs=None):
    """
    Create a new saved query with the provided fields.
    :param name: name of the saved query (mandatory)
    :param statement: leql statement of the query (mandatory)
    :param from_ts: 'from' timestamp of query - unix epoch timestamp (optional)
    :param to_ts: 'to' timestamp of query - unix epoch timestamp (optional)
    :param time_range: time range of query - cannot be defimed with 'from' and/or 'to' fields(
    optional)
    :param logs: list of logs of the saved query, colon(:) separated uuids.
    """
    headers = api_utils.generate_headers('rw')
    params = {
        'saved_query': {
            'name': name,
            'leql': {
                'statement': statement,
                'during': {
                    'from': from_ts,
                    'to': to_ts,
                    'time_range': time_range
                }
            },
            'logs': logs.split(':') if logs else []
        }
    }

    try:
        response = requests.post(_url(), json=params, headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Creating saved query failed, status code: %d' % response.status_code)
            _pretty_print_saved_query_error(response)
        elif response.status_code == 201:
            click.echo('Saved query created with name: %s' % name)
            _pretty_print_saved_query(response.json()['saved_query'])
    except requests.exceptions.RequestException as error:
        click.echo(error)
        sys.exit(1)


def update_saved_query(query_id, name=None, statement=None, from_ts=None, to_ts=None,
                       time_range=None, logs=None):
    """
    Update a saved query with the given parameters.
    :param query_id: id of the saved query to be updated
    :param name: new name of the saved query
    :param statement: new leql statement of the saved query
    :param from_ts: new 'from' timestamp of the saved query
    :param to_ts: new 'to' timestamp of the saved query
    :param time_range: new time range of the saved query
    :param logs: colon(:) separated list of logs of the saved query
    """
    headers = api_utils.generate_headers('rw')
    params = {
        'saved_query': {
        }
    }

    if name:
        params['saved_query']['name'] = name

    if logs:
        params['saved_query']['logs'] = logs.split(':')

    if any([statement, from_ts, to_ts, time_range]):
        leql = {}
        if statement:
            leql['statement'] = statement
        if any([from_ts, to_ts, time_range]):
            during = {}
            if from_ts:
                during.update({'from': from_ts, 'to': None, 'time_range': None})
            if to_ts:
                during.update({'to': to_ts, 'time_range': None})
            if time_range:
                during.update({'time_range': time_range, 'from': None, 'to': None})
            leql['during'] = during
        params['saved_query']['leql'] = leql

    try:
        response = requests.patch(_url() + "/" + query_id, json=params, headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Updating saved query failed, status code: %d' % response.status_code)
            _pretty_print_saved_query_error(response)
        elif response.status_code == 200:
            click.echo('Saved query with id %s updated.' % query_id)
            _pretty_print_saved_query(response.json()['saved_query'])
    except requests.exceptions.RequestException as error:
        click.echo(error)
        sys.exit(1)
