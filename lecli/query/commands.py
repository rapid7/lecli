# pylint: disable=too-many-arguments
"""
Module for query commands
"""
import time
import click

from lecli.query import api


@click.command()
# nargs (-1) makes sure multiple log keys is supported
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-c', '--favorites', default=None,
              help='Alias of log in config file')
@click.option('-g', '--logset', default=None,
              help='Name of logset to be got from server')
@click.option('-l', '--leql', default=None,
              help='LEQL query')
@click.option('-f', '--timefrom',
              help='Time to query from (unix epoch)', type=int)
@click.option('-t', '--timeto',
              help='Time to query to (unix epoch)', type=int)
@click.option('--datefrom',
              help='Date/Time to query from (ISO-8601 datetime)')
@click.option('--dateto',
              help='Date/Time to query to (ISO-8601 datetime)')
@click.option('-r', '--relative-range',
              help='Relative range to query until now (Examples: today, yesterday, last 10 min, '
                   'last 6 weeks')
@click.option('-s', '--saved-query', help='Saved query UUID to run.', type=click.UUID)
def query(logkeys, favorites, logset, leql, timefrom, timeto, datefrom, dateto,
          relative_range, saved_query):
    """Query logs using LEQL"""
    success = api.query(log_keys=logkeys, query_string=leql, date_from=datefrom, date_to=dateto,
                        time_from=timefrom, time_to=timeto, saved_query_id=saved_query,
                        relative_time_range=relative_range, favorites=favorites, logset=logset)

    if not success:
        click.echo("Example usage: lecli query --logset mylogset --leql "
                   "'where(method=GET) calculate(count)' "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli query --favorites mylogalias --leql "
                   "'where(method=GET) calculate(count)' "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli query --favorites mylogalias --leql "
                   "'where(method=GET) calculate(count)' "
                   "-r 'last 3 days'")


@click.command()
# nargs (-1) makes sure multiple log keys is supported
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-c', '--favorites', type=click.STRING,
              help='Alias of log in config file')
@click.option('-g', '--logset', type=click.STRING,
              help='Name of logset to be got from server')
@click.option('-f', '--timefrom', type=click.INT,
              help='Time to get events from (unix epoch)')
@click.option('-t', '--timeto', type=click.INT,
              help='Time to get events to (unix epoch)')
@click.option('--datefrom', type=click.STRING,
              help='Date/Time to get events from (ISO-8601 datetime)')
@click.option('--dateto', type=click.STRING,
              help='Date/Time to get events to (ISO-8601 datetime)')
@click.option('-r', '--relative-range', type=click.STRING,
              help='Relative range to query until now (Examples: today, yesterday, '
                   'last x timeunit: last 2 hours, last 6 weeks etc.')
@click.option('-s', '--saved-query', help='Saved query UUID to run.', type=click.UUID)
def get_events(logkeys, favorites, logset, timefrom, timeto, datefrom, dateto, relative_range,
               saved_query):
    """Get log events"""
    success = api.query(log_keys=logkeys, time_from=timefrom, query_string=api.ALL_EVENTS_QUERY,
                        time_to=timeto, date_from=datefrom, date_to=dateto, logset=logset,
                        relative_time_range=relative_range, favorites=favorites,
                        saved_query_id=saved_query)
    if not success:
        click.echo("Example usage: lecli get events 12345678-aaaa-bbbb-1234-1234cb123456 "
                   "-f 1465370400 -t 1465370500")
        click.echo("Example usage: lecli get events 12345678-aaaa-bbbb-1234-1234cb123456 "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli get events --logset mylogset "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli get events --favorites mylogalias "
                   "--datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59' ")
        click.echo("Example usage: lecli get events --favorites mylogalias "
                   "-r 'last 3 hours'")


@click.command()
# nargs (-1) makes sure multiple log keys is supported
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-c', '--favorites', type=click.STRING, default=None,
              help='Alias of log in config file')
@click.option('-g', '--logset', type=click.STRING, default=None,
              help='Name of logset to be got from server')
@click.option('-l', '--last', type=click.INT, default=1200,
              help='Time window from now to now-X in seconds over which events will be returned '
                   '(Defaults to 20 mins)')
@click.option('-r', '--relative-range', type=click.STRING,
              help='Relative range to query until now (Examples: today, yesterday, '
                   'last x timeunit: last 2 hours, last 6 weeks etc.')
@click.option('-s', '--saved-query', help='Saved query to run', type=click.UUID)
def get_recent_events(logkeys, favorites, logset, last, relative_range, saved_query):
    """Get recent log events"""
    start_time = now = None
    if not relative_range:
        now = time.time()
        start_time = now - last

    success = api.query(log_keys=logkeys, query_string=api.ALL_EVENTS_QUERY,
                        time_from=start_time, time_to=now, relative_time_range=relative_range,
                        favorites=favorites, logset=logset, saved_query_id=saved_query)
    if not success:
        click.echo(
            'Example usage: lecli get recentevents 12345678-aaaa-bbbb-1234-1234cb123456 -l 200')
        click.echo('Example usage: lecli get recentevents -c mylogalias -l 200')
        click.echo('Example usage: lecli get recentevents -g mylogset -l 200')
        click.echo("Example usage: lecli get recentevents -g mylogset -r 'last 50 mins'")


@click.command()
# nargs (-1) makes sure multiple log keys is supported
@click.argument('logkeys', type=click.STRING, nargs=-1)
@click.option('-c', '--favorites', type=click.STRING, default=None,
              help='Alias of log in config file')
@click.option('-g', '--logset', type=click.STRING, default=None,
              help='Name of logset to be got from server')
@click.option('-l', '--leql', type=click.STRING, default=None,
              help='LEQL query to filter')
@click.option('-i', '--poll-interval', type=click.FLOAT, default=1.0,
              help='Request interval of live tail in seconds, default is 1.0 second.')
@click.option('-s', '--saved-query', type=click.UUID, help='Saved query id to tail.')
def tail_events(logkeys, favorites, logset, leql, poll_interval, saved_query):
    """Tail events of given logkey(s) with provided options"""
    success = api.tail_logs(logkeys, leql, poll_interval, favorites, logset, saved_query)

    if not success:
        click.echo("Example usage: lecli tail events 12345678-aaaa-bbbb-1234-1234cb123456")
