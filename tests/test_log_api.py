import json
import uuid

import httpretty
import pytest

from mock import patch

from lecli.log import api

ID_WITH_VALID_LENGTH = str(uuid.uuid4())
MOCK_API_URL = 'http://mydummylink.com'
LOG_RESPONSE = {
    "log" : {
        "id" : "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "name" : "Test Log",
        "logsets_info" : [{
            "id" : "XXXXXXXX-ABCD-ABCD-ABCD-XXXXXXXXXXXX",
            "name" : "Test Logset 1",
            "links" : {
                "rel" : "Self",
                "href" : "http://mydummyurl.com/management/logsets/XXXXXXXX-ABCD-ABCD-ABCD-XXXXXXXXXXXX"
            }
        },
        {
            "id" : "XXXXXXXX-DCBA-DCBA-DCBA-XXXXXXXXXXXX",
            "name" : "Test Logset 2",
            "links" : {
                "rel" : "Self",
                "href" : "http://mydummyurl.com/management/logsets/XXXXXXXX-DCBA-DCBA-DCBA-XXXXXXXXXXXX"
            }
        }],
        "source_type" : "token",
        "token_seed" : "12345678-abcd-efgh-ijkl-12345678",
        "tokens": [{}],
        "structures" : [{}],
        "user_data": {
            "LocationDescription" : "All logs for DC1",
            "le_hostname" : "testhost"
        }
    }
}


@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.log.api._url')
def test_get_logs(mocked_url, mocked_ro_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_ro_apikey.return_value = ID_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.GET, MOCK_API_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({}))

    api.get_logs()
    out, err = capsys.readouterr()
    assert not err


@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.log.api._url')
def test_get_log(mocked_url, mocked_ro_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_ro_apikey.return_value = ID_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.GET, MOCK_API_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps(LOG_RESPONSE))

    api.get_log(ID_WITH_VALID_LENGTH)
    out, err = capsys.readouterr()

    assert not err


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.log.api._url')
def test_create_log_with_default_source_type(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = ID_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.POST, MOCK_API_URL,
                           status=201,
                           body=json.dumps(LOG_RESPONSE),
                           content_type='application/json')

    api.create_log("Test Log", None)
    out, err = capsys.readouterr()

    assert 'Test Log' in out
    assert 'token' in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.log.api._url')
def test_create_log_with_source_type(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = ID_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.POST, MOCK_API_URL,
                           status=201,
                           body='{"log": {"name": "test log","id": "2caec19c-d8a2-40ef-9c1e-91e89157fe28",'
                                '"source_type": "syslog","logsets_info": [{"id": "20a9b70b-e70c-4cb5-a4f6-0e40b60b7118","name": "logset"}]}}',
                           content_type = 'application/json')

    api.create_log("test log", None)
    out, err = capsys.readouterr()

    assert 'test log' in out
    assert 'syslog' in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.log.api._url')
def test_delete_log(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = ID_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.DELETE, MOCK_API_URL, status=204)
    log_id = str(uuid.uuid4())
    api.delete_log(log_id)

    out, err = capsys.readouterr()
    assert "Deleted log with id: %s" % log_id in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.log.api._url')
def test_rename_log(mocked_url, mocked_rw_apikey, mocked_ro_apikey, capsys):
    test_log_id = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = ID_WITH_VALID_LENGTH
    mocked_ro_apikey.return_value = ID_WITH_VALID_LENGTH

    request_body = '{"log": {"name": "test.log", "logsets_info": [], "source_type": "token"}}'
    expected_result = '{"log": {"name": "new_test_log_name", "logsets_info": [], "source_type": "token"}}'

    httpretty.register_uri(httpretty.GET, MOCK_API_URL,
                           status=200,
                           content_type='application/json',
                           body=request_body)

    httpretty.register_uri(httpretty.PUT, MOCK_API_URL, status=200,
                           body = expected_result, content_type='application/json')

    new_name_for_log = "new_test_log_name"
    api.rename_log(test_log_id, new_name_for_log)
    out, err = capsys.readouterr()

    assert new_name_for_log in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.log.api._url')
def test_replace_log(mocked_url, mocked_rw_apikey, capsys):
    log_id = str(uuid.uuid4())

    request_body = '{"log": {"name": "test.log", "logsets_info": [], "source_type": "token"}}'
    mocked_rw_apikey.return_value = ID_WITH_VALID_LENGTH
    mocked_url.return_value = '', MOCK_API_URL

    httpretty.register_uri(httpretty.PUT, MOCK_API_URL, status=200, body=request_body,
                           content_type='application/json')

    api.replace_log(log_id, params=request_body)

    out, err = capsys.readouterr()
    assert "test.log" in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.log.api._url')
@patch('lecli.logset.api._url')
def test_update_log(logset_url, log_url, mocked_ro_apikey, mocked_rw_apikey, capsys):
    test_log_id = str(uuid.uuid4())
    log_url.return_value = '', MOCK_API_URL
    logset_url.return_value = '', MOCK_API_URL

    mocked_rw_apikey.return_value = ID_WITH_VALID_LENGTH
    mocked_ro_apikey.return_value = ID_WITH_VALID_LENGTH

    request_body = '{"log": {"name": "test.log", "logsets_info": [], "source_type": "token"}}'
    expected_result = '{"log": {"name": "test.log", ' \
                      '"logsets_info": [{"id": "e227f890-7742-47b4-86b2-5ff1d345397e",' \
                      '"name": "test_logset"}], "source_type": "token"}}'

    httpretty.register_uri(httpretty.GET, MOCK_API_URL, status=200,
                           content_type='application/json', body=request_body)
    httpretty.register_uri(httpretty.GET, MOCK_API_URL, status=200,
                           content_type='application/json', body=request_body)
    httpretty.register_uri(httpretty.PUT, MOCK_API_URL, status=200,
                           content_type='application/json', body=expected_result)

    logset_info = {
        "logsets_info": [
            {
                "id": "e227f890-7742-47b4-86b2-5ff1d345397e",
                "name": "test_logset"
            }
        ]
    }

    api.update_log(test_log_id, logset_info)
    out, err = capsys.readouterr()

    assert "test_logset" in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.log.api._url')
def test_duplicate_log_id(mocked_url, mocked_rw_apikey):
    with pytest.raises(Exception) as exception:
        mocked_url.return_value = '', MOCK_API_URL
        mocked_rw_apikey.return_value = ID_WITH_VALID_LENGTH
        httpretty.register_uri(httpretty.POST, MOCK_API_URL, status=409, content_type='application/json')

        api.create_log('existing log')

        assert exception.value.message=='409'