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
from lecli.log import commands as log_commands
from lecli.logset import commands as logset_commands
from lecli import deprecated_commands


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
def replace():
    """Replace a resource"""
    pass


@cli.group()
def delete():
    """Delete a resource"""
    pass


if __name__ == '__main__':
    cli()

cli.add_command(query_commands.query)

get.add_command(query_commands.get_events, "events")
get.add_command(query_commands.get_recent_events, "recentevents")
get.add_command(saved_query_commands.get_saved_query, "savedquery")
get.add_command(saved_query_commands.get_saved_queries, "savedqueries")
get.add_command(team_commands.get_team, "team")
get.add_command(team_commands.get_teams, "teams")
get.add_command(usage_commands.get_usage, "usage")
get.add_command(user_commands.get_owner, "owner")
get.add_command(user_commands.get_users, "users")
get.add_command(log_commands.getlog, "log")
get.add_command(log_commands.getlogs, "logs")
get.add_command(logset_commands.getlogsets, "logsets")
get.add_command(logset_commands.getlogset, "logset")

create.add_command(saved_query_commands.create_saved_query, "savedquery")
create.add_command(team_commands.create_team, "team")
create.add_command(user_commands.create_user, "user")
create.add_command(log_commands.createlog, "log")
create.add_command(logset_commands.createlogset, "logset")

update.add_command(saved_query_commands.update_saved_query, "savedquery")
update.add_command(team_commands.updateteam, "team")
update.add_command(log_commands.updatelog, "log")
update.add_command(logset_commands.updatelogset, "logset")

rename.add_command(team_commands.rename_team, "team")
rename.add_command(log_commands.renamelog, "log")
rename.add_command(logset_commands.renamelogset, "logset")

replace.add_command(log_commands.replacelog, "log")
replace.add_command(logset_commands.replacelogset, "logset")

delete.add_command(saved_query_commands.delete_saved_query, "savedquery")
delete.add_command(team_commands.delete_team, "team")
delete.add_command(user_commands.delete_user, "user")
delete.add_command(log_commands.deletelog, "log")
delete.add_command(logset_commands.deletelogset, "logset")

cli.add_command(deprecated_commands.addusertoteam)
cli.add_command(deprecated_commands.adduser)
cli.add_command(deprecated_commands.createsavedquery)
cli.add_command(deprecated_commands.createteam)
cli.add_command(deprecated_commands.deletesavedquery)
cli.add_command(deprecated_commands.deleteteam)
cli.add_command(deprecated_commands.deleteuser)
cli.add_command(deprecated_commands.deleteuserfromteam)
cli.add_command(deprecated_commands.events)
cli.add_command(deprecated_commands.getowner)
cli.add_command(deprecated_commands.getsavedqueries)
cli.add_command(deprecated_commands.getsavedquery)
cli.add_command(deprecated_commands.getteams)
cli.add_command(deprecated_commands.getteam)
cli.add_command(deprecated_commands.listusers)
cli.add_command(deprecated_commands.recentevents)
cli.add_command(deprecated_commands.renameteam)
cli.add_command(deprecated_commands.updatesavedquery)
cli.add_command(deprecated_commands.usage)
