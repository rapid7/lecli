"""
Query API module.
"""
from __future__ import division

import sys
import json
import time
import datetime

import click
import requests
from termcolor import colored

from lecli import api_utils
from lecli import response_utils

ALL_EVENTS_QUERY = "where(/.*/)"


def _url(path):
    """
    Get rest query url of a specific path.
    """
    return 'https://rest.logentries.com/query/%s/' % path


def handle_response(response, progress_bar):
    """
    Handle response. Exit if it has any errors, continue if status code is 202, print response
    if status code is 200.
    """

    if response_utils.response_error(response) is True:  # Check response has no errors
        sys.exit(1)
    elif response.status_code == 200:
        progress = response.json().get('progress')
        if progress:
            progress_bar.update(progress)
        else:
            progress_bar.update(100)
            progress_bar.render_finish()
            print_response(response)
        if 'links' in response.json():
            next_url = response.json()['links'][0]['href']
            next_response = fetch_results(next_url)
            handle_response(next_response, progress_bar)
    elif response.status_code == 202:
        continue_request(response, progress_bar)


def continue_request(response, progress_bar):
    """
    Continue making request to the url in the response.
    """
    progress_bar.update(0)
    time.sleep(1)  # Wait for 1 second before hitting continue endpoint to prevent hitting API
    # limit
    if 'links' in response.json():
        continue_url = response.json()['links'][0]['href']
        new_response = fetch_results(continue_url)
        handle_response(new_response, progress_bar)


def fetch_results(provided_url):
    """
    Make the get request to the url and return the response.
    """
    try:
        response = requests.get(provided_url, headers=api_utils.generate_headers('rw'))
        return response
    except requests.exceptions.RequestException as error:
        click.echo(error)
        sys.exit(1)


def get_recent_events(log_keys, last_x_seconds=1200, time_range=None):
    """
    Get recent events belonging to provided log_keys in the last_x_seconds.
    """
    if time_range:
        leql = {"during": {"time_range": time_range}, "statement": ALL_EVENTS_QUERY}
    else:
        to_ts = int(time.time()) * 1000
        from_ts = (int(time.time()) - last_x_seconds) * 1000
        leql = {"during": {"from": from_ts, "to": to_ts}, "statement": ALL_EVENTS_QUERY}
    payload = {"logs": log_keys, "leql": leql}

    try:
        response = requests.post(_url('logs'), headers=api_utils.generate_headers('rw'),
                                 json=payload)
        with click.progressbar(length=100, label='Progress') as progress_bar:
            handle_response(response, progress_bar)
    except requests.exceptions.RequestException as error:
        click.echo(error)
        sys.exit(1)


def get_events(log_keys, time_from=None, time_to=None, date_from=None, date_to=None,
               time_range=None):
    """
    Get events belonging to log_keys and within the time range provided.
    """
    if date_from and date_to:
        from_ts = int(time.mktime(time.strptime(date_from, "%Y-%m-%d %H:%M:%S"))) * 1000
        to_ts = int(time.mktime(time.strptime(date_to, "%Y-%m-%d %H:%M:%S"))) * 1000
        leql = {"during": {"from": from_ts, "to": to_ts}, "statement": ALL_EVENTS_QUERY}
    elif time_to and time_from:
        from_ts = time_from * 1000
        to_ts = time_to * 1000
        leql = {"during": {"from": from_ts, "to": to_ts}, "statement": ALL_EVENTS_QUERY}
    else:
        leql = {"during": {"time_range": time_range}, "statement": ALL_EVENTS_QUERY}

    payload = {"logs": log_keys, "leql": leql}

    try:
        response = requests.post(_url('logs'), headers=api_utils.generate_headers('rw'),
                                 json=payload)
        with click.progressbar(length=100, label='Progress') as progress_bar:
            handle_response(response, progress_bar)
    except requests.exceptions.RequestException as error:
        click.echo(error)
        sys.exit(1)


def post_query(log_keys, query_string, time_from=None, time_to=None, date_from=None,
               date_to=None, time_range=None):
    """
    Post query to Logentries.
    """
    if date_from and date_to:
        from_ts = int(time.mktime(time.strptime(date_from, "%Y-%m-%d %H:%M:%S"))) * 1000
        to_ts = int(time.mktime(time.strptime(date_to, "%Y-%m-%d %H:%M:%S"))) * 1000
        leql = {"during": {"from": from_ts, "to": to_ts}, "statement": query_string}
    elif time_from and time_to:
        leql = {"during": {"from": time_from * 1000, "to": time_to * 1000},
                "statement": query_string}
    else:
        leql = {"during": {"time_range": time_range}, "statement": query_string}

    payload = {"logs": log_keys, "leql": leql}

    try:
        response = requests.post(_url('logs'), headers=api_utils.generate_headers('rw'),
                                 json=payload)
        with click.progressbar(length=100, label='Progress') as progress_bar:
            handle_response(response, progress_bar)
    except requests.exceptions.RequestException as error:
        click.echo(error)
        sys.exit(1)


def print_response(response):
    """
    Print response in a human readable way.
    """
    if 'events' in response.json():
        prettyprint_events(response)
    elif 'statistics' in response.json():
        prettyprint_statistics(response)


def prettyprint_events(response):
    """
    Print events in a human readable way.
    """
    data = response.json()
    for event in data['events']:
        time_value = datetime.datetime.fromtimestamp(event['timestamp'] / 1000)
        human_ts = time_value.strftime('%Y-%m-%d %H:%M:%S')
        try:
            message = json.loads(event['message'])
            click.echo(
                colored(str(human_ts), 'red') + '\t' +
                colored(json.dumps(message, indent=4, separators={':', ';'}), 'white'))
        except ValueError:
            click.echo(colored(str(human_ts), 'red') + '\t' + colored(event['message'], 'white'))


def prettyprint_statistics(response):
    """
    Print statistics in a human readable way.
    """
    data = response.json()

    # Extract keys
    time_from = data['statistics']['from']
    time_to = data['statistics']['to']

    # Handle timeseries
    if len(data['statistics']['timeseries']) != 0:
        # Extract keys
        stats_key = data['statistics']['stats'].keys()[0]
        stats_calc_value = data['statistics']['stats'].get(stats_key).values()
        total = stats_calc_value[0] if len(stats_calc_value) != 0 else 0
        click.echo('Total: %s' % total)

        click.echo('Timeseries: ')
        timeseries_key = data['statistics']['timeseries'].keys()[0]
        time_range = time_to - time_from
        num_timeseries_values = len(data['statistics']['timeseries'].get(timeseries_key))
        for index, value in enumerate(data['statistics']['timeseries'].get(timeseries_key)):
            timestamp = (time_from + (time_range / num_timeseries_values) * (index + 1)) / 1000
            time_value = datetime.datetime.fromtimestamp(timestamp)
            human_ts = time_value.strftime('%Y-%m-%d %H:%M:%S')
            click.echo(human_ts + ': ' + str(value.values()[0]))

    # Handle Groups
    elif len(data['statistics']['groups']) != 0:
        for group in data['statistics']['groups']:
            for key, value in group.iteritems():
                click.echo(str(key) + ':')
                for innerkey, innervalue in value.iteritems():
                    click.echo('\t' + str(innerkey) + ': ' + str(innervalue))

    else:
        click.echo(json.dumps(response.json(), indent=4, separators={':', ';'}))
