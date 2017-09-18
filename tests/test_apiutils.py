import ConfigParser
import hmac
import uuid

import pytest
from mock import patch, Mock

from lecli import api_utils

ID_WITH_VALID_LENGTH = str(uuid.uuid4())
ID_WITH_INVALID_LENGTH = str(uuid.uuid4()) + 'invalid'
MOCK_API_URL = 'http://mydummylink.com'


def test_gensignature():
    with patch.object(hmac.HMAC, 'digest', return_value='digest_output'):
        api_key = ID_WITH_VALID_LENGTH
        date = 'date'
        content_type = 'content_type'
        request_method = 'method'
        request_body = 'body'
        query_path = 'path'

        signature = api_utils.gensignature(api_key, date, content_type, request_method, request_body, query_path)

        assert signature == 'digest_output'


@patch('lecli.api_utils.get_ro_apikey')
def test_generate_headers_ro(mocked_ro_apikey):
    mocked_ro_apikey.return_value = ID_WITH_VALID_LENGTH

    headers = api_utils.generate_headers(api_key_type='ro')

    assert "x-api-key" in headers
    assert headers["x-api-key"] == ID_WITH_VALID_LENGTH


@patch('lecli.api_utils.get_rw_apikey')
def test_generate_header_rw(mocked_rw_apikey):
    mocked_rw_apikey.return_value = ID_WITH_VALID_LENGTH

    headers = api_utils.generate_headers(api_key_type='rw')

    assert 'x-api-key' in headers
    assert headers['x-api-key'] == ID_WITH_VALID_LENGTH


@patch('lecli.api_utils.get_owner_apikey')
@patch('lecli.api_utils.get_owner_apikey_id')
def test_generate_header_owner(mocked_owner_apikey, mocked_owner_apikey_id):
    mocked_owner_apikey.return_value = ID_WITH_VALID_LENGTH
    mocked_owner_apikey_id.return_value = ID_WITH_VALID_LENGTH
    headers = api_utils.generate_headers(api_key_type='owner', body='', method="GET", action="action")

    assert 'Date' in headers
    assert 'authorization-api-key' in headers
    assert ID_WITH_VALID_LENGTH in headers['authorization-api-key']


@patch('lecli.api_utils.get_ro_apikey')
def test_generate_headers_user_agent(mocked_ro_apikey):
    mocked_ro_apikey.return_value = ID_WITH_VALID_LENGTH
    headers = api_utils.generate_headers(api_key_type='ro')
    assert "User-Agent" in headers
    assert headers['User-Agent'] == 'lecli'


def test_get_valid_ro_apikey():
    with patch.object(ConfigParser.ConfigParser, 'get', return_value=ID_WITH_VALID_LENGTH):
        ro_api_key = api_utils.get_ro_apikey()

        assert ro_api_key == ID_WITH_VALID_LENGTH


def raise_no_option_error_on_read_only_key(*args):
    if args[1] == 'ro_api_key':
        raise ConfigParser.NoOptionError('option', 'section')
    elif args[1] == 'rw_api_key':
        return ID_WITH_VALID_LENGTH


@patch.object(ConfigParser.ConfigParser, 'get', side_effect=raise_no_option_error_on_read_only_key)
def test_get_rw_apikey_if_ro_apikey_not_present(mock_get):
    read_write_api_key = ID_WITH_VALID_LENGTH
    api_key = api_utils.get_ro_apikey()
    assert api_key == read_write_api_key


def test_get_invalid_ro_apikey(capsys):
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=ID_WITH_INVALID_LENGTH):
        with pytest.raises(SystemExit):
            ro_api_key = api_utils.get_ro_apikey()
            out, err = capsys.readouterr()

            assert ro_api_key is None
            assert ID_WITH_INVALID_LENGTH in out
            assert 'is not of correct length' in out


def test_get_valid_rw_apikey():
    with patch.object(ConfigParser.ConfigParser, 'get', return_value=ID_WITH_VALID_LENGTH):
        rw_api_key = api_utils.get_rw_apikey()

        assert rw_api_key == ID_WITH_VALID_LENGTH


def test_get_invalid_rw_apikey(capsys):
    with patch.object(ConfigParser.ConfigParser, 'get', return_value=ID_WITH_INVALID_LENGTH):
        with pytest.raises(SystemExit):
            api_utils.load_config = Mock()
            result = api_utils.get_rw_apikey()
            out, err = capsys.readouterr()

            assert result is None
            assert ID_WITH_INVALID_LENGTH in out
            assert 'is not of correct length' in out


def test_get_valid_owner_apikey():
    with patch.object(ConfigParser.ConfigParser, 'get', return_value=ID_WITH_VALID_LENGTH):
        owner_api_key = api_utils.get_owner_apikey()

        assert owner_api_key == ID_WITH_VALID_LENGTH


