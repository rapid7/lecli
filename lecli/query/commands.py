"""
Module for query commands
"""
import click

from lecli import api_utils
from lecli.query import api


@click.command()
# nargs (-1) makes sure multiple log keys is supported
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
        api.post_query(logkeys, leql, time_from=timefrom, time_to=timeto)
    elif all([logkeys, leql, datefrom, dateto]):
        api.post_query(logkeys, leql, date_from=datefrom, date_to=dateto)
    elif all([logkeys, relative_range]):
        api.post_query(logkeys, leql, time_range=relative_range)
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


@click.command()
# nargs (-1) makes sure multiple log keys is supported
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-n', '--lognick', type=click.STRING,
              help='Nickname of log in config file')
@click.option('-g', '--loggroup', type=click.STRING,
              help='Name of log group defined in config file')
@click.option('-f', '--timefrom', type=click.INT,
              help='Time to get events from (unix epoch)')
@click.option('-t', '--timeto', type=click.INT,
              help='Time to get events to (unix epoch)')
@click.option('--datefrom', type=click.STRING,
              help='Date/Time to get events from (ISO-8601 datetime)')
@click.option('--dateto', type=click.STRING,
              help='Date/Time to get events to (ISO-8601 datetime)')
@click.option('-r', '--relative_range', type=click.STRING,
              help='Relative range to query until now (Examples: today, yesterday, '
                   'last x timeunit: last 2 hours, last 6 weeks etc.')
def get_events(logkeys, lognick, loggroup, timefrom, timeto, datefrom, dateto, relative_range):
    """Get log events"""

    if lognick:
        logkeys = api_utils.get_named_logkey(lognick)
    elif loggroup:
        logkeys = api_utils.get_named_logkey_group(loggroup)

    if all([logkeys, timefrom, timeto]):
        api.get_events(logkeys, time_from=timefrom, time_to=timeto)
    elif all([logkeys, datefrom, dateto]):
        api.get_events(logkeys, date_from=datefrom, date_to=dateto)
    elif all([logkeys, relative_range]):
        api.get_events(logkeys, time_range=relative_range)
    else:
        click.echo("Example usage: lecli get events 12345678-aaaa-bbbb-1234-1234cb123456 "
                   "-f 1465370400 -t 1465370500")
        click.echo("Example usage: lecli get events 12345678-aaaa-bbbb-1234-1234cb123456 "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli get events --loggroup myloggroup "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli get events --lognick mynicknamedlog "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli get events --lognick mynicknamedlog "
                   "-r 'last 3 hours'")


@click.command()
# nargs (-1) makes sure multiple log keys is supported
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-n', '--lognick', type=click.STRING, default=None,
              help='Nickname of log in config file')
@click.option('-g', '--loggroup', type=click.STRING, default=None,
              help='Name of log group defined in config file')
@click.option('-l', '--last', type=click.INT, default=1200,
              help='Time window from now to now-X in seconds over which events will be returned '
                   '(Defaults to 20 mins)')
@click.option('-r', '--relative_range', type=click.STRING,
              help='Relative range to query until now (Examples: today, yesterday, '
                   'last x timeunit: last 2 hours, last 6 weeks etc.')
def get_recent_events(logkeys, lognick, loggroup, last, relative_range):
    """Get recent log events"""

    if lognick:
        logkeys = api_utils.get_named_logkey(lognick)
    elif loggroup:
        logkeys = api_utils.get_named_logkey_group(loggroup)

    if all([logkeys, relative_range]):
        api.get_recent_events(logkeys, time_range=relative_range)
    elif all([logkeys, last]):
        api.get_recent_events(logkeys, last_x_seconds=last)
    else:
        click.echo(
            'Example usage: lecli get recentevents 12345678-aaaa-bbbb-1234-1234cb123456 -l 200')
        click.echo('Example usage: lecli get recentevents -n mynicknamedlog -l 200')
        click.echo('Example usage: lecli get recentevents -g myloggroup -l 200')
        click.echo("Example usage: lecli get recentevents -g myloggroup -r 'last 50 mins'")


@click.command()
# nargs (-1) makes sure multiple log keys is supported
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-n', '--lognick', type=click.STRING, default=None,
              help='Nickname of log in config file')
@click.option('-g', '--loggroup', type=click.STRING, default=None,
              help='Name of log group defined in config file')
@click.option('-l', '--leql', type=click.STRING, default=None,
              help='LEQL query to filter')
@click.option('-i', '--poll_interval', type=click.FLOAT, default=1.0,
              help='Request interval of live tail in seconds, default is 1.0 second.')
def tail_events(logkeys, lognick, loggroup, leql, poll_interval):
    """Tail events of given logkey(s) with provided options"""
    if lognick:
        logkeys = api_utils.get_named_logkey(lognick)
    elif loggroup:
        logkeys = api_utils.get_named_logkey_group(loggroup)

    if len(logkeys) > 0:
        api.tail_logs(logkeys, leql, poll_interval)
    else:
        click.echo("Example usage: lecli tail events 12345678-aaaa-bbbb-1234-1234cb123456")
