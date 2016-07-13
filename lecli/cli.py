import click

from lecli import apiutils
from lecli import query_api
from lecli import team_api
from lecli import user_api


@click.group()
@click.version_option(version=0.2)
def cli():
    """Logentries Command Line Interface"""
    # load configs from config.ini file in user_config_dir depending on running OS
    apiutils.load_config()


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
@click.argument('userid', type=click.STRING, default=None)
def addusertoteam(teamid, userid):
    """Update the team with the provided id with name and user.
    This will add the user to this team if it exists"""
    team_api.add_user_to_team(teamid, userid)\


@cli.command()
@click.argument('teamid', type=click.STRING, default=None)
@click.argument('userid', type=click.STRING, default=None)
def deleteuserfromteam(teamid, userid):
    """Update the team with the provided id with name and user.
    This will add the user to this team if it exists"""
    team_api.delete_user_from_team(teamid, userid)


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
def query(logkeys, lognick, loggroup, leql, querynick, timefrom, timeto, datefrom, dateto):
    """Query logs using LEQL"""

    if lognick is not None:
        logkeys = apiutils.get_named_logkey(lognick)

    if loggroup is not None:
        logkeys = apiutils.get_named_logkey_group(loggroup)

    if all([leql, querynick]):
        click.echo("Cannot define a LEQL query and query nickname in the same query request")
    elif querynick is not None:
        leql = apiutils.get_query_from_nickname(querynick)

    if all([logkeys, leql, timefrom, timeto]):
        query_api.post_query(logkeys, leql, time_from=timefrom, time_to=timeto)
    elif all([logkeys, leql, datefrom, dateto]):
        query_api.post_query(logkeys, leql, date_from=datefrom, date_to=dateto)
    else:
        click.echo("Example usage: lecli query 12345678-aaaa-bbbb-1234-1234cb123456 -q "
                   "'where(method=GET) calculate(count)' -f 1465370400 -t 1465370500")
        click.echo("Example usage: lecli query 12345678-aaaa-bbbb-1234-1234cb123456 -q "
                   "'where(method=GET) calculate(count)'  "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'")
        click.echo("Example usage: lecli query --loggroup myloggroup --leql "
                   "'where(method=GET) calculate(count)' "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'")
        click.echo("Example usage: lecli query --lognick mynicknamedlog --leql "
                   "'where(method=GET) calculate(count)' "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'")


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
def events(logkeys, lognick, loggroup, timefrom, timeto, datefrom, dateto):
    """Get log events"""

    if lognick is not None:
        logkeys = apiutils.get_named_logkey(lognick)
    elif loggroup is not None:
        logkeys = apiutils.get_named_logkey_group(loggroup)

    if all([logkeys, timefrom, timeto]):
        query_api.get_events(logkeys, time_from=timefrom, time_to=timeto)
    elif all([logkeys, datefrom, dateto]):
        query_api.get_events(logkeys, date_from=datefrom, date_to=dateto)
    else:
        click.echo("Example usage: lecli events 12345678-aaaa-bbbb-1234-1234cb123456 "
                   "-f 1465370400 -t 1465370500")
        click.echo("Example usage: lecli events 12345678-aaaa-bbbb-1234-1234cb123456"
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'")
        click.echo("Example usage: lecli events --loggroup myloggroup"
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'")
        click.echo("Example usage: lecli events --lognick mynicknamedlog"
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'")


@cli.command()
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-n', '--lognick', default=None,
              help='Nickname of log in config file')
@click.option('-g', '--loggroup', default=None,
              help='Name of log group defined in config file')
@click.option('-t', '--timewindow', default=1200,
              help='Time window from now to now-X in seconds over which events will be returned '
                   '(Defaults to 20 mins)')
def recentevents(logkeys, lognick, loggroup, timewindow):
    """Get recent log events"""

    if lognick is not None:
        logkeys = apiutils.get_named_logkey(lognick)
    elif loggroup is not None:
        logkeys = apiutils.get_named_logkey_group(loggroup)

    if all([logkeys, timewindow]):
        query_api.get_recent_events(logkeys, timewindow)

    else:
        click.echo(
            'Example usage: lecli recentevents \'12345678-aaaa-bbbb-1234-1234cb123456\' -t 200')
        click.echo('Example usage: lecli recentevents -n mynicknamedlog -t 200')
        click.echo('Example usage: lecli recentevents -g myloggroup -t 200')


@cli.command()
def userlist():
    """Get list of users in account"""

    user_api.list_users()


@cli.command()
@click.option('-f', '--first', type=click.STRING,
              help='First name of user to be added')
@click.option('-l', '--last', type=click.STRING,
              help='Last name of user to be added')
@click.option('-e', '--email', type=click.STRING,
              help='Email address of user to be added')
@click.option('-u', '--userid', type=click.STRING,
              help='User ID of user to be added')
@click.option('--force', is_flag=True,
              help='Force adding user with confirmation prompt')
def useradd(first, last, email, userid, force):
    """Add a user to account"""

    if not any((first, last, email, userid)) or all((first, last, email, userid)):
        click.echo('Example usage\n' +
                   'Add a new user: lecli useradd -f John -l Smith -e john.smith@email.com\n' +
                   'Add an existing user: lecli useradd -u 1343423')

    elif first and last and email is not None:
        if force:
            user_api.add_new_user(first, last, email)
        else:
            if click.confirm('Please confirm you want to add user ' + first + ' ' + last):
                user_api.add_new_user(first, last, email)

    elif userid is not None:
        if force:
            user_api.add_existing_user(userid)
        else:
            if click.confirm('Please confirm you want to add user with user ID ' + userid):
                user_api.add_existing_user(userid)


@cli.command()
@click.option('-u', '--userid', type=click.STRING,
              help='User ID of user to be deleted')
def userdel(userid):
    """Delete a user from account"""
    if userid is None:
        click.echo('Example usage: lecli userdel -u 12345678-aaaa-bbbb-1234-1234cb123456')

    else:
        user_api.delete_user(userid)


@cli.command()
def getowner():
    """Get account owner details"""

    user_api.get_owner()


if __name__ == '__main__':
    cli()