def test_get_invalid_owner_apikey(capsys):
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=ID_WITH_INVALID_LENGTH):
        with pytest.raises(SystemExit):
            api_utils.load_config = Mock()
            result = api_utils.get_owner_apikey()
            out, err = capsys.readouterr()

            assert result is None
            assert ID_WITH_INVALID_LENGTH in out
            assert 'is not of correct length' in out


def test_get_valid_owner_apikey_id():
    with patch.object(ConfigParser.ConfigParser, 'get', return_value=ID_WITH_VALID_LENGTH):
        owner_api_key_id = api_utils.get_owner_apikey_id()

        assert owner_api_key_id == ID_WITH_VALID_LENGTH


def test_get_invalid_owner_apikey_id(capsys):
    with patch.object(ConfigParser.ConfigParser, 'get', return_value=ID_WITH_INVALID_LENGTH):
        with pytest.raises(SystemExit):
            api_utils.load_config = Mock()
            result = api_utils.get_owner_apikey_id()
            out, err = capsys.readouterr()

            assert result is None
            assert ID_WITH_INVALID_LENGTH in out
            assert 'is not of correct length' in out


def test_get_valid_account_resource_id():
    with patch.object(ConfigParser.ConfigParser, 'get', return_value=ID_WITH_VALID_LENGTH):
        account_resource_id = api_utils.get_account_resource_id()

        assert account_resource_id == ID_WITH_VALID_LENGTH


def test_get_invalid_account_resource_id(capsys):
    with patch.object(ConfigParser.ConfigParser, 'get',
                      return_value=ID_WITH_INVALID_LENGTH):
        with pytest.raises(SystemExit):
            result = api_utils.get_account_resource_id()
            out, err = capsys.readouterr()

            assert result is None
            assert ID_WITH_INVALID_LENGTH in out
            assert 'is not of correct length' in out


def test_get_valid_named_group_key():
    with patch.object(ConfigParser.ConfigParser, 'items',
                      return_value=[('test-log-group-favs', ID_WITH_VALID_LENGTH)]):
        logkeys = api_utils.get_named_logkey_group('test-log-group-favs')
        assert logkeys == filter(None, ID_WITH_VALID_LENGTH.splitlines())


def test_case_insensitivity_of_named_groups_key():
    with patch.object(ConfigParser.ConfigParser, 'items',
                      return_value=[('test-log-group-favs', '')]):
        logkeys = api_utils.get_named_logkey_group('TEST-log-group-favs')
        assert logkeys == filter(None, ''.splitlines())


def test_get_invalid_named_group_key(capsys):
    with patch.object(ConfigParser.ConfigParser, 'items',
                      return_value=[('test-log-group-favs', ["test-log-key1", "test-log-key2"])]):
        with pytest.raises(SystemExit):
            nick_to_query = 'test-log-group-favs-invalid'
            result = api_utils.get_named_logkey_group(nick_to_query)
            out, err = capsys.readouterr()

            assert result is None
            assert nick_to_query in out
            assert 'was not found' in out


@patch('ConfigParser.ConfigParser')
def test_replace_loggroup_section(mocked_configparser_class):
    loggroups_section = api_utils.LOGGROUPS_SECTION
    config_parser_mock = mocked_configparser_class.return_value
    config_parser_mock.add_section(loggroups_section)
    with patch.object(api_utils.CONFIG, 'items',
                       return_value=[('test-log-group-favs', ["test-log-key1", "test-log-key2"])]):
        api_utils.replace_loggroup_section()
        assert not api_utils.CONFIG.has_section(loggroups_section)
        assert config_parser_mock.has_section('CLI_Favorites')


@patch('lecli.api_utils.get_api_url')
def test_generate_api_url(mocked_api_url):
    mocked_api_url.return_value = MOCK_API_URL

    result = api_utils.get_api_url()

    assert MOCK_API_URL in result


def test_default_api_url():
    result = api_utils.get_api_url()

    assert "https://rest.logentries.com" in result


def test_combine_objects():
    left = {
        "log": {
            "id": "21dd21e7-708a-4bc4-bf45-ffbc78190ecd",
            "logsets_info": [],
            "name": "test_log_old",
            "structures": [],
            "tokens": [],
            "user_data": {}
        }
    }

    right = {
        "log": {
            "name": "test_log_new",
            "structures": [],
            "tokens": [],
            "user_data": {},
            "logsets_info": [{
                "id": "e227f890-7742-47b4-86b2-5ff1d345397e",
                "name": "test_logset"
            }]
        }
    }

    expected_result = {
        "log": {
            "id": "21dd21e7-708a-4bc4-bf45-ffbc78190ecd",
            "logsets_info": [{
                "id": "e227f890-7742-47b4-86b2-5ff1d345397e",
                "name": "test_logset"
            }],
            "name": "test_log_new",
            "structures": [],
            "tokens": [],
            "user_data": {}
        }
    }

    result = api_utils.combine_objects(left, right)

    assert result == expected_result
