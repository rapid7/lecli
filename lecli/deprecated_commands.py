"""Deprecated commands"""
# pylint: skip-file

import click
from lecli.query import commands as query_commands
from lecli.saved_query import commands as saved_query_commands
from lecli.team import commands as team_commands
from lecli.usage import commands as usage_commands
from lecli.user import commands as user_commands

@click.command()
@click.pass_context
def getsavedqueries(ctx):
    """Deprecated method to get a list of saved queries"""
    click.echo("""This method is deprecated, please use: \n\t lecli get savedqueries""")
    ctx.forward(saved_query_commands.get_saved_queries)


@click.command()
@click.argument('query_id', type=click.STRING)
@click.pass_context
def getsavedquery(ctx, query_id):
    """Deprecated command to get the saved query with the given ID"""
    click.echo("""This method is deprecated, please use: \n\t lecli get savedquery""")
    ctx.forward(saved_query_commands.get_saved_query)


@click.command()
@click.argument('name', type=click.STRING)
@click.argument('statement', type=click.STRING)
@click.option('-f', '--timefrom', help='Time to query from (unix epoch)', type=int)
@click.option('-t', '--timeto', help='Time to query to (unix epoch)', type=int)
@click.option('-r', '--relative_range', help='Relative time range (ex: last x :timeunit)',
              type=click.STRING)
@click.option('-l', '--logs', help='Logs(colon delimited if multiple)', type=click.STRING)
@click.pass_context
def createsavedquery(ctx, name, statement, timefrom, timeto, relative_range, logs):
    """Deprecated method to create a saved query with the given arguments"""
    click.echo("""This method is deprecated, please use: \n\t lecli create savedquery""")
    ctx.forward(saved_query_commands.create_saved_query, name, statement, timefrom, timeto, relative_range, logs)


@click.command()
@click.argument('query_id', type=click.STRING)
@click.option('-n', '--name', help='Name of the saved query', type=click.STRING)
@click.option('-s', '--statement', help='LEQL statement', type=click.STRING)
@click.option('-f', '--timefrom', help='Time to query from (unix epoch)', type=int)
@click.option('-t', '--timeto', help='Time to query to (unix epoch)', type=int)
@click.option('-r', '--relative_range', help='Relative time range (ex: last x :timeunit)',
              type=click.STRING)
@click.option('-l', '--logs', help='Logs(colon delimited if multiple)', type=click.STRING)
@click.pass_context
def updatesavedquery(ctx, query_id, name, statement, timefrom, timeto, relative_range, logs):
    """Deprecated method to update the saved query with the given arguments"""
    click.echo("""This method is deprecated, please use: \n\t lecli update savedquery""")
    ctx.forward(saved_query_commands.update_saved_query)


@click.command()
@click.argument('query_id', type=click.STRING)
@click.pass_context
def deletesavedquery(ctx, query_id):
    """Deprecated method to delete the saved query with given ID"""
    click.echo("""This method is deprecated, please use: \n\t lecli delete savedquery""")
    ctx.forward(saved_query_commands.delete_saved_query)


@click.command()
@click.option('-s', '--start', type=click.STRING, default=None)
@click.option('-e', '--end', type=click.STRING, default=None)
@click.pass_context
def usage(ctx, start, end):
    """Deprecated method to get account's usage information"""
    click.echo("""This method is deprecated, please use: \n\t lecli get usage""")
    ctx.forward(usage_commands.get_usage)


@click.command()
@click.pass_context
def getteams(ctx):
    """Deprecated method to get teams that are associated with this account"""
    click.echo("""This method is deprecated, please use: \n\t lecli get teams""")
    ctx.forward(team_commands.get_teams)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.pass_context
def getteam(ctx, teamid):
    """Deprecated method to get team with the provided id"""
    click.echo("""This method is deprecated, please use: \n\t lecli get team""")
    ctx.forward(team_commands.get_team)


@click.command()
@click.argument('name', type=click.STRING, default=None)
@click.pass_context
def createteam(ctx, name):
    """Deprecated method to create a team with the provided name"""
    click.echo("""This method is deprecated, please use: \n\t lecli create team""")
    ctx.forward(team_commands.create_team)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.pass_context
def deleteteam(ctx, teamid):
    """Deprecated method to delete a team with the provided ID"""
    click.echo("""This method is deprecated, please use: \n\t lecli delete team""")
    ctx.forward(team_commands.delete_team)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('name', type=click.STRING, default=None)
