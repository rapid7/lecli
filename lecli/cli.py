"""
Main lecli module powered by click library.
"""
import click

import lecli
from lecli import api_utils
from lecli.query import commands as query_commands
from lecli.saved_query import commands as saved_query_commands
from lecli.team import commands as team_commands
from lecli.usage import commands as usage_commands
from lecli.user import commands as user_commands


@click.group()
@click.version_option(version=lecli.__version__)
def cli():
    """Logentries Command Line Interface"""
    # load configs from config.ini file in user_config_dir depending on running OS
    api_utils.load_config()


@cli.group()
def get():
    """Get a resource"""
    pass


@cli.group()
def create():
    """Create a resource"""
    pass


@cli.group()
def update():
    """Update a resource"""
    pass


@cli.group()
def rename():
    """Rename a resource"""
    pass


@cli.group()
def delete():
    """Delete a resource"""
    pass


if __name__ == '__main__':
    cli()


cli.add_command(query_commands.query)

get.add_command(query_commands.get_events, "events")
get.add_command(query_commands.get_recent_events, "recent_events")
get.add_command(saved_query_commands.get_saved_query, "saved_query")
get.add_command(saved_query_commands.get_saved_queries, "saved_queries")
get.add_command(team_commands.get_team, "team")
get.add_command(team_commands.get_teams, "teams")
get.add_command(usage_commands.get_usage, "usage")
get.add_command(user_commands.get_owner, "owner")
get.add_command(user_commands.get_users, "users")

create.add_command(saved_query_commands.create_saved_query, "saved_query")
create.add_command(team_commands.create_team, "team")
create.add_command(user_commands.create_user, "user")

update.add_command(saved_query_commands.update_saved_query, "saved_query")
update.add_command(team_commands.addusertoteam, "team_with_user")

rename.add_command(team_commands.rename_team, "team")

delete.add_command(saved_query_commands.delete_saved_query, "saved_query")
delete.add_command(team_commands.delete_team, "team")
delete.add_command(team_commands.deleteuserfromteam, "user_from_team")
delete.add_command(user_commands.delete_user, "user")
