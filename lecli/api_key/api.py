"""
Api Keys API module.
"""
import json
import sys

import requests

from lecli import api_utils
from lecli import response_utils


def _url(provided_parts=()):
    """
    Get rest query "path" and "url" respectively
    """
    ordered_path_parts = ['management', 'accounts', api_utils.get_account_resource_id(), 'apikeys']
    ordered_path_parts.extend(provided_parts)
    return api_utils.build_url(ordered_path_parts)


def handle_api_key_response(response):
    """
    Handle get api key response
    """
    if response_utils.response_error(response):
        sys.exit(1)
    elif response.status_code in [200, 201]:
        api_utils.pretty_print_string_as_json(response.text)


def delete(api_key_id):
    """
    Delete an api key with the provided ID
    """
    action, url = _url((api_key_id,))
    headers = api_utils.generate_headers('owner', method='DELETE', body='', action=action)

    try:
        response = requests.delete(url, headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Deleting api key failed.')
            sys.exit(1)
        elif response.status_code == 204:
            sys.stdout.write('Deleted api key with id: %s \n' % api_key_id)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def get(api_key_id):
    """
    Get a specific apikey
    """
    action, url = _url((api_key_id,))
    headers = api_utils.generate_headers('rw', method='GET', body='',
                                         action=action)
    try:
        response = requests.get(url, headers=headers)
        handle_api_key_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def get_all(owner=False):
    """
    Get apikeys associated with the account - this uses rw apikey so does not return owner api keys
    """
    action, url = _url()
    headers = api_utils.generate_headers('owner' if owner else 'rw', method='GET', body='',
                                         action=action)
    try:
        response = requests.get(url, headers=headers)
        handle_api_key_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def create(payload):
    """
    Create an api key with the provided ID
    """
    action, url = _url()

    headers = api_utils.generate_headers('owner', method='POST', body=json.dumps(payload),
                                         action=action)

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response_utils.response_error(response):
            sys.stderr.write('Create api key failed.')
            sys.exit(1)
        elif response.status_code == 201:
            handle_api_key_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def update(api_key_id, active):
    """
    Enable or disable an api key with given ID
    """
    action, url = _url((api_key_id,))
    payload = {
        "apikey":
            {
                "active": active
            }
    }

    headers = api_utils.generate_headers('owner', method='PATCH', body=json.dumps(payload),
                                         action=action)
    try:
        response = requests.patch(url, json=payload, headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write('Failed to %s api key with id: %s \n' %
                             ('enable' if active else 'disable', api_key_id))
            sys.exit(1)
        elif response.status_code == 200:
            sys.stdout.write('%s api key with id: %s\n' %
                             ('Enabled' if active else 'Disabled', api_key_id))
            handle_api_key_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)
