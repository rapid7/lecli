import click

import apiutils
import queryapi
import userapi


@click.group()
@click.version_option(version=0.1)
def cli():
    """Logentries Command Line Interface"""
    pass


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
        queryapi.post_query(logkeys, leql, time_from=timefrom, time_to=timeto)
    elif all([logkeys, leql, datefrom, dateto]):
        queryapi.post_query(logkeys, leql, date_from=datefrom, date_to=dateto)
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
        queryapi.get_events(logkeys, time_from=timefrom, time_to=timeto)
    elif all([logkeys, datefrom, dateto]):
        queryapi.get_events(logkeys, date_from=datefrom, date_to=dateto)
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
              help='Time window from now to now-X in seconds over which events will be returned (Defaults to 20 mins)')
def recentevents(logkeys, lognick, loggroup, timewindow):
    """Get recent log events"""

    if lognick is not None:
        logkeys = apiutils.get_named_logkey(lognick)
    elif loggroup is not None:
        logkeys = apiutils.get_named_logkey_group(loggroup)

    if all([logkeys, timewindow]):
        queryapi.get_recent_events(logkeys, timewindow)

    else:
        click.echo('Example usage: lecli recentevents \'12345678-aaaa-bbbb-1234-1234cb123456\' -t 200')
        click.echo('Example usage: lecli recentevents -n mynicknamedlog -t 200')
        click.echo('Example usage: lecli recentevents -g myloggroup -t 200')


@cli.command()
def userlist():
    """Get list of users in account"""

    userapi.list_users()


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
            userapi.add_new_user(first, last, email)
        else:
            if click.confirm('Please confirm you want to add user ' + first + ' ' + last):
                userapi.add_new_user(first, last, email)

    elif userid is not None:
        if force:
            userapi.add_existing_user(userid)
        else:
            if click.confirm('Please confirm you want to add user with user ID ' + userid):
                userapi.add_existing_user(userid)


@cli.command()
@click.option('-u', '--userid', type=click.STRING,
              help='User ID of user to be deleted')
def userdel(userid):
    """Delete a user from account"""
    if userid is None:
        click.echo('Example usage: lecli userdel -u 12345678-aaaa-bbbb-1234-1234cb123456')

    else:
        userapi.delete_user(userid)


@cli.command()
def getowner():
    """Get account owner details"""

    userapi.get_owner()


if __name__ == '__main__':
    cli()
