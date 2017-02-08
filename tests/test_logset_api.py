import json
import httpretty
import pytest

from mock import patch
from examples import misc_examples as misc_ex
from examples import response_examples as resp_ex
from lecli.logset import api


@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.logset.api._url')
def test_get_logsets(mocked_url, mocked_ro_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGSETAPI_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps(resp_ex.logsets_response))

    api.get_logsets()
    out, err = capsys.readouterr()

    assert 'XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXXXXXX' in out


@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.logset.api._url')
def test_get_logset(mocked_url, mocked_ro_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGSETAPI_URL + '/XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXXXXXX',
                           status=200,
                           content_type='application/json',
                           body=json.dumps(resp_ex.logsets_response))

    api.get_logset('XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXXXXXX')
    out, err = capsys.readouterr()

    assert 'XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXXXXXX' in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_create_logset_with_name(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_LOGSETAPI_URL,
                           status=201,
                           content_type='application/json',
                           body=json.dumps(resp_ex.create_logset_response))

    api.create_logset('Test Logset')
    out, err = capsys.readouterr()

    assert 'Test Logset' in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_create_logset_from_file(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_LOGSETAPI_URL,
                           status=201,
                           content_type='application/json',
                           body=json.dumps(resp_ex.create_logset_response))

    params = {
        "logset": {
            "id": "abcd1234-abcd-0000-abcd-abcd1234",
            "name": "Test Logset"
        }
    }

    api.create_logset(params=params)
    out, err = capsys.readouterr()

    assert 'Test Logset' in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_create_logset_invalid_json(mocked_url, mocked_rw_apikey, capsys):
    with pytest.raises(SystemExit) as exit:
        mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
        mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

        httpretty.register_uri(httpretty.POST, misc_ex.MOCK_LOGSETAPI_URL,
                               status=400,
                               content_type='application/json',
                               body='Client Error: Bad Request for url: https://rest.logentries.com/management/logsets')

        invalid_params = {
            "logset": {
                "id": "12341234-XXXX-YYYY-XXXX-12341234",
                "unknown_field": "unknown value"
            }
        }

        api.create_logset(params=invalid_params)
        out, err = capsys.readouterr()

        assert exit.code is 1
        assert "Creating logset failed, status code: 400" in out


@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_rename_logset(mocked_url, mocked_rw_apikey, mocked_ro_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    response_body = '{"logset": {"id": "XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXX","logs_info": [],"name": "old logset name"}}'
    expected_result = '{"logset": {"id": "XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXX","logs_info": [],"name": "new logset name"}}'

    resource_url = misc_ex.MOCK_LOGSETAPI_URL + '/XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXX'

    httpretty.register_uri(httpretty.GET, resource_url,
                           status=200,
                           content_type='application/json',
                           body=response_body)

    httpretty.register_uri(httpretty.PUT, resource_url,
                           status=200,
                           content_type='application/json',
                           body=expected_result)

    api.rename_logset('XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXX', 'new logset name')
    out, err = capsys.readouterr()

    assert "new logset name" in out


@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_rename_unknown_logset(mocked_url, mocked_rw_apikey, mocked_ro_apikey, capsys):
    with pytest.raises(SystemExit) as exit:
        mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
        mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

        httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGSETAPI_URL + '/XXXXXXXX-XXXX-0000-XXXX-XXXXXXXX',
                               status=404,
                               content_type='application/json')

        api.rename_logset('XXXXXXXX-XXXX-0000-XXXX-XXXXXXXX', 'new name')
        out, err = capsys.readouterr()

        assert "404" in out
        assert exit.code is 1


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.logset.api._url')
def test_add_log_to_logset(mocked_url, mocked_ro_apikey, mocked_rw_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGSETAPI_URL + '/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX',
                           status=200,
                           content_type='application/json',
                           body=resp_ex.basic_logset_response)

    httpretty.register_uri(httpretty.PUT, misc_ex.MOCK_LOGSETAPI_URL + '/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX',
                           status=200,
                           content_type='application/json',
                           body=resp_ex.basic_logset_response_with_log)


    api.add_log('XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX', 'XXXXXXXX-ABCD-YYYY-DCBA-XXXXXXXXXXXX')
    out, err = capsys.readouterr()

    assert "XXXXXXXX-ABCD-YYYY-DCBA-XXXXXXXXXXXX" in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.logset.api._url')
