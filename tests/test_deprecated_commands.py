from click.testing import CliRunner
from mock import patch

from examples import misc_examples as misc_ex
from lecli import deprecated_commands


@patch('lecli.user.api.get_owner')
def test_get_owner(mocked_get_owner):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.getowner)

    assert "This method is deprecated" in result.output
    mocked_get_owner.assert_called_once_with()


@patch('lecli.user.api.delete_user')
def test_userdel(mocked_delete_user):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.deleteuser, input=None)

    assert "This method is deprecated" in result.output
    assert "Example usage: lecli delete user -u 12345678-aaaa-bbbb-1234-1234cb123456" in result.output

    runner.invoke(deprecated_commands.deleteuser, ['-u', misc_ex.TEST_USER_KEY])
    assert mocked_delete_user.called


@patch('lecli.user.api.add_new_user')
def test_useradd(mocked_add_new_user):
    first = "first"
    last = "last"
    email = "email"

    runner = CliRunner()
    result = runner.invoke(deprecated_commands.adduser, ['-f', first, '-l', last, '-e', email], input='y')

    assert "This method is deprecated" in result.output
    mocked_add_new_user.assert_called_once_with(first, last, email)


@patch('lecli.user.api.list_users')
def test_userlist(mocked_list_users):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.listusers)

    assert "This method is deprecated" in result.output
    mocked_list_users.assert_called_once_with()


@patch('lecli.query.api.get_recent_events')
def test_recentevents(mocked_recent_events):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.recentevents, [str(misc_ex.TEST_LOG_GROUP)])

    assert "This method is deprecated" in result.output
    assert mocked_recent_events.called


@patch('lecli.query.api.get_recent_events')
def test_recentevents_with_relative_range(mocked_recent_events):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.recentevents, [str(misc_ex.TEST_LOG_GROUP), '-r', misc_ex.RELATIVE_TIME])

    assert "This method is deprecated" in result.output
    assert mocked_recent_events.called


@patch('lecli.query.api.get_events')
def test_events(mocked_get_events):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.events, [str(misc_ex.TEST_LOG_GROUP), '-f', misc_ex.TIME_FROM, '-t',
                               misc_ex.TIME_TO])

    assert "This method is deprecated" in result.output
    assert mocked_get_events.called


@patch('lecli.query.api.get_events')
def test_events_with_relative_range(mocked_get_events):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.events, [str(misc_ex.TEST_LOG_GROUP), '-r', misc_ex.RELATIVE_TIME])

    assert "This method is deprecated" in result.output
    assert mocked_get_events.called


@patch('lecli.team.api.get_teams')
def test_get_teams(mocked_get_teams):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.getteams)

    assert "This method is deprecated" in result.output
    assert mocked_get_teams.called


@patch('lecli.team.api.get_team')
def test_get_team(mocked_get_team):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.getteam, [str(misc_ex.TEST_TEAM_ID)])

    assert "This method is deprecated" in result.output
    assert mocked_get_team.called


@patch('lecli.team.api.create_team')
def test_create_team(mocked_create_team):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.createteam, ["test_team_name"])

    assert "This method is deprecated" in result.output
    assert mocked_create_team.called


@patch('lecli.team.api.delete_team')
def test_delete_team(mocked_delete_team):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.deleteteam, [str(misc_ex.TEST_TEAM_ID)])

    assert "This method is deprecated" in result.output
    assert mocked_delete_team.called


@patch('lecli.team.api.rename_team')
def test_rename_team(mocked_rename_team):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.renameteam, [str(misc_ex.TEST_TEAM_ID), "new_name"])

    assert "This method is deprecated" in result.output
    assert mocked_rename_team.called


@patch('lecli.team.api.add_user_to_team')
def test_add_user_to_team(mocked_add_user):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.addusertoteam, [str(misc_ex.TEST_TEAM_ID), "test_user_name"])

    assert "This method is deprecated" in result.output
    assert mocked_add_user.called


@patch('lecli.usage.api.get_usage')
def test_add_user_to_team(mocked_get_usage):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.usage, ['-s', misc_ex.USAGE_DATE_FROM, '-e', misc_ex.USAGE_DATE_TO])

    assert "This method is deprecated" in result.output
    assert mocked_get_usage.called


@patch('lecli.saved_query.api.create_saved_query')
def test_create_saved_query(mocked_create_saved_query):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.createsavedquery, ['new_saved_query', 'where(/*/)', '-f', 10, '-t', 1000])

    assert "This method is deprecated" in result.output
    assert mocked_create_saved_query.called


@patch('lecli.saved_query.api.update_saved_query')
def test_update_saved_query(mocked_update_saved_query):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.updatesavedquery, ['123456789012345678901234567890123456', '-f', 10, '-t',
                                         1000])

    assert "This method is deprecated" in result.output
    assert mocked_update_saved_query.called


@patch('lecli.saved_query.api.get_saved_query')
def test_get_saved_query(mocked_get_saved_query):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.getsavedquery, ['123456789012345678901234567890123456'])

    assert "This method is deprecated" in result.output
    assert mocked_get_saved_query.called


@patch('lecli.saved_query.api.get_saved_query')
def test_get_saved_queries(mocked_get_saved_queries):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.getsavedqueries)

    assert "This method is deprecated" in result.output
    assert mocked_get_saved_queries.called


@patch('lecli.saved_query.api.get_saved_query')
def test_get_saved_query(mocked_get_saved_query):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.getsavedquery, ['12341234'])

    assert "This method is deprecated" in result.output
    assert mocked_get_saved_query.called


@patch('lecli.saved_query.api.delete_saved_query')
def test_delete_saved_query(mocked_delete_saved_query):
    runner = CliRunner()
    result = runner.invoke(deprecated_commands.deletesavedquery, ['123456789012345678901234567890123456'])

    assert "This method is deprecated" in result.output
    assert mocked_delete_saved_query.called
