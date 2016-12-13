"""
Main lecli module powered by click library.
"""
import click

import lecli
from lecli import api_utils
from lecli import query_api
from lecli import team_api
from lecli import user_api
from lecli import usage_api
from lecli import saved_query_api


@click.group()
@click.version_option(version=lecli.__version__)
def cli():
    """Logentries Command Line Interface"""
    # load configs from config.ini file in user_config_dir depending on running OS
    api_utils.load_config()


@cli.command()
def getsavedqueries():
    """Get a list of saved queries"""
    saved_query_api.get_saved_query()


@cli.command()
@click.argument('query_id', type=click.STRING)
def getsavedquery(query_id):
    """Get the saved query with the given ID"""
    saved_query_api.get_saved_query(query_id)


@cli.command()
@click.argument('name', type=click.STRING)
@click.argument('statement', type=click.STRING)
@click.option('-f', '--timefrom', help='Time to query from (unix epoch)', type=int)
@click.option('-t', '--timeto', help='Time to query to (unix epoch)', type=int)
@click.option('-r', '--relative_range', help='Relative time range (ex: last x :timeunit)',
              type=click.STRING)
@click.option('-l', '--logs', help='Logs(colon delimited if multiple)', type=click.STRING)
def createsavedquery(name, statement, timefrom, timeto, relative_range, logs):
    """Create a saved query with the given arguments"""
    saved_query_api.create_saved_query(name, statement, timefrom, timeto, relative_range, logs)


@cli.command()
@click.argument('query_id', type=click.STRING)
@click.option('-n', '--name', help='Name of the saved query', type=click.STRING)
@click.option('-s', '--statement', help='LEQL statement', type=click.STRING)
@click.option('-f', '--timefrom', help='Time to query from (unix epoch)', type=int)
@click.option('-t', '--timeto', help='Time to query to (unix epoch)', type=int)
@click.option('-r', '--relative_range', help='Relative time range (ex: last x :timeunit)',
              type=click.STRING)
@click.option('-l', '--logs', help='Logs(colon delimited if multiple)', type=click.STRING)
def updatesavedquery(query_id, name, statement, timefrom, timeto, relative_range, logs):
    """Update the saved query with the given arguments"""
    saved_query_api.update_saved_query(query_id, name, statement, timefrom, timeto, relative_range,
                                       logs)


@cli.command()
@click.argument('query_id', type=click.STRING)
def deletesavedquery(query_id):
    """Delete the saved query with given ID"""
    saved_query_api.delete_saved_query(query_id)


@cli.command()
@click.option('-s', '--start', type=click.STRING, default=None)
@click.option('-e', '--end', type=click.STRING, default=None)
def usage(start, end):
    """Get account's usage information"""
    if all([start, end]):
        usage_api.get_usage(start, end)
    else:
        click.echo("Example usage: lecli usage -s '2016-01-01' -e '2016-06-01'")
        click.echo("Note: Start and end dates should be in ISO-8601 format: YYYY-MM-DD")


@cli.command()
def getteams():
    """Get teams that is associated with this account"""
    team_api.get_teams()


@cli.command()
@click.argument('teamid', type=click.STRING, default=None)
def getteam(teamid):
    """Get team with the provided id"""
    if teamid is not None:
        team_api.get_team(teamid)


@cli.command()
@click.argument('name', type=click.STRING, default=None)
def createteam(name):
    """Create a team with the provided name"""
    if name is not None:
        team_api.create_team(name)


@cli.command()
@click.argument('teamid', type=click.STRING, default=None)
def deleteteam(teamid):
    """Create a team with the provided name"""
    team_api.delete_team(teamid)


@cli.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('name', type=click.STRING, default=None)
def renameteam(teamid, name):
    """Update the team with the provided id with name and user.
    This will add the user to this team if it exists"""
    team_api.rename_team(teamid, name)


@cli.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('userkey', type=click.STRING, default=None)
def addusertoteam(teamid, userkey):
    """Update the team with the provided id with name and user.
    This will add the user to this team if it exists"""
    team_api.add_user_to_team(teamid, userkey)


@cli.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('userkey', type=click.STRING, default=None)
def deleteuserfromteam(teamid, userkey):
    """Update the team with the provided id with name and user.
    This will add the user to this team if it exists"""
    team_api.delete_user_from_team(teamid, userkey)


@cli.command()
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-n', '--lognick', default=None,
              help='Nickname of log in config file')
@click.option('-g', '--loggroup', default=None,
              help='Name of log group defined in config file')
@click.option('-l', '--leql', default=None,
              help='LEQL query')
@click.option('-q', '--querynick',
              help='Query shortcut nickname')
@click.option('-f', '--timefrom',
              help='Time to query from (unix epoch)', type=int)
@click.option('-t', '--timeto',
              help='Time to query to (unix epoch)', type=int)
@click.option('--datefrom',
              help='Date/Time to query from (ISO-8601 datetime)')
@click.option('--dateto',
              help='Date/Time to query to (ISO-8601 datetime)')