def test_add_unknown_log_to_logset(mocked_url, mocked_ro_apikey, mocked_rw_apikey, capsys):
    with pytest.raises(SystemExit) as exit:
        mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
        mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
        mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

        httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGSETAPI_URL + '/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX',
                               status=200,
                               content_type='application/json',
                               body=resp_ex.basic_logset_response)

        httpretty.register_uri(httpretty.PUT, misc_ex.MOCK_LOGSETAPI_URL + '/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX',
                               status=400,
                               content_type='application/json')

        api.add_log('XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX', 'unknown_log')
        out, err = capsys.readouterr()

        assert "400" in out
        assert exit.code is 1


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.logset.api._url')
def test_add_log_to_unknown_logset(mocked_url, mocked_ro_apikey, mocked_rw_apikey, capsys):
   with pytest.raises(SystemExit) as exit:
       mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
       mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
       mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

       httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGSETAPI_URL + '/123',
                              status=404,
                              content_type='application/json')

       api.add_log('123', '123')
       out, err = capsys.readouterr()

       assert "404" in out
       assert exit.code is 1


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.logset.api._url')
def test_remove_log_from_logset(mocked_url, mocked_ro_apikey, mocked_rw_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGSETAPI_URL +'/123',
                           status=200,
                           content_type='application/json',
                           body=resp_ex.basic_logset_response_with_log)

    httpretty.register_uri(httpretty.PUT, misc_ex.MOCK_LOGSETAPI_URL + '/123',
                           status=200,
                           content_Type='application/json',
                           body=resp_ex.basic_logset_response)

    api.delete_log('123', 'XXXXXXXX-ABCD-YYYY-DCBA-XXXXXXXXXXXX')
    out, err = capsys.readouterr()

    assert "XXXXXXXX-ABCD-YYYY-DCBA-XXXXXXXXXXXX" not in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_delete_logset(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.DELETE, misc_ex.MOCK_LOGSETAPI_URL + '/123',
                           status=204,
                           content_type='application/json')

    api.delete_logset('123')
    out, err = capsys.readouterr()

    assert "Deleted logset with id: 123" in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_delete_unknown_logset(mocked_url, mocked_rw_apikey, capsys):
    with pytest.raises(SystemExit) as exit:
        mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
        mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

        httpretty.register_uri(httpretty.DELETE, misc_ex.MOCK_LOGSETAPI_URL + '/123',
                               status=404,
                               content_type='application/json')

        api.delete_logset('123')
        out, err = capsys.readouterr()

        assert "404" in out
        assert exit.code is 1


@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_delete_logset_with_log_in_another_logset(mocked_url, mocked_rw_apikey, mocked_ro_apikey, capsys):
    mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_ro_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH

    httpretty.register_uri(httpretty.DELETE, misc_ex.MOCK_LOGSETAPI_URL + '/123',
                           status=204, content_type='application/json')

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_LOGSETAPI_URL + '/456',
                           status=200, content_type='application/json',
                           body=resp_ex.basic_logset_response_with_log)

    api.delete_logset('123')
    api.get_logset('456')
    out, err = capsys.readouterr()

    assert "XXXXXXXX-ABCD-YYYY-DCBA-XXXXXXXXXXXX" in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_replace_logset(mocked_url, mocked_rw_apikey, capsys):
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_url.return_value = misc_ex.MOCK_LOGSETAPI_URL

    dest_url = misc_ex.MOCK_LOGSETAPI_URL + '/123'

    httpretty.register_uri(httpretty.PUT, dest_url,
                           status=200,
                           body=resp_ex.basic_logset_response_with_log,
                           content_type='application/json')

    api.replace_logset('123', params=resp_ex.basic_logset_response_with_log)

    out, err = capsys.readouterr()
    assert "XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXX" in out