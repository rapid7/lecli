"""
Module for team commands
"""
import click

from lecli.team import team_api


@click.command()
def get_teams():
    """Get teams that are associated with this account"""
    team_api.get_teams()


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
def get_team(teamid):
    """Get team with the provided id"""
    if teamid is not None:
        team_api.get_team(teamid)


@click.command()
@click.argument('name', type=click.STRING, default=None)
def create_team(name):
    """Create a team with the provided name"""
    if name is not None:
        team_api.create_team(name)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
def delete_team(teamid):
    """Delete a team with the provided id"""
    team_api.delete_team(teamid)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('name', type=click.STRING, default=None)
def rename_team(teamid, name):
    """Rename a given team with the name provided"""
    team_api.rename_team(teamid, name)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('userkey', type=click.STRING, default=None)
def addusertoteam(teamid, userkey):
    """Update the team with the provided id with name and user.
    This will add the user to this team if it exists"""
    team_api.add_user_to_team(teamid, userkey)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('userkey', type=click.STRING, default=None)
def deleteuserfromteam(teamid, userkey):
    """Delete the user with the given userkey from the team"""
    team_api.delete_user_from_team(teamid, userkey)
