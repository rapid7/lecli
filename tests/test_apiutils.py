import ConfigParser
import hmac

import pytest
from mock import patch, Mock

from lecli import apiutils
from examples import misc_examples as misc_ex


def test_gensignature():
    with patch.object(hmac.HMAC, 'digest', return_value='digest_output'):
        api_key = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
        date = 'date'
        content_type = 'content_type'
        request_method = 'method'
        request_body = 'body'
        query_path = 'path'

        signature = apiutils.gensignature(api_key, date, content_type, request_method, request_body, query_path)

        assert signature == 'digest_output'


@patch('lecli.apiutils.get_ro_apikey')
def test_generate_headers_ro(mocked_ro_apikey):
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    headers = apiutils.generate_headers(api_key_type='ro')

    assert "x-api-key" in headers
    assert headers["x-api-key"] == misc_ex.TEST_APIKEY_WITH_VALID_LENGTH


@patch('lecli.apiutils.get_rw_apikey')
def test_generate_header_rw(mocked_rw_apikey):
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    headers = apiutils.generate_headers(api_key_type='rw')

    assert 'x-api-key' in headers
    assert headers['x-api-key'] == misc_ex.TEST_APIKEY_WITH_VALID_LENGTH


@patch('lecli.apiutils.get_owner_apikey')
@patch('lecli.apiutils.get_owner_apikey_id')
def test_generate_header_owner(mocked_owner_apikey, mocked_owner_apikey_id):
    mocked_owner_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_owner_apikey_id.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    headers = apiutils.generate_headers(api_key_type='owner', body='', method="GET", action="action")

    assert 'Date' in headers
    assert 'authorization-api-key' in headers
    assert misc_ex.TEST_APIKEY_WITH_VALID_LENGTH in headers['authorization-api-key']


@patch('lecli.apiutils.get_ro_apikey')
def test_generate_headers_user_agent(mocked_ro_apikey):
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    headers = apiutils.generate_headers(api_key_type='ro')
    assert "User-Agent" in headers
    assert headers['User-Agent'] == 'lecli'


def test_get_valid_ro_apikey():
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=misc_ex.TEST_APIKEY_WITH_VALID_LENGTH):
        ro_api_key = apiutils.get_ro_apikey()

        assert ro_api_key == misc_ex.TEST_APIKEY_WITH_VALID_LENGTH


def test_get_invalid_ro_apikey(capsys):
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=misc_ex.TEST_APIKEY_WITH_INVALID_LENGTH):
        with pytest.raises(SystemExit):
            ro_api_key = apiutils.get_ro_apikey()
            out, err = capsys.readouterr()

            assert ro_api_key is None
            assert misc_ex.TEST_APIKEY_WITH_INVALID_LENGTH in out
            assert 'is not of correct length' in out


def test_get_valid_rw_apikey():
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=misc_ex.TEST_APIKEY_WITH_VALID_LENGTH):
        rw_api_key = apiutils.get_rw_apikey()

        assert rw_api_key == misc_ex.TEST_APIKEY_WITH_VALID_LENGTH


def test_get_invalid_rw_apikey(capsys):
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=misc_ex.TEST_APIKEY_WITH_INVALID_LENGTH):
        with pytest.raises(SystemExit):
            apiutils.load_config = Mock()
            result = apiutils.get_rw_apikey()
            out, err = capsys.readouterr()

            assert result is None
            assert misc_ex.TEST_APIKEY_WITH_INVALID_LENGTH in out
            assert 'is not of correct length' in out


def test_get_valid_owner_apikey():
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=misc_ex.TEST_APIKEY_WITH_VALID_LENGTH):
        owner_api_key = apiutils.get_owner_apikey()

        assert owner_api_key == misc_ex.TEST_APIKEY_WITH_VALID_LENGTH


def test_get_invalid_owner_apikey(capsys):
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=misc_ex.TEST_APIKEY_WITH_INVALID_LENGTH):
        with pytest.raises(SystemExit):
            apiutils.load_config = Mock()
            result = apiutils.get_owner_apikey()
            out, err = capsys.readouterr()

            assert result is None
            assert misc_ex.TEST_APIKEY_WITH_INVALID_LENGTH in out
            assert 'is not of correct length' in out


