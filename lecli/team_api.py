import json

import requests

from lecli import apiutils


def _url():
    """
    Get rest query url of account resource id.
    """
    return 'https://rest.logentries.com/management/accounts/%s' + \
           apiutils.get_account_resource_id() + '/teams'


def response_error(response):
    """
    Check response if it has any errors.
    """
    if response.headers.get('X-RateLimit-Remaining') is not None:
        if int(response.headers['X-RateLimit-Remaining']) == 0:
            print 'Error: Rate Limit Reached, will reset in %s seconds' % response.headers.get(
                'X-RateLimit-Reset')
            return True
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print 'Request Error:', error.message
        if response.status_code == 500:
            print 'Your account may have no owner assigned. ' \
                  'Please visit www.logentries.com for information on assigning an account owner.'
        return True

    if response.status_code == 200:
        if response.headers['Content-Type'] != 'application/json':
            print 'Unexpected Content Type Received in Response: %s' % response.headers[
                'Content-Type']
            return True
    return False


def print_teams(response):
    """
    Print teams.
    """
    print json.dumps(response, indent=4, sort_keys=True)


def handle_get_teams_response(response):
    """
    Handle get teams response.
    """
    if response_error(response):
        exit(1)
    elif response.status_code == 200:
        if response.json().get('teams'):
            print_teams(response.json()['teams'])
        elif response.json().get('team'):
            print_teams(response.json()['team'])


def get_teams():
    """
    Get teams associated with the user.
    """
    headers = apiutils.generate_headers('rw')
    try:
        response = requests.request('GET', _url(), data='', headers=headers)
        handle_get_teams_response(response)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def get_team(team_id):
    """
    Get a specific team.
    """
    headers = apiutils.generate_headers('rw')
    params = {'teamid': team_id}
    try:
        response = requests.get(_url() + "/" + team_id, params=params,
                                headers=headers)
        handle_get_teams_response(response)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def create_team(name):
    """
    Add a new user to the current account.
    """
    params = {
        'team': {
            'name': str(name),
            'users': []
        }
    }
    headers = apiutils.generate_headers('rw')

    try:
        response = requests.post(_url(), json=params, headers=headers)
        if response_error(response):
            print 'Creating team failed, status code: %d' % response.status_code
            exit(1)
        elif response.status_code == 201:
            print 'Team created with name: %s' % name

    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def delete_team(team_id):
    """
    Delete a team with the provided team ID.
    """
    url = _url() + '/' + team_id
    headers = apiutils.generate_headers('rw')

    try:
        response = requests.delete(url, headers=headers)
        if response_error(response):  # Check response has no errors
            print 'Delete team failed, status code: %d' % response.status_code
            exit(1)
        elif response.status_code == 204:
            print 'Deleted team with id: %s' % team_id
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def rename_team(team_id, team_name):
    """
    Rename team with the provided team_id.
    """
    url = _url() + '/' + team_id
    params = {
        'team': {
            'name': team_name,
            # as this is a patch request, it won't modify users in the team.
            # what we want is to update the name of the team only.
            'users': [
                {'id': ''}
            ]
        }
    }
    headers = apiutils.generate_headers('rw')

    try:
        response = requests.patch(url, json=params, headers=headers)
        if response_error(response):  # Check response has no errors
            print 'Renaming team with id: %s failed, status code: %d' \
                  % (team_id, response.status_code)
            exit(1)
        elif response.status_code == 200:
            print "Team: '%s' renamed to: '%s'" % (team_id, team_name)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def add_user_to_team(team_id, user_id):
    """
    Add user with the provided user_id to team with provided team_id.
    """
    headers = apiutils.generate_headers('rw')
    params = {'teamid': team_id}
    try:
        response = requests.request('GET', _url() + '/' + team_id, params=params,
                                    headers=headers)
        if response.status_code == 200:
            url = _url() + '/' + team_id
            params = {
                'team': {
                    'name': response.json()['team']['name'],
                    'users': [
                        # we are doing a patch request here so it's safe to include the user_id
                        # we want to add here
                        {'id': user_id}
                    ]
                }
            }
            headers = apiutils.generate_headers('rw')
            try:
                response = requests.patch(url, json=params, headers=headers)
                if response_error(response):  # Check response has no errors
                    print 'Adding user to team with id: %s failed, status code: %d' \
                          % (team_id, response.status_code)
                    exit(1)
                elif response.status_code == 200:
                    print "Added user with id: '%s' to team" % user_id
            except requests.exceptions.RequestException as error:
                print error
                exit(1)
        elif response_error(response):
            print 'Cannot find team. Adding user to team %s failed, ' \
                  'status code: %d' % (team_id, response.status_code)
            exit(1)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)


def delete_user_from_team(team_id, user_id):
    """
    Delete a user from a team.
    """
    headers = apiutils.generate_headers('rw')
    params = {'teamid': team_id}
    try:
        response = requests.request('GET', _url() + '/' + team_id, params=params,
                                    headers=headers)
        if response.status_code == 200:
            url = _url() + '/' + team_id
            params = {
                'team': {
                    'name': response.json()['team']['name'],
                    'users': [user for user in response.json()['team']['users'] if user['id'] !=
                              user_id]
                }
            }
            headers = apiutils.generate_headers('rw')
            try:
                response = requests.put(url, json=params, headers=headers)
                if response_error(response):  # Check response has no errors
                    print 'Deleting user from team with id: %s failed, status code: %d' \
                          % (team_id, response.status_code)
                    exit(1)
                elif response.status_code == 200:
                    print "Deleted user with id: '%s' from team: %s" % (user_id, team_id)
            except requests.exceptions.RequestException as error:
                print error
                exit(1)
        elif response_error(response):
            print 'Cannot find team. Deleting user from team %s failed, ' \
                  'status code: %d' % (team_id, response.status_code)
            exit(1)
    except requests.exceptions.RequestException as error:
        print error
        exit(1)
