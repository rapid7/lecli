"""
Query API module.
"""
from __future__ import division

import json
import sys
import time
import datetime

import click
import requests
from termcolor import colored

from lecli import api_utils
from lecli import response_utils

ALL_EVENTS_QUERY = "where(/.*/)"


def _url(provided_path_parts=()):
    """
    Get rest query url of a specific path.
    """
    ordered_path_parts = ['query']
    ordered_path_parts.extend(provided_path_parts)
    return api_utils.build_url(ordered_path_parts)


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


def handle_tail(response, poll_interval, poll_iteration=1000):
    """
    handle tailing loop
    """
    for _ in range(poll_iteration):
        if response_utils.response_error(response):
            sys.exit(1)
        elif response.status_code == 200:
            print_response(response)

        # fetch results from the next link
        if 'links' in response.json():
            next_url = response.json()['links'][0]['href']
            time.sleep(poll_interval)
            response = fetch_results(next_url)
        else:
            click.echo('No continue link found in the received response.', err=True)


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


def fetch_results(provided_url, params=None):
    """
    Make the get request to the url and return the response.
    """
    try:
        response = requests.get(provided_url, headers=api_utils.generate_headers('rw'),
                                params=params)
        return response
    except requests.exceptions.RequestException as error:
        click.echo(error, err=True)
        sys.exit(1)


def validate_query(**kwargs):
    """
    Validate query options
    """
    date_from = kwargs.get('date_from')
    time_from = kwargs.get('time_from')
    relative_time_range = kwargs.get('relative_time_range')
    saved_query_id = kwargs.get('saved_query_id')
    query_string = kwargs.get('query_string')
    log_keys = kwargs.get('log_keys')
    querynick = kwargs.get('querynick')
    lognick = kwargs.get('lognick')
    loggroup = kwargs.get('loggroup')

    valid = True
    if all([any([lognick, loggroup]), log_keys]):
        valid = False
        click.echo('Cannot define lognicks or loggroups and logkeys together in the same query '
                   'request.', err=True)
    if all([time_from, date_from]):
        valid = False
        click.echo('Cannot define start time(epoch) and start date(ISO-8601) in the same query '
                   'request.', err=True)
    if all([saved_query_id, any([querynick, query_string]), query_string != ALL_EVENTS_QUERY]):
        valid = False
        click.echo('Cannot define saved query and LEQL/query nickname in the same query request.',
                   err=True)
    if all([query_string, querynick]):
        valid = False
        click.echo('Cannot define a LEQL query and query nickname in the same query request.',
                   err=True)
    if all([lognick, loggroup]):
        valid = False
        click.echo('Cannot define a log nickname and a log group in the same query request.',
                   err=True)
    if all([relative_time_range, any([time_from, date_from])]):
        valid = False
        click.echo('Cannot define relative time range and start time/date in the same query '
                   'request.', err=True)
    if not any([log_keys, lognick, loggroup, saved_query_id]):
        valid = False
        click.echo('Either of log keys, log nick, log group or saved query must be supplied.',
                   err=True)
    if not any([time_from, date_from, relative_time_range, saved_query_id]):
        valid = False
        click.echo('Either of start time, start date or relative time range must be supplied.',
                   err=True)
    return valid


def query(**kwargs):
    """
    Post query to Logentries.
    """
    date_from = kwargs.get('date_from')
    date_to = kwargs.get('date_to')
    time_from = kwargs.get('time_from')
    time_to = kwargs.get('time_to')
    relative_time_range = kwargs.get('relative_time_range')
    saved_query_id = kwargs.get('saved_query_id')
    query_string = kwargs.get('query_string')
    log_keys = kwargs.get('log_keys')
    querynick = kwargs.get('querynick')
    lognick = kwargs.get('lognick')
    loggroup = kwargs.get('loggroup')
    if not validate_query(date_from=date_from, time_from=time_from, query_string=query_string,
                          relative_time_range=relative_time_range, saved_query_id=saved_query_id,
                          log_keys=log_keys, querynick=querynick, lognick=lognick,
                          loggroup=loggroup):
        return False

    time_range = prepare_time_range(time_from, time_to, relative_time_range, date_from, date_to)
    if querynick:
        query_string = api_utils.get_named_query(querynick)

    if lognick:
        log_keys = api_utils.get_named_logkey(lognick)
    if loggroup:
        log_keys = api_utils.get_named_logkey_group(loggroup)

    try:
        if saved_query_id:
            response = run_saved_query(saved_query_id, time_range, log_keys)
        else:
            response = post_query(log_keys, query_string, time_range)
        with click.progressbar(length=100, label='Progress\t') as progress_bar:
            handle_response(response, progress_bar)
        return True
    except requests.exceptions.RequestException as error:
        click.echo(error)
        sys.exit(1)


def post_query(log_keys, query_string, time_range):
    """
    POST a request to Rest Query API

    :param log_keys: list of log keys
    :param query_string: leql query statement
    :param time_range: time range including either relative time range or start and end times
    :return: response
    """
    payload = {"logs": log_keys, "leql": {"statement": query_string, "during": time_range}}
    response = requests.post(_url(('logs',))[1], headers=api_utils.generate_headers('rw'),
                             json=payload)
    return response


def prepare_time_range(time_from, time_to, relative_time_range, date_from=None, date_to=None):
    """
    Prepare time range based on given options. Options are validated in advance.
    """
    if relative_time_range:
        return {"time_range": relative_time_range}
    elif time_from and time_to:
        return {"from": int(time_from) * 1000, "to": int(time_to) * 1000}
    elif date_from and date_to:
        from_ts = int(time.mktime(time.strptime(date_from, "%Y-%m-%d %H:%M:%S"))) * 1000
        to_ts = int(time.mktime(time.strptime(date_to, "%Y-%m-%d %H:%M:%S"))) * 1000
        return {"from": from_ts, "to": to_ts}


def tail_logs(logkeys, leql, poll_interval, lognick=None, loggroup=None, saved_query_id=None):
    """
    Tail given logs
    """
    if lognick:
        logkeys = api_utils.get_named_logkey(lognick)
    elif loggroup:
        logkeys = api_utils.get_named_logkey_group(loggroup)

    if saved_query_id:
        if logkeys:
            url = _url(('live', 'logs', ':'.join(logkeys), str(saved_query_id)))[1]
        else:
            url = _url(('live', 'saved_query', str(saved_query_id)))[1]
    else:
        url = _url(('live', 'logs'))[1]
    try:
        if saved_query_id:
            response = requests.get(url, headers=api_utils.generate_headers('rw'))
        else:
            payload = {'logs': logkeys}
            if leql:
                payload.update({'leql': {'statement': leql}})

            response = requests.post(url, headers=api_utils.generate_headers('rw'), json=payload)
        handle_tail(response, poll_interval)
        return True
    except requests.exceptions.RequestException as error:
        click.echo(error, err=True)
        sys.exit(1)


def run_saved_query(saved_query_id, params, log_keys):
    """
    Run the given saved query
    """
    if log_keys:
        url = _url(('logs', ':'.join(log_keys), str(saved_query_id)))[1]
    else:
        url = _url(('saved_query', str(saved_query_id)))[1]

    return fetch_results(url, params)


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
