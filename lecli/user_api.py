import json

import requests
from tabulate import tabulate

from lecli import apiutils


def _url(endpoint):
    """
    Get rest query url of account resource id.
    """
    if endpoint == 'owner':
        return 'https://rest.logentries.com/management/accounts/' + str(
            apiutils.get_account_resource_id()) + '/owners'
    elif endpoint == 'user':
        return 'https://rest.logentries.com/management/accounts/' + str(
            apiutils.get_account_resource_id()) + '/users'


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
        if response.status_code == 500:
            print 'Your account may have no owner assigned. ' \
                  'Please visit www.logentries.com for information on assigning an account owner.'
        return True

    if response.status_code == 200:
        if response.headers['Content-Type'] != 'application/json':
            print 'Unexpected Content Type Received in Response: ' + response.headers[
                'Content-Type']
            return True
        else:
            return False
    return False


def handle_userlist_response(response):
    """
    Handle userlist response. Exit if it has any errors, print if status code is 200.
    """
    if response_error(response) is True:  # Check response has no errors
        exit(1)
    elif response.status_code == 200:
        print_users(response)


def handle_create_user_response(response):
    """
    Handle create user response. If it has any errors, print help.
    """
    if response_error(response) is True:  # Check response has no errors
        if response.status_code >= 400:
            print 'Failed to add user - User may have already been added this account or have a ' \
                  'Logentries account'
            print 'To add a new user: lecli useradd -f John -l Smyth -e john@smyth.com'
            print 'To add an existing user using their user ID: lecli useradd -u ' \
                  '12345678-aaaa-bbbb-1234-1234cb123456'
        exit(1)

    if response.status_code == 200:
        user = response.json()['user']
        print 'Added user to account:\nName: %s %s \nLogin: %s \nEmail: %s \nUser ID: %s' % \
              (user['first_name'], user['last_name'], user['login_name'], user['email'], user['id'])

    if response.status_code == 201:
        user = response.json()['user']
        print 'Added user to account:\nName: %s %s \nLogin: %s \nEmail: %s \nUser ID: %s' % \
              (user['first_name'], user['last_name'], user['login_name'], user['email'], user['id'])

    if response.status_code == 403:
        print "User you attempted to add is the account owner"


def list_users():
    """
    List users that is in the current account.
    """
    action = 'management/accounts/' + str(apiutils.get_account_resource_id()) + '/users'
    try:
        response = requests.request('GET', _url('user'), headers=apiutils.generate_headers(
            'owner', 'GET', action, ''))
        handle_userlist_response(response)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def add_new_user(first_name, last_name, email):
    """
    Add a new user to the current account.
    """
    action = 'management/accounts/' + str(apiutils.get_account_resource_id()) + '/users'
    json_content = {
        "user": {"email": str(email),
                 "first_name": str(first_name),
                 "last_name": str(last_name)
                 }
    }
    body = json.dumps(json_content)
    headers = apiutils.generate_headers('owner', method='POST', action=action, body=body)

    try:
        response = requests.request('POST', _url('user'), json=json_content, headers=headers)
        handle_create_user_response(response)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def add_existing_user(user_id):
    """
    Add a user that already exist to the current account.
    """
    url = _url('user') + '/' + str(user_id)
    action = url.split("com/")[1]
    headers = apiutils.generate_headers('owner', method='POST', action=action, body='')

    try:
        response = requests.request('POST', url, data='', headers=headers)
        handle_create_user_response(response)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def delete_user(user_id):
    """
    Delete a user from the current account.
    """
    url = _url('user') + '/' + str(user_id)
    action = url.split("com/")[1]
    headers = apiutils.generate_headers('owner', method='DELETE', action=action, body='')

    try:
        response = requests.request('DELETE', url, data='', headers=headers)
        if response_error(response) is True:  # Check response has no errors
            print 'Delete user failed, status code: ' + str(response.status_code)
            exit(1)
        elif response.status_code == 204:
            print 'Deleted user'
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def get_owner():
    """
    Get owner information of the current account.
    """
    action = 'management/accounts/' + str(apiutils.get_account_resource_id()) + '/owners'
    try:
        response = requests.request('GET', _url('owner'), headers=apiutils.generate_headers(
            'owner', 'GET', action, ''))
        handle_userlist_response(response)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def print_users(response):
    """
    Print users in the current account.
    """
    if 'users' in response.json():
        print tabulate(response.json()['users'], headers={})
    elif 'owners' in response.json():
        print tabulate(response.json()['owners'], headers={})
