"""
Module for team commands
"""
import click

from lecli.team import api


@click.command()
def get_teams():
    """Get teams that are associated with this account"""
    api.get_teams()


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
def get_team(teamid):
    """Get team with the provided id"""
    if teamid is not None:
        api.get_team(teamid)


@click.command()
@click.argument('name', type=click.STRING, default=None)
def create_team(name):
    """Create a team with the provided name"""
    if name is not None:
        api.create_team(name)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
def delete_team(teamid):
    """Delete a team with the provided id"""
    api.delete_team(teamid)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('name', type=click.STRING, default=None)
def rename_team(teamid, name):
    """Rename a given team with the name provided"""
    api.rename_team(teamid, name)


@click.command(help='Available commands are:\n\t"add_user"\n\t"delete_user"')
@click.argument('command', type=click.STRING, default=None)
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('userkey', type=click.STRING, default=None)
def updateteam(command, teamid, userkey):
    """Update a team by adding or deleting a user."""
    if command == 'add_user':
        api.add_user_to_team(teamid, userkey)
    elif command == 'delete_user':
        api.delete_user_from_team(teamid, userkey)
    else:
        click.echo('Missing argument "command".')


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('userkey', type=click.STRING, default=None)
def addusertoteam(teamid, userkey):
    """
    DEPRECATED
    Update the team with the provided id with name and user.
    This will add the user to this team if it exists"""
    api.add_user_to_team(teamid, userkey)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('userkey', type=click.STRING, default=None)
def deleteuserfromteam(teamid, userkey):
    """
    DEPRECATED
    Delete the user with the given userkey from the team
    """
    api.delete_user_from_team(teamid, userkey)
