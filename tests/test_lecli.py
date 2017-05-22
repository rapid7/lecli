import os
import uuid

from click.testing import CliRunner
from mock import patch
from mock import MagicMock

from examples import misc_examples as misc_ex
from lecli import cli


@patch('lecli.user.api.get_owner')
def test_get_owner(mocked_get_owner):
    runner = CliRunner()
    runner.invoke(cli.user_commands.get_owner)

    mocked_get_owner.assert_called_once_with()


@patch('lecli.user.api.delete_user')
def test_userdel(mocked_delete_user):
    runner = CliRunner()
    result = runner.invoke(cli.user_commands.delete_user, input=None)

    assert result.output == "Example usage: lecli delete user -u 12345678-aaaa-bbbb-1234-1234cb123456\n"

    runner.invoke(cli.user_commands.delete_user, ['-u', misc_ex.TEST_USER_KEY])
    mocked_delete_user.assert_called_once_with(misc_ex.TEST_USER_KEY)


@patch('lecli.user.api.add_new_user')
def test_useradd(mocked_add_new_user):
    first = "first"
    last = "last"
    email = "email"

    runner = CliRunner()
    runner.invoke(cli.user_commands.create_user, ['-f', first, '-l', last, '-e', email], input='y')
    mocked_add_new_user.assert_called_once_with(first, last, email)


@patch('lecli.user.api.list_users')
def test_userlist(mocked_list_users):
    runner = CliRunner()
    runner.invoke(cli.user_commands.get_users)
    mocked_list_users.assert_called_once_with()


@patch('lecli.query.api.get_recent_events')
def test_recentevents(mocked_recent_events):
    runner = CliRunner()
    runner.invoke(cli.query_commands.get_recent_events, [str(misc_ex.TEST_LOG_GROUP)])

    assert mocked_recent_events.called


@patch('lecli.query.api.get_recent_events')
def test_recentevents_with_relative_range(mocked_recent_events):
    runner = CliRunner()
    runner.invoke(cli.query_commands.get_recent_events, [str(misc_ex.TEST_LOG_GROUP), '-r', misc_ex.RELATIVE_TIME])

    assert mocked_recent_events.called


@patch('lecli.query.api.get_events')
def test_events(mocked_get_events):
    runner = CliRunner()
    runner.invoke(cli.query_commands.get_events, [str(misc_ex.TEST_LOG_GROUP), '-f', misc_ex.TIME_FROM, '-t',
                               misc_ex.TIME_TO])

    assert mocked_get_events.called


@patch('lecli.query.api.tail_logs')
def test_live_tail(mocked_tail_logs):
    runner = CliRunner()
    runner.invoke(cli.query_commands.tail_events, [str(uuid.uuid4())])

    assert mocked_tail_logs.called


@patch('lecli.query.api.get_events')
def test_events_with_relative_range(mocked_get_events):
    runner = CliRunner()
    runner.invoke(cli.query_commands.get_events, [str(misc_ex.TEST_LOG_GROUP), '-r', misc_ex.RELATIVE_TIME])

    assert mocked_get_events.called


@patch('lecli.query.api.post_query')
def test_query(mocked_post_query):
    runner = CliRunner()
    runner.invoke(cli.query_commands.query, [str(misc_ex.TEST_LOG_GROUP), '-l', misc_ex.TEST_QUERY, '-f',
                              misc_ex.TIME_FROM, '-t',
                              misc_ex.TIME_TO])

    assert mocked_post_query.called


@patch('lecli.query.api.post_query')
def test_query_with_relative_range(mocked_post_query):
    runner = CliRunner()
    runner.invoke(cli.query_commands.query, [str(misc_ex.TEST_LOG_GROUP), '-l', misc_ex.TEST_QUERY, '-r',
                              misc_ex.RELATIVE_TIME])

    assert mocked_post_query.called


@patch('lecli.team.api.get_teams')
def test_get_teams(mocked_get_teams):
    runner = CliRunner()
    runner.invoke(cli.team_commands.get_teams)

    assert mocked_get_teams.called


@patch('lecli.team.api.get_team')
def test_get_team(mocked_get_team):
    runner = CliRunner()
    runner.invoke(cli.team_commands.get_team, [str(misc_ex.TEST_TEAM_ID)])

    assert mocked_get_team.called


@patch('lecli.team.api.create_team')
def test_create_team(mocked_create_team):
    runner = CliRunner()
    runner.invoke(cli.team_commands.create_team, ["test_team_name"])

    assert mocked_create_team.called


