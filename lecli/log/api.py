"""
Log API module.
"""
import sys
import requests

from lecli import api_utils
from lecli import response_utils
from tabulate import tabulate

def _url():
    """
    Get rest query url of log resource id
    """
    return api_utils.get_management_url() + '/logs'


def print_logs(response):
    """
    Print logs.
    """
    data = response if isinstance(response, list) else [response]
    for item in data:
        if 'id' in item:
            print "ID: %s" % item['id']
        if 'name' in item:
            print "Name: %s" % item['name']
        if 'logsets_info' in item and item['logsets_info']:
            print "Logsets: %s" % tabulate(item['logsets_info'])
        if 'tokens' in item and item['tokens']:
            print "Tokens: %s" % item['tokens']
        if 'token_seed' in item:
            print "Token Seed: %s" % item['token_seed']
        if 'source_type' in item:
            print "Source Type: %s" % item['source_type']
        if 'structures' in item and item['structures']:
            print "Structures: %s" % item['structures']
        if 'user_data' in item:
            print "User Data: %s" % item['user_data']



def handle_get_log_response(response):
    """
    Handle get log response
    """
    if response_utils.response_error(response):
        sys.exit(1)
    elif response.status_code == 200:
        key_name = 'logs' if 'logs' in response.json() else 'log'
        print_logs(response.json()[key_name])


def get_logs():
    """
    Get logs associated with the user
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
    Get a specific log
    """
    headers = api_utils.generate_headers('ro')
    try:
        response = requests.get("/".join([_url(), log_id]), headers=headers)
        handle_get_log_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def create_log(logname, params):
    """Add a new log to the current account.
    If a JSON object is given, use that as the request parameters.
    Otherwise, use the name provided
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
            sys.stderr.write('Create log failed, status code: %d' % response.status_code)
            sys.exit(1)
        elif response.status_code == 201:
            print_logs(response.json()['log'])
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def delete_log(log_id):
    """
    Delete a log with the provided log ID
    """
    url = "/".join([_url(), log_id])
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.delete(url, headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Delete log failed, status code: %d' % response.status_code)
            sys.exit(1)
        elif response.status_code == 204:
            sys.stdout.write('Deleted log with id: %s \n' % log_id)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def replace_log(log_id, params):
    """
    Replace the given log with the details provided
    """
    url = "/".join([_url(), log_id])
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.put(url, json=params, headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Update log with details: %s failed with status code: %d' % params,
                             response.status_code)
            sys.exit(1)
        elif response.status_code == 200:
            sys.stdout.write('Log: %s updated to:\n' % log_id)
            print_logs(response.json()['log'])
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def rename_log(log_id, log_name):
    """
    Rename the given log with the provided name
    """
    url = "/".join([_url(), log_id])
    headers = api_utils.generate_headers('ro')

    try:
        response = requests.get(url, headers=headers)
        params = response.json()
        params['log']['name'] = log_name
        replace_log(log_id, params)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def update_log(log_id, params):
    """
    Update a log with the details provided
    """
    url = "/".join([_url(), log_id])
    headers = api_utils.generate_headers('ro')

    try:
        response = requests.get(url, headers=headers)
        existing_log = response.json()
        replace_log(log_id, api_utils.combine_objects(existing_log, params))
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)
