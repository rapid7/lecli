from __future__ import division
import json
import time

import datetime
import requests
from termcolor import colored

from lecli import apiutils


def _url(path):
    """
    Get rest query url of a specific path.
    """
    return 'https://rest.logentries.com/query/' + path + '/'


def response_error(response):
    """
    Check response if it has any errors.
    """
    if response.headers.get('X-RateLimit-Remaining') is not None:
        if int(response.headers['X-RateLimit-Remaining']) == 0:
            print 'Error: Rate Limit Reached, will reset in ' + response.headers.get(
                'X-RateLimit-Reset') + ' seconds'
            return True

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print "Request Error:", error.message
        return True

    if response.status_code == 200:
        if response.headers['Content-Type'] != 'application/json':
            print 'Unexpected Content Type Received in Response: ' + response.headers[
                'Content-Type']
            return True
        else:
            return False

    return False


def handle_response(response):
    """
    Handle response. Exit if it has any errors, continue if status code is 202, print response
    if status code is 200.
    """
    if response_error(response) is True:  # Check response has no errors
        exit(1)
    elif response.status_code == 200:
        print_response(response)
        if 'links' in response.json():
            next_url = response.json()['links'][0]['href']
            next_response = fetch_results(next_url)
            handle_response(next_response)
            return
        return
    elif response.status_code == 202:
        continue_request(response)
        return


def continue_request(response):
    """
    Continue making request to the url in the response.
    """
    time.sleep(1)  # Wait for 1 second before hitting continue endpoint to prevent hitting API limit
    if 'links' in response.json():
        continue_url = response.json()['links'][0]['href']
        new_response = fetch_results(continue_url)
        handle_response(new_response)


def fetch_results(provided_url):
    """
    Make the get request to the url and return the response.
    """
    try:
        response = requests.get(provided_url, headers=apiutils.generate_headers('rw'))
        return response
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def get_recent_events(log_keys, last_x_seconds=200):
    """
    Get recent events belonging to provided log_keys in the last_x_seconds.
    """
    to_ts = int(time.time()) * 1000
    from_ts = (int(time.time()) - last_x_seconds) * 1000

    leql = {"during": {"from": from_ts, "to": to_ts}, "statement": "where(/.*/)"}
    payload = {"logs": log_keys, "leql": leql}

    try:
        response = requests.post(_url('logs'), headers=apiutils.generate_headers('rw'),
                                 json=payload)
        handle_response(response)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def get_events(log_keys, time_from=None, time_to=None, date_from=None, date_to=None):
    """
    Get events belonging to log_keys and within the time range provided.
    """
    if date_from is not None and date_to is not None:
        from_ts = int(time.mktime(time.strptime(date_from, "%Y-%m-%d %H:%M:%S"))) * 1000
        to_ts = int(time.mktime(time.strptime(date_to, "%Y-%m-%d %H:%M:%S"))) * 1000
    else:
        from_ts = time_from * 1000
        to_ts = time_to * 1000

    leql = {"during": {"from": from_ts, "to": to_ts}, "statement": "where(/.*/)"}
    payload = {"logs": log_keys, "leql": leql}

    try:
        response = requests.post(_url('logs'), headers=apiutils.generate_headers('rw'),
                                 json=payload)
        handle_response(response)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def post_query(log_keys, query_string, time_from=None, time_to=None, date_from=None, date_to=None):
    """
    Post query to Logentries.
    """
    if date_from is not None and date_to is not None:
        from_ts = int(time.mktime(time.strptime(date_from, "%Y-%m-%d %H:%M:%S"))) * 1000
        to_ts = int(time.mktime(time.strptime(date_to, "%Y-%m-%d %H:%M:%S"))) * 1000
    else:
        from_ts = time_from * 1000
        to_ts = time_to * 1000

    leql = {"during": {"from": from_ts, "to": to_ts}, "statement": query_string}
    payload = {"logs": log_keys, "leql": leql}

    try:
        response = requests.post(_url('logs'), headers=apiutils.generate_headers('rw'),
                                 json=payload)
        handle_response(response)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


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
        print event['timestamp'] / 1000
        time_value = datetime.datetime.fromtimestamp(event['timestamp'] / 1000)
        human_ts = time_value.strftime('%Y-%m-%d %H:%M:%S')
        print colored(str(human_ts), 'red') + '\t' + colored(event['message'], 'white')


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
        timeseries_key = data['statistics']['timeseries'].keys()[0]
        stats_key = data['statistics']['stats'].keys()[0]
        num_timeseries_values = len(data['statistics']['timeseries'].get(timeseries_key))
        stats_calc_key = data['statistics']['stats'].get(stats_key).keys()[0]
        total = data['statistics']['stats'].get(stats_key).get(stats_calc_key)
        time_range = time_to - time_from

        print 'Total' + ': ' + str(total)

        print 'Timeseries: '
        for index, value in enumerate(data['statistics']['timeseries'].get(timeseries_key)):
            timestamp = (time_from + (time_range / num_timeseries_values) * (index + 1)) / 1000
            time_value = datetime.datetime.fromtimestamp(timestamp)
            human_ts = time_value.strftime('%Y-%m-%d %H:%M:%S')
            print human_ts + ': ' + str(value.values()[0])

    # Handle Groups
    elif len(data['statistics']['groups']) != 0:
        for group in data['statistics']['groups']:
            for key, value in group.iteritems():
                print str(key) + ':'
                for innerkey, innervalue in value.iteritems():
                    print '\t' + str(innerkey) + ': ' + str(innervalue)

    else:
        print json.dumps(response.json(), indent=4, separators={':', ';'})
