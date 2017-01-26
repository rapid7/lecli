from click.testing import CliRunner
from mock import patch

from examples import misc_examples as misc_ex
from lecli import cli


@patch('lecli.user.user_api.get_owner')
def test_get_owner(mocked_get_owner):
    runner = CliRunner()
    runner.invoke(cli.user_commands.get_owner)

    mocked_get_owner.assert_called_once_with()


@patch('lecli.user.user_api.delete_user')
def test_userdel(mocked_delete_user):
    runner = CliRunner()
    result = runner.invoke(cli.user_commands.delete_user, input=None)

    assert result.output == "Example usage: lecli deleteuser -u 12345678-aaaa-bbbb-1234-1234cb123456\n"

    runner.invoke(cli.user_commands.delete_user, ['-u', misc_ex.TEST_USER_KEY])
    mocked_delete_user.assert_called_once_with(misc_ex.TEST_USER_KEY)


@patch('lecli.user.user_api.add_new_user')
def test_useradd(mocked_add_new_user):
    first = "first"
    last = "last"
    email = "email"

    runner = CliRunner()
    runner.invoke(cli.user_commands.create_user, ['-f', first, '-l', last, '-e', email], input='y')
    mocked_add_new_user.assert_called_once_with(first, last, email)


@patch('lecli.user.user_api.list_users')
def test_userlist(mocked_list_users):
    runner = CliRunner()
    runner.invoke(cli.user_commands.get_users)
    mocked_list_users.assert_called_once_with()


@patch('lecli.query.query_api.get_recent_events')
def test_recentevents(mocked_recent_events):
    runner = CliRunner()
    runner.invoke(cli.query_commands.get_recent_events, [str(misc_ex.TEST_LOG_GROUP)])

    assert mocked_recent_events.called


@patch('lecli.query.query_api.get_recent_events')
def test_recentevents_with_relative_range(mocked_recent_events):
    runner = CliRunner()
    runner.invoke(cli.query_commands.get_recent_events, [str(misc_ex.TEST_LOG_GROUP), '-r', misc_ex.RELATIVE_TIME])

    assert mocked_recent_events.called


@patch('lecli.query.query_api.get_events')
def test_events(mocked_get_events):
    runner = CliRunner()
    runner.invoke(cli.query_commands.get_events, [str(misc_ex.TEST_LOG_GROUP), '-f', misc_ex.TIME_FROM, '-t',
                               misc_ex.TIME_TO])

    assert mocked_get_events.called


@patch('lecli.query.query_api.get_events')
def test_events_with_relative_range(mocked_get_events):
    runner = CliRunner()
    runner.invoke(cli.query_commands.get_events, [str(misc_ex.TEST_LOG_GROUP), '-r', misc_ex.RELATIVE_TIME])

    assert mocked_get_events.called


@patch('lecli.query.query_api.post_query')
def test_query(mocked_post_query):
    runner = CliRunner()
    runner.invoke(cli.query_commands.query, [str(misc_ex.TEST_LOG_GROUP), '-l', misc_ex.TEST_QUERY, '-f',
                              misc_ex.TIME_FROM, '-t',
                              misc_ex.TIME_TO])

    assert mocked_post_query.called


@patch('lecli.query.query_api.post_query')
def test_query_with_relative_range(mocked_post_query):
    runner = CliRunner()
    runner.invoke(cli.query_commands.query, [str(misc_ex.TEST_LOG_GROUP), '-l', misc_ex.TEST_QUERY, '-r',
                              misc_ex.RELATIVE_TIME])

    assert mocked_post_query.called


@patch('lecli.team.team_api.get_teams')
def test_get_teams(mocked_get_teams):
    runner = CliRunner()
    runner.invoke(cli.team_commands.get_teams)

    assert mocked_get_teams.called


@patch('lecli.team.team_api.get_team')
def test_get_team(mocked_get_team):
    runner = CliRunner()
    runner.invoke(cli.team_commands.get_team, [str(misc_ex.TEST_TEAM_ID)])

    assert mocked_get_team.called


@patch('lecli.team.team_api.create_team')
def test_create_team(mocked_create_team):
    runner = CliRunner()
    runner.invoke(cli.team_commands.create_team, ["test_team_name"])

    assert mocked_create_team.called


@patch('lecli.team.team_api.delete_team')
def test_delete_team(mocked_delete_team):
    runner = CliRunner()
    runner.invoke(cli.team_commands.delete_team, [str(misc_ex.TEST_TEAM_ID)])

    assert mocked_delete_team.called


@patch('lecli.team.team_api.rename_team')
def test_rename_team(mocked_rename_team):
    runner = CliRunner()
    runner.invoke(cli.team_commands.rename_team, [str(misc_ex.TEST_TEAM_ID), "new_name"])

    assert mocked_rename_team.called


@patch('lecli.team.team_api.add_user_to_team')
def test_add_user_to_team(mocked_add_user):
    runner = CliRunner()
    runner.invoke(cli.team_commands.addusertoteam, [str(misc_ex.TEST_TEAM_ID), "test_user_name"])

    assert mocked_add_user.called


@patch('lecli.usage.usage_api.get_usage')
def test_add_user_to_team(mocked_get_usage):
    runner = CliRunner()
    runner.invoke(cli.usage_commands.get_usage, ['-s', misc_ex.USAGE_DATE_FROM, '-e', misc_ex.USAGE_DATE_TO])

    assert mocked_get_usage.called


@patch('lecli.saved_query.saved_query_api.create_saved_query')
def test_create_saved_query(mocked_create_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.create_saved_query, ['new_saved_query', 'where(/*/)', '-f', 10, '-t', 1000])

    assert mocked_create_saved_query.called


@patch('lecli.saved_query.saved_query_api.create_saved_query')
def test_create_query_with_missing_statement(mocked_create_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.create_saved_query, ['new_saved_query', '-f', 10, '-t', 1000])

    assert not mocked_create_saved_query.called


@patch('lecli.saved_query.saved_query_api.update_saved_query')
def test_update_saved_query(mocked_update_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.update_saved_query, ['123456789012345678901234567890123456', '-f', 10, '-t',
                                         1000])

    assert mocked_update_saved_query.called


@patch('lecli.saved_query.saved_query_api.update_saved_query')
def test_failing_update_saved_query(mocked_create_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.create_saved_query, ['-f', 10, '-t', 1000])

    assert not mocked_create_saved_query.called


@patch('lecli.saved_query.saved_query_api.get_saved_query')
def test_get_saved_query(mocked_get_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.get_saved_query, ['123456789012345678901234567890123456'])

    assert mocked_get_saved_query.called


@patch('lecli.saved_query.saved_query_api.get_saved_query')
def test_get_saved_queries(mocked_get_saved_queries):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.get_saved_queries)

    assert mocked_get_saved_queries.called


@patch('lecli.saved_query.saved_query_api.get_saved_query')
def test_get_saved_query(mocked_get_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.get_saved_query, ['12341234'])

    assert mocked_get_saved_query.called


@patch('lecli.saved_query.saved_query_api.delete_saved_query')
def test_delete_saved_query(mocked_delete_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.delete_saved_query, ['123456789012345678901234567890123456'])

    assert mocked_delete_saved_query.called


@patch('lecli.saved_query.saved_query_api.delete_saved_query')
def test_delete_saved_query_without_id(mocked_delete_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.delete_saved_query)

    assert not mocked_delete_saved_query.called
