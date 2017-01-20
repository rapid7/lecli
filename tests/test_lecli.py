from click.testing import CliRunner
from mock import patch
from mock import mock_open
from mock import MagicMock

from examples import misc_examples as misc_ex
from lecli import cli


@patch('lecli.cli.user_api.get_owner')
def test_get_owner(mocked_get_owner):
    runner = CliRunner()
    runner.invoke(cli.getowner)

    mocked_get_owner.assert_called_once_with()

@patch('lecli.cli.user_api.delete_user')
def test_userdel(mocked_delete_user):
    runner = CliRunner()
    result = runner.invoke(cli.deleteuser, input=None)

    assert result.output == "Example usage: lecli deleteuser -u 12345678-aaaa-bbbb-1234-1234cb123456\n"

    runner.invoke(cli.deleteuser, ['-u', misc_ex.TEST_USER_KEY])
    mocked_delete_user.assert_called_once_with(misc_ex.TEST_USER_KEY)


@patch('lecli.cli.user_api.add_new_user')
def test_useradd(mocked_add_new_user):
    first = "first"
    last = "last"
    email = "email"

    runner = CliRunner()
    runner.invoke(cli.adduser, ['-f', first, '-l', last, '-e', email], input='y')
    mocked_add_new_user.assert_called_once_with(first, last, email)


@patch('lecli.cli.user_api.list_users')
def test_userlist(mocked_list_users):
    runner = CliRunner()
    runner.invoke(cli.listusers)
    mocked_list_users.assert_called_once_with()


@patch('lecli.cli.query_api.get_recent_events')
def test_recentevents(mocked_recent_events):
    runner = CliRunner()
    runner.invoke(cli.recentevents, [str(misc_ex.TEST_LOG_GROUP)])

    assert mocked_recent_events.called


@patch('lecli.cli.query_api.get_recent_events')
def test_recentevents_with_relative_range(mocked_recent_events):
    runner = CliRunner()
    runner.invoke(cli.recentevents, [str(misc_ex.TEST_LOG_GROUP), '-r', misc_ex.RELATIVE_TIME])

    assert mocked_recent_events.called


@patch('lecli.cli.query_api.get_events')
def test_events(mocked_get_events):
    runner = CliRunner()
    runner.invoke(cli.events, [str(misc_ex.TEST_LOG_GROUP), '-f', misc_ex.TIME_FROM, '-t',
                               misc_ex.TIME_TO])

    assert mocked_get_events.called


@patch('lecli.cli.query_api.get_events')
def test_events_with_relative_range(mocked_get_events):
    runner = CliRunner()
    runner.invoke(cli.events, [str(misc_ex.TEST_LOG_GROUP), '-r', misc_ex.RELATIVE_TIME])

    assert mocked_get_events.called


@patch('lecli.cli.query_api.post_query')
def test_query(mocked_post_query):
    runner = CliRunner()
    runner.invoke(cli.query, [str(misc_ex.TEST_LOG_GROUP), '-l', misc_ex.TEST_QUERY, '-f',
                              misc_ex.TIME_FROM, '-t',
                              misc_ex.TIME_TO])

    assert mocked_post_query.called


@patch('lecli.cli.query_api.post_query')
def test_query_with_relative_range(mocked_post_query):
    runner = CliRunner()
    runner.invoke(cli.query, [str(misc_ex.TEST_LOG_GROUP), '-l', misc_ex.TEST_QUERY, '-r',
                              misc_ex.RELATIVE_TIME])

    assert mocked_post_query.called


@patch('lecli.cli.team_api.get_teams')
def test_get_teams(mocked_get_teams):
    runner = CliRunner()
    runner.invoke(cli.getteams)

    assert mocked_get_teams.called


@patch('lecli.cli.team_api.get_team')
def test_get_team(mocked_get_team):
    runner = CliRunner()
    runner.invoke(cli.getteam, [str(misc_ex.TEST_TEAM_ID)])

    assert mocked_get_team.called


@patch('lecli.cli.team_api.create_team')
def test_create_team(mocked_create_team):
    runner = CliRunner()
    runner.invoke(cli.createteam, ["test_team_name"])

    assert mocked_create_team.called


@patch('lecli.cli.team_api.delete_team')
def test_delete_team(mocked_delete_team):
    runner = CliRunner()
    runner.invoke(cli.deleteteam, [str(misc_ex.TEST_TEAM_ID)])

    assert mocked_delete_team.called


@patch('lecli.cli.team_api.rename_team')
def test_rename_team(mocked_rename_team):
    runner = CliRunner()
    runner.invoke(cli.renameteam, [str(misc_ex.TEST_TEAM_ID), "new_name"])

    assert mocked_rename_team.called


@patch('lecli.cli.team_api.add_user_to_team')
def test_add_user_to_team(mocked_add_user):
    runner = CliRunner()
    runner.invoke(cli.addusertoteam, [str(misc_ex.TEST_TEAM_ID), "test_user_name"])

    assert mocked_add_user.called


@patch('lecli.cli.usage_api.get_usage')
def test_add_user_to_team(mocked_get_usage):
    runner = CliRunner()
    runner.invoke(cli.usage, ['-s', misc_ex.USAGE_DATE_FROM, '-e', misc_ex.USAGE_DATE_TO])

    assert mocked_get_usage.called


