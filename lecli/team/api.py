"""
Team API module.
"""
import sys

import click
import requests
from tabulate import tabulate

from lecli import api_utils
from lecli import response_utils


def _url(provided_path_parts=()):
    """
    Get rest query url of account resource id.
    """
    ordered_path_parts = ['management', 'accounts', api_utils.get_account_resource_id(), 'teams']
    ordered_path_parts.extend(provided_path_parts)
    return api_utils.build_url(ordered_path_parts)


def print_teams(response):
    """
    Print teams.
    """
    for item in response:
        click.echo("ID: %s" % item['id'])
        click.echo("Name: %s" % item['name'])
        click.echo("Users: %s" % tabulate(item['users']))


def print_team(response):
    """
    Print team.
    """
    click.echo("ID: %s" % response['id'])
    click.echo("Name: %s" % response['name'])
    click.echo("Users: %s" % tabulate(response['users']))


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
        response = requests.get(_url()[1], data='', headers=headers)
        handle_get_teams_response(response)
    except requests.exceptions.RequestException as error:
        click.echo(error, err=True)
        sys.exit(1)


def get_team(team_id):
    """
    Get a specific team.
    """
    headers = api_utils.generate_headers('rw')
    params = {'teamid': team_id}
    try:
        response = requests.get(_url((team_id,))[1], params=params, headers=headers)
        handle_get_teams_response(response)
    except requests.exceptions.RequestException as error:
        click.echo(error, err=True)
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
        response = requests.post(_url()[1], json=params, headers=headers)
        if response_utils.response_error(response):
            click.echo('Creating team failed.', err=True)
            sys.exit(1)
        elif response.status_code == 201:
            click.echo('Team created with name: %s' % name)

    except requests.exceptions.RequestException as error:
        click.echo(error, err=True)
        sys.exit(1)


def delete_team(team_id):
    """
    Delete a team with the provided team ID.
    """
    headers = api_utils.generate_headers('rw')

    try:
        response = requests.delete(_url((team_id,))[1], headers=headers)
        if response_utils.response_error(response):  # Check response has no errors
            click.echo('Delete team failed.', err=True)
            sys.exit(1)
        elif response.status_code == 204:
            click.echo('Deleted team with id: %s.' % team_id)
    except requests.exceptions.RequestException as error:
        click.echo(error, err=True)
        sys.exit(1)


def rename_team(team_id, team_name):
    """
    Rename team with the provided team_id.
    """
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
        response = requests.patch(_url((team_id,))[1], json=params, headers=headers)
        if response_utils.response_error(response):  # Check response has no errors
            click.echo('Renaming team with id: %s failed.' % team_id, err=True)
            sys.exit(1)
        elif response.status_code == 200:
            click.echo("Team: '%s' renamed to: '%s'" % (team_id, team_name))
    except requests.exceptions.RequestException as error:
        click.echo(error, err=True)
        sys.exit(1)


def add_user_to_team(team_id, user_key):
    """
    Add user with the provided user_key to team with provided team_id.
    """
    headers = api_utils.generate_headers('rw')
    params = {'teamid': team_id}
    try:
        response = requests.get(_url((team_id,))[1], params=params, headers=headers)
        if response.status_code == 200:
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
                response = requests.patch(_url((team_id,))[1], json=params, headers=headers)
                if response_utils.response_error(response):  # Check response has no errors
                    click.echo('Adding user to team with key: %s failed.' % team_id, err=True)
                    sys.exit(1)
                elif response.status_code == 200:
                    click.echo('Added user with key: %s to team.' % user_key)
            except requests.exceptions.RequestException as error:
                click.echo(error, err=True)
                sys.exit(1)
        elif response_utils.response_error(response):
            click.echo('Cannot find team. Adding user to team %s failed.' % team_id, err=True)
            sys.exit(1)
    except requests.exceptions.RequestException as error:
        click.echo(error, err=True)
        sys.exit(1)


def delete_user_from_team(team_id, user_key):
    """
    Delete a user from a team.
    """
    headers = api_utils.generate_headers('rw')
    params = {'teamid': team_id}
    try:
        response = requests.request('GET', _url((team_id,))[1], params=params,
                                    headers=headers)
        if response.status_code == 200:
            params = {
                'team': {
                    'name': response.json()['team']['name'],
                    'users': [user for user in response.json()['team']['users'] if user['id'] !=
                              user_key]
                }
            }
            headers = api_utils.generate_headers('rw')
            try:
                response = requests.put(_url((team_id,))[1], json=params, headers=headers)
                if response_utils.response_error(response):  # Check response has no errors
                    click.echo('Deleting user from team with key: %s failed.' % team_id, err=True)
                    sys.exit(1)
                elif response.status_code == 200:
                    click.echo("Deleted user with key: '%s' from team: %s" % (user_key, team_id))
            except requests.exceptions.RequestException as error:
                click.echo(error, err=True)
                sys.exit(1)
        elif response_utils.response_error(response):
            click.echo('Cannot find team. Deleting user from team %s failed.' % team_id, err=True)
            sys.exit(1)
    except requests.exceptions.RequestException as error:
        click.echo(error, err=True)
        sys.exit(1)
