"""
User API module.
"""
import sys
import json

import requests
from tabulate import tabulate

from lecli import api_utils
from lecli import response_utils


def _url(provided_path_parts=()):
    """
    Get rest query url of account resource id.
    """
    ordered_path_parts = ['management', 'accounts', api_utils.get_account_resource_id()]
    ordered_path_parts.extend(provided_path_parts)
    return api_utils.build_url(ordered_path_parts)


def handle_userlist_response(response):
    """
    Handle userlist response. Exit if it has any errors, print if status code is 200.
    """
    if response_utils.response_error(response) is True:  # Check response has no errors
        sys.stderr.write(response.text)
        sys.exit(1)
    elif response.status_code == 200:
        print_users(response)


def handle_create_user_response(response):
    """
    Handle create user response. If it has any errors, print help.
    """
    if response_utils.response_error(response) is True:  # Check response has no errors
        if response.status_code >= 400:
            sys.stderr.write('Failed to add user - User may have already been '
                             'added this account or have a Logentries account')
            sys.stderr.write('To add a new user: lecli adduser -f John -l Smyth -e john@smyth.com')
            sys.stderr.write('To add an existing user using their User Key: '
                             'lecli adduser -u 12345678-aaaa-bbbb-1234-1234cb123456')
        sys.exit(1)

    if response.status_code == 200:
        user = response.json()['user']
        print 'Added user to account:\nName: %s %s \nLogin: %s \nEmail: %s \nUser Key: %s' % \
              (user['first_name'], user['last_name'], user['login_name'], user['email'], user['id'])

    if response.status_code == 201:
        user = response.json()['user']
        print 'Added user to account:\nName: %s %s \nLogin: %s \nEmail: %s \nUser Key: %s' % \
              (user['first_name'], user['last_name'], user['login_name'], user['email'], user['id'])

    if response.status_code == 403:
        sys.stderr.write("User you attempted to add is the account owner")


def list_users():
    """
    List users that is in the current account.
    """
    action, url = _url(('users',))
    try:
        response = requests.request('GET', url,
                                    headers=api_utils.generate_headers('owner', 'GET', action, ''))
        handle_userlist_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def add_new_user(first_name, last_name, email):
    """
    Add a new user to the current account.
    """
    action, url = _url(('users',))
    json_content = {
        "user":
            {
                "email": str(email),
                "first_name": str(first_name),
                "last_name": str(last_name)
            }
    }
    body = json.dumps(json_content)
    headers = api_utils.generate_headers('owner', method='POST', action=action, body=body)

    try:
        response = requests.request('POST', url, json=json_content, headers=headers)
        handle_create_user_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def add_existing_user(user_key):
    """
    Add a user that already exist to the current account.
    """
    action, url = _url(('users', user_key))
    headers = api_utils.generate_headers('owner', method='POST', action=action, body='')

    try:
        response = requests.request('POST', url, data='', headers=headers)
        handle_create_user_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def delete_user(user_key):
    """
    Delete a user from the current account.
    """
    action, url = _url(('users', user_key))
    headers = api_utils.generate_headers('owner', method='DELETE', action=action, body='')

    try:
        response = requests.request('DELETE', url, data='', headers=headers)
        if response_utils.response_error(response) is True:  # Check response has no errors
            sys.stderr.write('Delete user failed, status code: %s' % response.status_code)
            sys.exit(1)
        elif response.status_code == 204:
            print 'Deleted user'
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def get_owner():
    """
    Get owner information of the current account.
    """
    action, url = _url(('owners',))
    try:
        response = requests.request('GET', url,
                                    headers=api_utils.generate_headers('owner', 'GET', action, ''))
        handle_userlist_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def print_users(response):
    """
    Print users in the current account.
    """
    if 'users' in response.json():
        print tabulate(response.json()['users'], headers={})
    elif 'owners' in response.json():
        print tabulate(response.json()['owners'], headers={})