def test_get_valid_owner_apikey_id():
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=misc_ex.TEST_APIKEY_WITH_VALID_LENGTH):
        owner_api_key_id = apiutils.get_owner_apikey_id()

        assert owner_api_key_id == misc_ex.TEST_APIKEY_WITH_VALID_LENGTH


def test_get_invalid_owner_apikey_id(capsys):
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=misc_ex.TEST_APIKEY_WITH_INVALID_LENGTH):
        with pytest.raises(SystemExit):
            apiutils.load_config = Mock()
            result = apiutils.get_owner_apikey_id()
            out, err = capsys.readouterr()

            assert result is None
            assert misc_ex.TEST_APIKEY_WITH_INVALID_LENGTH in out
            assert 'is not of correct length' in out


def test_get_valid_account_resource_id():
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=misc_ex.TEST_APIKEY_WITH_VALID_LENGTH):
        account_resource_id = apiutils.get_account_resource_id()

        assert account_resource_id == misc_ex.TEST_APIKEY_WITH_VALID_LENGTH


def test_get_invalid_account_resource_id(capsys):
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=misc_ex.TEST_APIKEY_WITH_INVALID_LENGTH):
        with pytest.raises(SystemExit):
            result = apiutils.get_account_resource_id()
            out, err = capsys.readouterr()

            assert result is None
            assert misc_ex.TEST_APIKEY_WITH_INVALID_LENGTH in out
            assert 'is not of correct length' in out


def test_get_valid_named_logkey():
    with patch.object(ConfigParser.ConfigParser, 'items', return_value=[('test-logkey-nick',
                                                                         misc_ex.TEST_LOG_KEY)]):
        logkey = apiutils.get_named_logkey('test-logkey-nick')
        assert logkey == (misc_ex.TEST_LOG_KEY,)


def test_case_insensitivity_of_named_logkey():
    with patch.object(ConfigParser.ConfigParser, 'items', return_value=[('test-logkey-nick',
                                                                         misc_ex.TEST_LOG_KEY)]):
        logkey = apiutils.get_named_logkey('TEST-logkey-nick')
        assert logkey == (misc_ex.TEST_LOG_KEY,)


def test_get_invalid_named_logkey(capsys):
    with patch.object(ConfigParser.ConfigParser, 'items', return_value=[('test-logkey-nick',
                                                                         misc_ex.TEST_LOG_KEY)]):
        with pytest.raises(SystemExit):
            nick_to_query = 'test-logkey-nick_invalid'
            logkey = apiutils.get_named_logkey(nick_to_query)
            out, err = capsys.readouterr()

            assert logkey is None
            assert nick_to_query in out
            assert 'was not found' in out


def test_get_valid_named_group_key():
    with patch.object(ConfigParser.ConfigParser, 'items',
                      return_value=[('test-log-group-nick', misc_ex.TEST_LOG_GROUP)]):
        logkeys = apiutils.get_named_logkey_group('test-log-group-nick')
        assert logkeys == filter(None, str(misc_ex.TEST_LOG_GROUP).splitlines())


def test_case_insensitivity_of_named_groups_key():
    with patch.object(ConfigParser.ConfigParser, 'items',
                      return_value=[('test-log-group-nick', misc_ex.TEST_LOG_GROUP)]):
        logkeys = apiutils.get_named_logkey_group('TEST-log-group-nick')
        assert logkeys == filter(None, str(misc_ex.TEST_LOG_GROUP).splitlines())


def test_get_invalid_named_group_key(capsys):
    with patch.object(ConfigParser.ConfigParser, 'items',
                      return_value=[('test-log-group-nick', ["test-log-key1", "test-log-key2"])]):
        with pytest.raises(SystemExit):
            nick_to_query = 'test-log-group-nick-invalid'
            result = apiutils.get_named_logkey_group(nick_to_query)
            out, err = capsys.readouterr()

            assert result is None
            assert nick_to_query in out
            assert 'was not found' in out
