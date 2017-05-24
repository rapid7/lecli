"""
Logset API module.
"""
import json
import sys

import requests

from lecli import api_utils
from lecli import response_utils


def _url(provided_path_parts=()):
    """
    Get rest query url of logset resource id.
    """
    ordered_path_parts = ['management', 'logsets']
    ordered_path_parts.extend(provided_path_parts)
    return api_utils.build_url(ordered_path_parts)


def handle_response(response, error_message, success_code, success_message=None):
    """Handle logset responses"""
    if response_utils.response_error(response):
        sys.stderr.write(error_message)
        sys.exit(1)
    elif response.status_code == success_code:
        if success_message:
            sys.stdout.write(success_message)
        else:
            api_utils.pretty_print_string_as_json(response.text)


def get_logsets():
    """
    Get all logsets
    """
    headers = api_utils.generate_headers('ro')
    try:
        response = requests.request('GET', _url()[1], headers=headers)
        handle_response(response, 'Unable to fetch logsets\n', 200)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def get_logset(logset_id):
    """
    Get the logset with the given id
    """
    headers = api_utils.generate_headers('ro')
    try:
        response = requests.get(_url((logset_id,))[1], headers=headers)
        handle_response(response, 'Unable to fetch logset %s \n' % logset_id, 200)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def create_logset(logset_name=None, params=None):
    """
    Add a new logset to the current account.
    If a filename is given, load the contents of the file
    as json parameters for the request.
    If a name is given, create a new logset with the given name
    """
    if params is not None:
        request_params = params
    else:
        request_params = {
            'logset': {
                'name': logset_name
            }
        }

    headers = api_utils.generate_headers('rw')

    try:
        response = requests.post(_url()[1], json=request_params, headers=headers)
        handle_response(response, 'Creating logset failed.\n', 201)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def delete_logset(logset_id):
    """
    Delete the logset with the given id
    """
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.delete(_url((logset_id,))[1], headers=headers)
        handle_response(response, 'Delete logset failed.\n', 204,
                        'Deleted logset with id: %s \n' % logset_id)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def rename_logset(logset_id, logset_name):
    """
    Rename a given logset
    """
    headers = api_utils.generate_headers('ro')

    try:
        response = requests.get(_url((logset_id,))[1], headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Rename logset failed.\n')
            sys.exit(1)
        elif response.status_code == 200:
            params = response.json()
            params['logset']['name'] = logset_name
            replace_logset(logset_id, params)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def replace_logset(logset_id, params):
    """
    Replace a given logset with the details provided
    """
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.put(_url((logset_id,))[1], json=params, headers=headers)
        handle_response(response, 'Update logset with details %s failed.\n' % params, 200)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def add_log(logset_id, log_id):
    """
    Add a log to the logset
    """
    params = {
        "logset":{
            "logs_info": [{
                "id": str(log_id)
            }]
        }
    }
    headers = api_utils.generate_headers('ro')

    try:
        response = requests.get(_url((logset_id,))[1], headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Add log %s to logset %s failed\n'
                             % (log_id, logset_id))
            sys.exit(1)
        elif response.status_code == 200:
            existing_logset = response.json()
            replace_logset(logset_id, api_utils.combine_objects(existing_logset, params))
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def extract_log_from_logset(logset, log_id):
    """Helper method to remove a given log from a logset"""
    pruned_logset = []
    if 'logs_info' in logset['logset']:
        for log in logset['logset']['logs_info']:
            if log['id'] != log_id:
                pruned_logset.append(log)

    if pruned_logset is not []:
        logset['logset']['logs_info'] = pruned_logset
        return logset
    else:
        sys.stderr.write("Log %s does not exist in logset ", (log_id))
        sys.exit(1)


def delete_log(logset_id, log_id):
    """
    Delete a log from the logset
    """
    headers = api_utils.generate_headers('ro')
    try:
        response = requests.get(_url((logset_id,))[1], headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Delete log %s from logset %s failed\n'
                             % (log_id, logset_id))
            sys.exit(1)
        elif response.status_code == 200:
            existing_logset = response.json()
            params = extract_log_from_logset(existing_logset, log_id)
            replace_logset(logset_id, params)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def replace_logset_from_file(logset_id, filename):
    """Helper method to load file contents as json
        in order to call replace"""
    with open(filename) as json_data:
        try:
            params = json.load(json_data)
            replace_logset(logset_id, params)
        except ValueError as error:
            sys.stderr.write(error.message + '\n')
            sys.exit(1)
