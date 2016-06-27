from click.testing import CliRunner
from mock import patch

from examples import misc_examples as misc_ex
from lecli import lecli


@patch('lecli.userapi.get_owner')
def test_get_owner(mocked_get_owner):
    runner = CliRunner()
    runner.invoke(lecli.getowner)

    mocked_get_owner.assert_called_once_with()


@patch('lecli.userapi.delete_user')
def test_userdel(mocked_delete_user):
    runner = CliRunner()
    result = runner.invoke(lecli.userdel, input=None)

    assert result.output == "Example usage: lecli userdel -u 12345678-aaaa-bbbb-1234-1234cb123456\n"

    runner.invoke(lecli.userdel, ['-u', misc_ex.TEST_USER_ID])
    mocked_delete_user.assert_called_once_with(misc_ex.TEST_USER_ID)


@patch('lecli.userapi.add_new_user')
def test_useradd(mocked_add_new_user):
    first = "first"
    last = "last"
    email = "email"

    runner = CliRunner()
    runner.invoke(lecli.useradd, ['-f', first, '-l', last, '-e', email], input='y')
    mocked_add_new_user.assert_called_once_with(first, last, email)


@patch('lecli.userapi.list_users')
def test_userlist(mocked_list_users):
    runner = CliRunner()
    runner.invoke(lecli.userlist)
    mocked_list_users.assert_called_once_with()


@patch('lecli.queryapi.get_recent_events')
def test_recentevents(mocked_recent_events):
    runner = CliRunner()
    runner.invoke(lecli.recentevents, [str(misc_ex.TEST_LOG_GROUP)])

    assert mocked_recent_events.called


@patch('lecli.queryapi.get_events')
def test_events(mocked_get_events):
    runner = CliRunner()
    runner.invoke(lecli.events, [str(misc_ex.TEST_LOG_GROUP), '-f', misc_ex.TIME_FROM, '-t', misc_ex.TIME_TO])

    assert mocked_get_events.called


@patch('lecli.queryapi.post_query')
def test_query(mocked_post_query):
    runner = CliRunner()
    runner.invoke(lecli.query, [str(misc_ex.TEST_LOG_GROUP), '-l', misc_ex.TEST_QUERY, '-f', misc_ex.TIME_FROM, '-t',
                                misc_ex.TIME_TO])

    assert mocked_post_query.called