@patch('lecli.team.api.delete_team')
def test_delete_team(mocked_delete_team):
    runner = CliRunner()
    runner.invoke(cli.team_commands.delete_team, [str(misc_ex.TEST_TEAM_ID)])

    assert mocked_delete_team.called


@patch('lecli.team.api.rename_team')
def test_rename_team(mocked_rename_team):
    runner = CliRunner()
    runner.invoke(cli.team_commands.rename_team, [str(misc_ex.TEST_TEAM_ID), "new_name"])

    assert mocked_rename_team.called


@patch('lecli.team.api.add_user_to_team')
def test_add_user_to_team(mocked_add_user):
    runner = CliRunner()
    runner.invoke(cli.team_commands.addusertoteam, [str(misc_ex.TEST_TEAM_ID), "test_user_name"])

    assert mocked_add_user.called


@patch('lecli.usage.api.get_usage')
def test_add_user_to_team(mocked_get_usage):
    runner = CliRunner()
    runner.invoke(cli.usage_commands.get_usage, ['-s', misc_ex.USAGE_DATE_FROM, '-e', misc_ex.USAGE_DATE_TO])

    assert mocked_get_usage.called


@patch('lecli.saved_query.api.create_saved_query')
def test_create_saved_query(mocked_create_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.create_saved_query, ['new_saved_query', 'where(/*/)', '-f', 10, '-t', 1000])

    assert mocked_create_saved_query.called


@patch('lecli.saved_query.api.create_saved_query')
def test_create_query_with_missing_statement(mocked_create_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.create_saved_query, ['new_saved_query', '-f', 10, '-t', 1000])

    assert not mocked_create_saved_query.called


@patch('lecli.saved_query.api.update_saved_query')
def test_update_saved_query(mocked_update_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.update_saved_query, ['123456789012345678901234567890123456', '-f', 10, '-t',
                                         1000])

    assert mocked_update_saved_query.called


@patch('lecli.saved_query.api.update_saved_query')
def test_failing_update_saved_query(mocked_create_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.create_saved_query, ['-f', 10, '-t', 1000])

    assert not mocked_create_saved_query.called


@patch('lecli.saved_query.api.get_saved_query')
def test_get_saved_query(mocked_get_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.get_saved_query, ['123456789012345678901234567890123456'])

    assert mocked_get_saved_query.called


@patch('lecli.saved_query.api.get_saved_query')
def test_get_saved_queries(mocked_get_saved_queries):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.get_saved_queries)

    assert mocked_get_saved_queries.called


@patch('lecli.saved_query.api.get_saved_query')
def test_get_saved_query(mocked_get_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.get_saved_query, ['12341234'])

    assert mocked_get_saved_query.called


@patch('lecli.saved_query.api.delete_saved_query')
def test_delete_saved_query(mocked_delete_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.delete_saved_query, ['123456789012345678901234567890123456'])

    assert mocked_delete_saved_query.called


@patch('lecli.saved_query.api.delete_saved_query')
def test_delete_saved_query_without_id(mocked_delete_saved_query):
    runner = CliRunner()
    runner.invoke(cli.saved_query_commands.delete_saved_query)

    assert not mocked_delete_saved_query.called


@patch('lecli.log.api.get_logs')
def test_get_logs(mocked_get_logs):
    runner = CliRunner()
    runner.invoke(cli.log_commands.getlogs)

    mocked_get_logs.assert_called_once()


@patch('lecli.log.api.get_log')
def test_get_log(mocked_get_log):
    runner = CliRunner()
    runner.invoke(cli.log_commands.getlog, ['123'])

    mocked_get_log.assert_called_once_with('123')


@patch('lecli.log.api.create_log')
def test_create_log(mocked_create_log):
    runner = CliRunner()
    runner.invoke(cli.log_commands.createlog, ['-n', 'new log'])

    mocked_create_log.assert_called_once_with('new log', None)


@patch('lecli.log.api.delete_log')
def test_delete_log(mocked_delete_log):
    runner = CliRunner()
    runner.invoke(cli.log_commands.deletelog, ['123'])

    mocked_delete_log.assert_called_once_with('123')


@patch('lecli.log.api.rename_log')
def test_rename_log(mocked_rename_log):
    runner = CliRunner()
    runner.invoke(cli.log_commands.renamelog, ['123', 'new name'])

    mocked_rename_log.assert_called_once_with('123', 'new name')


@patch('lecli.log.api.replace_log')
def test_replace_log(mocked_replace_log):
    runner = CliRunner()
    with open('file.json', 'w') as f:
        f.write('{"log": {"id": "ba2b371a-87fa-40ee-97fd-e9b0d2424b2f","name": "new_log"}}')

    runner.invoke(cli.log_commands.replacelog, ['1234', 'file.json'])

    mocked_replace_log.assert_called_once()
    try:
        os.remove('file.json')
    except OSError:
        pass