@patch('lecli.cli.saved_query_api.create_saved_query')
def test_create_saved_query(mocked_create_saved_query):
    runner = CliRunner()
    runner.invoke(cli.createsavedquery, ['new_saved_query', 'where(/*/)', '-f', 10, '-t', 1000])

    assert mocked_create_saved_query.called


@patch('lecli.cli.saved_query_api.create_saved_query')
def test_create_query_with_missing_statement(mocked_create_saved_query):
    runner = CliRunner()
    runner.invoke(cli.createsavedquery, ['new_saved_query', '-f', 10, '-t', 1000])

    assert not mocked_create_saved_query.called


@patch('lecli.cli.saved_query_api.update_saved_query')
def test_update_saved_query(mocked_update_saved_query):
    runner = CliRunner()
    runner.invoke(cli.updatesavedquery, ['123456789012345678901234567890123456', '-f', 10, '-t',
                                         1000])

    assert mocked_update_saved_query.called


@patch('lecli.cli.saved_query_api.update_saved_query')
def test_failing_update_saved_query(mocked_create_saved_query):
    runner = CliRunner()
    runner.invoke(cli.createsavedquery, ['-f', 10, '-t', 1000])

    assert not mocked_create_saved_query.called


@patch('lecli.cli.saved_query_api.get_saved_query')
def test_get_saved_query(mocked_get_saved_query):
    runner = CliRunner()
    runner.invoke(cli.getsavedquery, ['123456789012345678901234567890123456'])

    assert mocked_get_saved_query.called


@patch('lecli.cli.saved_query_api.get_saved_queries')
def test_get_saved_queries(mocked_get_saved_queries):
    runner = CliRunner()
    runner.invoke(cli.getsavedqueries)

    assert mocked_get_saved_queries.called

@patch('lecli.cli.saved_query_api.get_saved_query')
def test_get_saved_queries(mocked_get_saved_queries):
    runner = CliRunner()
    runner.invoke(cli.getsavedqueries)

    assert mocked_get_saved_queries.called


@patch('lecli.cli.saved_query_api.delete_saved_query')
def test_delete_saved_query(mocked_delete_saved_query):
    runner = CliRunner()
    runner.invoke(cli.deletesavedquery, ['123456789012345678901234567890123456'])

    assert mocked_delete_saved_query.called


@patch('lecli.cli.saved_query_api.delete_saved_query')
def test_delete_saved_query_without_id(mocked_delete_saved_query):
    runner = CliRunner()
    runner.invoke(cli.deletesavedquery)

    assert not mocked_delete_saved_query.called

@patch('lecli.cli.log_api.get_logs')
def test_get_logs(mocked_get_logs):
    runner = CliRunner()
    runner.invoke(cli.getlogs)

    mocked_get_logs.assert_called_once_with()


@patch('lecli.cli.log_api.get_log')
def test_get_log(mocked_get_log):
    runner = CliRunner()
    runner.invoke(cli.getlog, ['123'])

    mocked_get_log.assert_called_once_with('123')


@patch('lecli.cli.log_api.create_log')
@patch('os.path.exists', MagicMock(return_value=True))
@patch('os.path.isfile', MagicMock(return_value=True))
def test_create_log(mocked_create_log):
    runner = CliRunner()
    runner.invoke(cli.createlog, ['-n', 'new log'])

    mocked_create_log.assert_called_once_with('new log', None)

@patch('lecli.cli.log_api.delete_log')
def test_delete_log(mocked_delete_log):
    runner = CliRunner()
    runner.invoke(cli.deletelog, ['123'])

    mocked_delete_log.assert_called_once_with('123')


@patch('lecli.cli.log_api.rename_log')
def test_rename_log(mocked_rename_log):
    runner = CliRunner()
    runner.invoke(cli.renamelog, ['123', 'new name'])

    mocked_rename_log.assert_called_once_with('123', 'new name')


@patch('lecli.cli.log_api.replace_log')
@patch('os.path.exists', MagicMock(return_value=True))
@patch('os.path.isfile', MagicMock(return_value=True))
@patch("json.load", MagicMock('{"log": {"id": "ba2b371a-87fa-40ee-97fd-e9b0d2424b2f","name": "new_log"}}'))
def test_replace_log(mocked_replace_log):
    with patch('__builtin__.open', mock_open(read_data='data'), create=True):

        runner = CliRunner()
        runner.invoke(cli.replacelog, ['1234', 'file.json'])

        mocked_replace_log.assert_called_once()


@patch('lecli.cli.log_api.create_log')
@patch('os.path.exists', MagicMock(return_value=False))
@patch('os.path.isfile', MagicMock(return_value=False))
def test_non_existant_file(mocked_create_log):
    runner = CliRunner()
    runner.invoke(cli.createlog, ['123', 'non_existant_file.json'])

    assert not mocked_create_log.called

@patch('lecli.cli.log_api.create_log')
@patch('os.path.exists', MagicMock(return_value=True))
@patch('os.path.isfile', MagicMock(return_value=False))
def test_not_a_file(mocked_create_log):
    runner = CliRunner()
    runner.invoke(cli.createlog, ['123', 'directory'])

    assert not mocked_create_log.called