@click.pass_context
def renameteam(ctx, teamid, name):
    """Deprecated method to update the team with the provided id with name and user."""
    click.echo("""This method is deprecated, please use: \n\t lecli rename team""")
    ctx.forward(team_commands.rename_team)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('userkey', type=click.STRING, default=None)
@click.pass_context
def addusertoteam(ctx, teamid, userkey):
    """Deprecated method to update the team with the provided id with name and user."""
    click.echo("""This method is deprecated, please use: \n\t lecli update team add_user""")
    ctx.forward(team_commands.addusertoteam)


@click.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('userkey', type=click.STRING, default=None)
@click.pass_context
def deleteuserfromteam(ctx, teamid, userkey):
    """Deprecated method to update the team with the provided id with name and user."""
    click.echo("""This method is deprecated, please use: \n\t lecli delete user_from_team""")
    ctx.forward(team_commands.deleteuserfromteam)


@click.command()
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-n', '--lognick', default=None,
              help='Nickname of log in config file')
@click.option('-g', '--loggroup', default=None,
              help='Name of log group defined in config file')
@click.option('-f', '--timefrom',
              help='Time to get events from (unix epoch)', type=int)
@click.option('-t', '--timeto',
              help='Time to get events to (unix epoch)', type=int)
@click.option('--datefrom',
              help='Date/Time to get events from (ISO-8601 datetime)')
@click.option('--dateto',
              help='Date/Time to get events to (ISO-8601 datetime)')
@click.option('-r', '--relative_range',
              help='Relative range to query until now (Examples: today, yesterday, '
                   'last x timeunit: last 2 hours, last 6 weeks etc.')
@click.pass_context
def events(ctx, logkeys, lognick, loggroup, timefrom, timeto, datefrom, dateto, relative_range):
    """Deprecated method to get log events"""
    click.echo("""This method is deprecated, please use: \n\t lecli get events""")
    ctx.forward(query_commands.get_events)


@click.command()
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-n', '--lognick', default=None,
              help='Nickname of log in config file')
@click.option('-g', '--loggroup', default=None,
              help='Name of log group defined in config file')
@click.option('-l', '--last', default=1200,
              help='Time window from now to now-X in seconds over which events will be returned '
                   '(Defaults to 20 mins)')
@click.option('-r', '--relative_range',
              help='Relative range to query until now (Examples: today, yesterday, '
                   'last x timeunit: last 2 hours, last 6 weeks etc.')
@click.pass_context
def recentevents(ctx, logkeys, lognick, loggroup, last, relative_range):
    """Deprecated method to get recent log events"""
    click.echo("""This method is deprecated, please use: \n\t lecli get recentevents""")
    ctx.forward(query_commands.get_recent_events)


@click.command()
@click.pass_context
def listusers(ctx):
    """Deprecated method to get list of users in account"""
    click.echo("""This method is deprecated, please use: \n\t lecli get users""")
    ctx.forward(user_commands.get_users)


@click.command()
@click.option('-f', '--first', type=click.STRING,
              help='First name of user to be added')
@click.option('-l', '--last', type=click.STRING,
              help='Last name of user to be added')
@click.option('-e', '--email', type=click.STRING,
              help='Email address of user to be added')
@click.option('-u', '--userkey', type=click.STRING,
              help='User Key of user to be added')
@click.option('--force', is_flag=True,
              help='Force adding user with confirmation prompt')
@click.pass_context
def adduser(ctx, first, last, email, userkey, force):
    """Deprecated method to add a user to account"""
    click.echo("""This method is deprecated, please use: \n\t lecli create user""")
    ctx.forward(user_commands.create_user)


@click.command()
@click.option('-u', '--userkey', type=click.STRING,
              help='User Key of user to be deleted')
@click.pass_context
def deleteuser(ctx, userkey):
    """Deprecated method to delete a user from account"""
    click.echo("""This method is deprecated, please use: \n\t lecli delete user""")
    ctx.forward(user_commands.delete_user)


@click.command()
@click.pass_context
def getowner(ctx):
    """Deprecated method to get account owner details"""
    click.echo("""This method is deprecated, please use: \n\t lecli get owner""")
    ctx.forward(user_commands.get_owner)
