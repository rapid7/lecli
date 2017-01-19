"""
Log API module.
"""
import sys
import json
import requests

from lecli import api_utils
from lecli import response_utils

def _url():
    """
    Get rest query url of log resource id.
    """
    return api_utils.get_management_url()


def handle_get_log_response(response):
    """
    Handle get log response.
    """
    if response_utils.response_error(response):
        sys.exit(1)
    elif response.status_code == 200:
        key_name = 'logs' if 'logs' in response.json() else 'log'
        print json.dumps(response.json()[key_name], indent=4, sort_keys=True)


def get_logs():
    """
    Get logs associated with the user.
    """
    headers = api_utils.generate_headers('ro')
    try:
        response = requests.request('GET', _url(), headers=headers)
        handle_get_log_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def get_log(log_id):
    """
    Get a specific log.
    """
    headers = api_utils.generate_headers('ro')
    try:
        response = requests.get(_url() + "/" + str(log_id),
                                headers=headers)
        handle_get_log_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def create_log(logname, params):
    """
    Add a new log to the current account.
    If a filename is given, load the contents of the file
    as json parameters for the request.
    If a name is given, create a new log with the given name
    """

    if params is not None:
        request_params = params
    else:
        request_params = {
            'log': {
                'name': logname
            }
        }

    headers = api_utils.generate_headers('rw')

    try:
        response = requests.post(_url(), json=request_params, headers=headers)
        if response_utils.response_error(response):
            print 'Creating log failed, status code: %d' % response.status_code
            sys.exit(1)
        elif response.status_code == 201:
            pretty_print_string_as_json(response.text)

    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def delete_log(log_id):
    """
    Delete a log with the provided log ID.
    """
    url = _url() + '/' + log_id
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.delete(url, headers=headers)
        if response_utils.response_error(response):
            print 'Delete log failed, status code: %d' % response.status_code
            sys.exit(1)
        elif response.status_code == 204:
            print 'Deleted log with id: %s' % log_id
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def patch_log(log_id, url, headers, params):
    """Makes a HTTP PATCH call with the given details"""
    try:
        response = requests.patch(url, json=params, headers=headers)
        if response_utils.response_error(response):
            print 'Updating log with details: %s failed, status code: %d' \
                  % (params, response.status_code)
            sys.exit(1)
        elif response.status_code == 200:
            print "Log: '%s' updated to: %s"  % (log_id, params)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def rename_log(log_id, log_name):
    """
    Update the given log with the name provided
    """
    url = "/".join([_url(), log_id])

    params = {
        'log': {
            'name': log_name
        }
    }

    headers = api_utils.generate_headers('rw')

    patch_log(log_id, url, headers, params)


def update_log(log_id, params):
    """
    Update the given log with the given details
    """
    url = _url() + '/' + str(log_id)

    headers = api_utils.generate_headers('rw')

    patch_log(log_id, url, headers, params)

def replace_log(log_id, params):
    """
       Replace a log with a new log as provided
    """
    url = _url() + '/' + str(log_id)

    headers = api_utils.generate_headers('rw')

    try:
        response = requests.put(url, json=params, headers=headers)
        if response_utils.response_error(response):  # Check response has no errors
            print 'Replacing log with details: %s failed, status code: %d' \
                  % (params, response.status_code)
            sys.exit(1)
        elif response.status_code == 200:
            print "Log: '%s' replaced with: %s" % (log_id, params)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)

def pretty_print_string_as_json(text):
    """
    Pretty prints a json string
    """
    print json.dumps(json.loads(text), indent=4, sort_keys=True)
