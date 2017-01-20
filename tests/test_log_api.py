import json

import httpretty
import pytest
from mock import patch
from mock import MagicMock

from lecli import log_api
from examples import misc_examples as misc_ex
from examples import response_examples as resp_ex

@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.log_api._url')
def test_get_logs(mocked_url, mocked_ro_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGAPI_URL
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGAPI_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({'logs': resp_ex.log_response}))

    log_api.get_logs()
    out, err = capsys.readouterr()

    assert '"id": "12345"' in out

@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.log_api._url')
def test_get_log(mocked_url, mocked_ro_apikey, capsys):
    log_id = misc_ex.TEST_LOG_RESOURCE_ID
    mocked_url.return_value = misc_ex.MOCK_LOGAPI_URL
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGAPI_URL + '/' + log_id,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({'log': resp_ex.log_response}))

    log_api.get_log(log_id)
    out, err = capsys.readouterr()

    assert '"id": "12345"' in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.log_api._url')
def test_create_log_with_default_source_type(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_LOGAPI_URL,
                           status=201,
                           body=json.dumps({'logs': resp_ex.log_response}),
                           content_type='application/json')

    log_api.create_log("Test Log", None)
    out, err = capsys.readouterr()

    assert 'Test Log' in out
    assert 'token' in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.log_api._url')
def test_create_log_with_source_type(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_LOGAPI_URL,
                           status=201,
                           body='{"log": {"name": "test log","id": "2caec19c-d8a2-40ef-9c1e-91e89157fe28",'
                                  '"source_type": "syslog","logsets_info": [{"id": "20a9b70b-e70c-4cb5-a4f6-0e40b60b7118","name": "logset"}]}}',
                           content_type='application/json')

    log_api.create_log("test log", None)
    out, err = capsys.readouterr()

    assert 'test log' in out
    assert "syslog" in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.log_api._url')
def test_delete_log(mocked_url, mocked_rw_apikey, capsys):

    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_url.return_value = misc_ex.MOCK_LOGAPI_URL

    dest_url = misc_ex.MOCK_LOGAPI_URL + '/' + str(misc_ex.TEST_LOG_RESOURCE_ID)
    httpretty.register_uri(httpretty.DELETE, dest_url, status=204)

    log_api.delete_log(misc_ex.TEST_LOG_RESOURCE_ID)

    out, err = capsys.readouterr()
    assert "Deleted log with id: 12345" in out

@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.log_api._url')
def test_rename_log(mocked_url, mocked_rw_apikey, mocked_ro_apikey, capsys):
    test_log_id = misc_ex.TEST_LOG_RESOURCE_ID
    mocked_url.return_value = misc_ex.MOCK_LOGAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    request_body = '{"log": { "name": "test.log","logsets_info": [],"source_type": "token"}}'
    expected_result = '{"log": { "name": "new_test_log_name","logsets_info": [],"source_type": "token"}}'

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGAPI_URL + '/' + test_log_id,
                           status=200,
                           content_type='application/json',
                           body=request_body)

    httpretty.register_uri(httpretty.PUT,
                           misc_ex.MOCK_LOGAPI_URL + "/" + test_log_id,
                           status=200,
                           body = expected_result,
                           content_type='application/json')

    new_name_for_log = "new_test_log_name"
    log_api.rename_log(test_log_id, new_name_for_log)
    out, err = capsys.readouterr()

    assert new_name_for_log in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.log_api._url')
def test_replace_log(mocked_url, mocked_rw_apikey, capsys):
    log_id = misc_ex.TEST_LOG_RESOURCE_ID

    request_body = '{"log": { "name": "test.log","logsets_info": [],"source_type": "token"}}'
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_url.return_value = misc_ex.MOCK_LOGAPI_URL

    dest_url = misc_ex.MOCK_LOGAPI_URL + '/' + str(misc_ex.TEST_LOG_RESOURCE_ID)

    httpretty.register_uri(httpretty.PUT, dest_url, status=200, body = request_body, content_type='application/json')

    log_api.replace_log(log_id, params=request_body)

    out, err = capsys.readouterr()
    assert "test.log" in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.log_api._url')
def test_duplicate_log_id(mocked_url, mocked_rw_apikey):
    with pytest.raises(Exception) as exception:
        mocked_url.return_value = misc_ex.MOCK_LOGAPI_URL
        mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
        httpretty.register_uri(httpretty.POST, misc_ex.MOCK_LOGAPI_URL,
                               status=409,
                               content_type='application/json')

        log_api.create_log('existing log')

        assert exception.value.message=="409"
