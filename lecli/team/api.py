"""
Team API module.
"""
import sys
import requests
from tabulate import tabulate

from lecli import api_utils
from lecli import response_utils


def _url():
    """
    Get rest query url of account resource id.
    """
    return 'https://rest.logentries.com/management/accounts/%s/teams' % \
           api_utils.get_account_resource_id()


def print_teams(response):
    """
    Print teams.
    """
    for item in response:
        print "ID: %s" % item['id']
        print "Name: %s" % item['name']
        print "Users: %s" % tabulate(item['users'])


def print_team(response):
    """
    Print team.
    """
    print "ID: %s" % response['id']
    print "Name: %s" % response['name']
    print "Users: %s" % tabulate(response['users'])


def handle_get_teams_response(response):
    """
    Handle get teams response.
    """
    if response_utils.response_error(response):
        sys.exit(1)
    elif response.status_code == 200:
        if response.json().get('teams'):
            print_teams(response.json()['teams'])
        elif response.json().get('team'):
            print_team(response.json()['team'])


def get_teams():
    """
    Get teams associated with the user.
    """
    headers = api_utils.generate_headers('rw')
    try:
        response = requests.request('GET', _url(), data='', headers=headers)
        handle_get_teams_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def get_team(team_id):
    """
    Get a specific team.
    """
    headers = api_utils.generate_headers('rw')
    params = {'teamid': team_id}
    try:
        response = requests.get(_url() + "/" + team_id, params=params,
                                headers=headers)
        handle_get_teams_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


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
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.post(_url(), json=params, headers=headers)
        if response_utils.response_error(response):
            print 'Creating team failed, status code: %d' % response.status_code
            sys.exit(1)
        elif response.status_code == 201:
            print 'Team created with name: %s' % name

    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def delete_team(team_id):
    """
    Delete a team with the provided team ID.
    """
    url = _url() + '/' + team_id
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.delete(url, headers=headers)
        if response_utils.response_error(response):  # Check response has no errors
            print 'Delete team failed, status code: %d' % response.status_code
            sys.exit(1)
        elif response.status_code == 204:
            print 'Deleted team with id: %s' % team_id
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


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
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.patch(url, json=params, headers=headers)
        if response_utils.response_error(response):  # Check response has no errors
            print 'Renaming team with id: %s failed, status code: %d' \
                  % (team_id, response.status_code)
            sys.exit(1)
        elif response.status_code == 200:
            print "Team: '%s' renamed to: '%s'" % (team_id, team_name)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def add_user_to_team(team_id, user_key):
    """
    Add user with the provided user_key to team with provided team_id.
    """
    headers = api_utils.generate_headers('rw')
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
                        # we are doing a patch request here so it's safe to include the user_key
                        # we want to add here
                        {'id': user_key}
                    ]
                }
            }
            headers = api_utils.generate_headers('rw')
            try:
                response = requests.patch(url, json=params, headers=headers)
                if response_utils.response_error(response):  # Check response has no errors
                    print 'Adding user to team with key: %s failed, status code: %d' \
                          % (team_id, response.status_code)
                    sys.exit(1)
                elif response.status_code == 200:
                    print "Added user with key: '%s' to team" % user_key
            except requests.exceptions.RequestException as error:
                sys.stderr.write(error)
                sys.exit(1)
        elif response_utils.response_error(response):
            print 'Cannot find team. Adding user to team %s failed, ' \
                  'status code: %d' % (team_id, response.status_code)
            sys.exit(1)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)


def delete_user_from_team(team_id, user_key):
    """
    Delete a user from a team.
    """
    headers = api_utils.generate_headers('rw')
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
                              user_key]
                }
            }
            headers = api_utils.generate_headers('rw')
            try:
                response = requests.put(url, json=params, headers=headers)
                if response_utils.response_error(response):  # Check response has no errors
                    print 'Deleting user from team with key: %s failed, status code: %d' \
                          % (team_id, response.status_code)
                    sys.exit(1)
                elif response.status_code == 200:
                    print "Deleted user with key: '%s' from team: %s" % (user_key, team_id)
            except requests.exceptions.RequestException as error:
                sys.stderr.write(error)
                sys.exit(1)
        elif response_utils.response_error(response):
            print 'Cannot find team. Deleting user from team %s failed, ' \
                  'status code: %d' % (team_id, response.status_code)
            sys.exit(1)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)