@click.option('-r', '--relative_range',
              help='Relative range to query until now (Examples: today, yesterday, last 10 min, '
                   'last 6 weeks')
def query(logkeys, lognick, loggroup, leql, querynick, timefrom, timeto, datefrom, dateto,
          relative_range):
    """Query logs using LEQL"""

    if lognick:
        logkeys = api_utils.get_named_logkey(lognick)
    elif loggroup:
        logkeys = api_utils.get_named_logkey_group(loggroup)

    if all([leql, querynick]):
        click.echo("Cannot define a LEQL query and query nickname in the same query request")
    elif querynick:
        leql = api_utils.get_named_query(querynick)

    if all([logkeys, leql, timefrom, timeto]):
        query_api.post_query(logkeys, leql, time_from=timefrom, time_to=timeto)
    elif all([logkeys, leql, datefrom, dateto]):
        query_api.post_query(logkeys, leql, date_from=datefrom, date_to=dateto)
    elif all([logkeys, relative_range]):
        query_api.post_query(logkeys, leql, time_range=relative_range)
    else:
        click.echo("Example usage: lecli query 12345678-aaaa-bbbb-1234-1234cb123456 -q "
                   "'where(method=GET) calculate(count)' -f 1465370400 -t 1465370500")
        click.echo("Example usage: lecli query 12345678-aaaa-bbbb-1234-1234cb123456 -q "
                   "'where(method=GET) calculate(count)'  "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli query --loggroup myloggroup --leql "
                   "'where(method=GET) calculate(count)' "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli query --lognick mynicknamedlog --leql "
                   "'where(method=GET) calculate(count)' "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli query --lognick mynicknamedlog --leql "
                   "'where(method=GET) calculate(count)' "
                   "-r 'last 3 days'")


@cli.command()
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
def events(logkeys, lognick, loggroup, timefrom, timeto, datefrom, dateto, relative_range):
    """Get log events"""

    if lognick:
        logkeys = api_utils.get_named_logkey(lognick)
    elif loggroup:
        logkeys = api_utils.get_named_logkey_group(loggroup)

    if all([logkeys, timefrom, timeto]):
        query_api.get_events(logkeys, time_from=timefrom, time_to=timeto)
    elif all([logkeys, datefrom, dateto]):
        query_api.get_events(logkeys, date_from=datefrom, date_to=dateto)
    elif all([logkeys, relative_range]):
        query_api.get_events(logkeys, time_range=relative_range)
    else:
        click.echo("Example usage: lecli events 12345678-aaaa-bbbb-1234-1234cb123456 "
                   "-f 1465370400 -t 1465370500")
        click.echo("Example usage: lecli events 12345678-aaaa-bbbb-1234-1234cb123456 "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli events --loggroup myloggroup "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli events --lognick mynicknamedlog "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli events --lognick mynicknamedlog "
                   "-r 'last 3 hours'")


@cli.command()
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
def recentevents(logkeys, lognick, loggroup, last, relative_range):
    """Get recent log events"""

    if lognick:
        logkeys = api_utils.get_named_logkey(lognick)
    elif loggroup:
        logkeys = api_utils.get_named_logkey_group(loggroup)

    if all([logkeys, relative_range]):
        query_api.get_recent_events(logkeys, time_range=relative_range)
    elif all([logkeys, last]):
        query_api.get_recent_events(logkeys, last_x_seconds=last)
    else:
        click.echo(
            'Example usage: lecli recentevents \'12345678-aaaa-bbbb-1234-1234cb123456\' -l 200')
        click.echo('Example usage: lecli recentevents -n mynicknamedlog -l 200')
        click.echo('Example usage: lecli recentevents -g myloggroup -l 200')
        click.echo("Example usage: lecli recentevents -g myloggroup -r 'last 50 mins'")


@cli.command()
def listusers():
    """Get list of users in account"""

    user_api.list_users()


@cli.command()
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
def adduser(first, last, email, userkey, force):
    """Add a user to account"""

    if not any((first, last, email, userkey)) or all((first, last, email, userkey)):
        click.echo('Example usage\n' +
                   'Add a new user: lecli adduser -f John -l Smith -e john.smith@email.com\n' +
                   'Add an existing user: lecli adduser -u 1343423')

    elif first and last and email is not None:
        if force:
            user_api.add_new_user(first, last, email)
        else:
            if click.confirm('Please confirm you want to add user ' + first + ' ' + last):
                user_api.add_new_user(first, last, email)

    elif userkey is not None:
        if force:
            user_api.add_existing_user(userkey)
        else:
            if click.confirm('Please confirm you want to add user with User Key ' + userkey):
                user_api.add_existing_user(userkey)


@cli.command()
@click.option('-u', '--userkey', type=click.STRING,
              help='User Key of user to be deleted')
def deleteuser(userkey):
    """Delete a user from account"""
    if userkey is None:
        click.echo('Example usage: lecli deleteuser -u 12345678-aaaa-bbbb-1234-1234cb123456')

    else:
        user_api.delete_user(userkey)


@cli.command()
def getowner():
    """Get account owner details"""

    user_api.get_owner()


if __name__ == '__main__':
    cli()