@patch('lecli.log.api.create_log')
@patch('os.path.exists', MagicMock(return_value=False))
@patch('os.path.isfile', MagicMock(return_value=False))
def test_non_existant_file(mocked_create_log):
    runner = CliRunner()
    runner.invoke(cli.log_commands.createlog, ['123', 'non_existant_file.json'])

    assert not mocked_create_log.called


@patch('lecli.log.api.create_log')
@patch('os.path.exists', MagicMock(return_value=True))
@patch('os.path.isfile', MagicMock(return_value=False))
def test_not_a_file(mocked_create_log):
    runner = CliRunner()
    runner.invoke(cli.log_commands.createlog, ['123', 'not_a_file'])

    assert not mocked_create_log.called


@patch('lecli.logset.api.get_logsets')
def test_get_logsets(mocked_get_logsets):
    runner = CliRunner()
    runner.invoke(cli.logset_commands.getlogsets)

    mocked_get_logsets.assert_called_once()


@patch('lecli.logset.api.get_logset')
def test_get_logset(mocked_get_logset):
    runner = CliRunner()
    runner.invoke(cli.logset_commands.getlogset, ['1234'])

    mocked_get_logset.assert_called_once_with('1234')


@patch('lecli.logset.api.create_logset')
def test_create_logset_with_name(mocked_create_logset):
    runner = CliRunner()
    runner.invoke(cli.logset_commands.createlogset, ['-n', 'Test Logset'])

    mocked_create_logset.assert_called_once_with('Test Logset', None)


@patch('lecli.logset.api.rename_logset')
def test_rename_logset(mocked_rename_logset):
    runner = CliRunner()
    runner.invoke(cli.logset_commands.renamelogset, ['123', 'new_name'])

    mocked_rename_logset.assert_called_once_with('123', 'new_name')


@patch('lecli.logset.api.add_log')
def test_add_log_to_logset(mocked_add_log_to_logset):
    runner = CliRunner()
    runner.invoke(cli.logset_commands.updatelogset, ['add_log','123', 'abc'])

    mocked_add_log_to_logset.assert_called_once_with('123', 'abc')


@patch('lecli.logset.api.delete_log')
def test_remove_log_from_logset(mocked_delete_log_from_logset):
    runner = CliRunner()
    runner.invoke(cli.logset_commands.updatelogset, ['delete_log','123', 'abc'])

    mocked_delete_log_from_logset.assert_called_once_with('123', 'abc')


@patch('lecli.logset.api.delete_logset')
def test_delete_logset(mocked_delete_logset):
    runner = CliRunner()
    runner.invoke(cli.logset_commands.deletelogset, ['123'])

    mocked_delete_logset.assert_called_once_with('123')


@patch('lecli.logset.api.replace_logset')
def test_replace_logset(mocked_replace_logset):
    runner = CliRunner()
    with open('logset.json', 'w') as f:
        f.write('{"logset": {"id": "ba2b371a-87fa-40ee-97fd-e9b0d2424b2f","name": "new logset"}}')

    runner.invoke(cli.logset_commands.replacelogset, ['1234', 'logset.json'])

    mocked_replace_logset.assert_called_once()
    try:
        os.remove('logset.json')
    except OSError:
        pass


@patch('lecli.api_key.api.create')
def test_create_apikey(mocked_create_apikey):
    runner = CliRunner()
    with open('file.json', 'w') as f:
        f.write('{"test": {"key": "value"}}')

    runner.invoke(cli.api_key_commands.create_api_key, ['file.json'])
    mocked_create_apikey.assert_called_once()
    try:
        os.remove('file.json')
    except OSError:
        pass


@patch('lecli.api_key.api.delete')
def test_delete_apikey(mocked_delete_apikey):
    runner = CliRunner()
    runner.invoke(cli.api_key_commands.delete_api_key, ['123'])

    mocked_delete_apikey.assert_called_once_with('123')


@patch('lecli.api_key.api.update')
def test_enable_apikey(mocked_update_apikey):
    runner = CliRunner()
    runner.invoke(cli.api_key_commands.update_api_key, ['123', '--enable'])

    mocked_update_apikey.assert_called_once_with('123', True)


@patch('lecli.api_key.api.update')
def test_disable_apikey(mocked_update_apikey):
    runner = CliRunner()
    runner.invoke(cli.api_key_commands.update_api_key, ['123', '--disable'])

    mocked_update_apikey.assert_called_once_with('123', False)
