import json
import uuid

import httpretty
import pytest

from mock import patch

from lecli.logset import api

MOCK_API_URL = 'http://mydummylink.com'
LOGSET_RESPONSE = {
  "logset": {
    "id": "XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXXXXXX",
    "name": "Test Logset",
    "description": "Example logset",
    "user_data": {},
    "logs_info": [
      {
        "id": "XXXXXXXX-ABCD-YYYY-DCBA-XXXXXXXXXXXX",
        "name": "SyslogD Log",
        "links": [
          {
            "rel": "Self",
            "href": "https://rest.logentries.com/management/logs/XXXXXXXX-ABCD-YYYY-DCBA-XXXXXXXXXXXX"
          }
        ]
      }
    ]
  }
}
BASIC_LOGSET_RESPONSE = '{"logset": {"id": "XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXX", "logs_info": [],"name": "new logset name"}}'
BASIC_LOGSET_RESPONSE_WITH_LOG = '{"logset": {"id": "XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXX", "logs_info": [{"id":"XXXXXXXX-ABCD-YYYY-DCBA-XXXXXXXXXXXX"}],"name": "new logset name"}}'


@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.logset.api._url')
def test_get_logsets(mocked_url, mocked_ro_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_ro_apikey.return_value = str(uuid.uuid4())

    httpretty.register_uri(httpretty.GET, MOCK_API_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps(LOGSET_RESPONSE))

    api.get_logsets()
    out, err = capsys.readouterr()

    assert 'XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXXXXXX' in out


@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.logset.api._url')
def test_get_logset(mocked_url, mocked_ro_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_ro_apikey.return_value = str(uuid.uuid4())
    logset_id = 'XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXXXXXX'
    httpretty.register_uri(httpretty.GET, MOCK_API_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps(LOGSET_RESPONSE))

    api.get_logset(logset_id)
    out, err = capsys.readouterr()

    assert logset_id in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_create_logset_with_name(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())

    httpretty.register_uri(httpretty.POST, MOCK_API_URL, status=201,
                           content_type='application/json',
                           body=json.dumps(LOGSET_RESPONSE))

    api.create_logset('Test Logset')
    out, err = capsys.readouterr()

    assert 'Test Logset' in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_create_logset_from_file(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())

    httpretty.register_uri(httpretty.POST, MOCK_API_URL, status=201,
                           content_type='application/json',
                           body=json.dumps(LOGSET_RESPONSE))

    params = {
        "logset": {
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
        mocked_url.return_value = '', MOCK_API_URL
        mocked_rw_apikey.return_value = str(uuid.uuid4())

        httpretty.register_uri(httpretty.POST, MOCK_API_URL, status=400,
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
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_ro_apikey.return_value = str(uuid.uuid4())

    response_body = '{"logset": {"id": "XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXX","logs_info": [],"name": "old logset name"}}'
    expected_result = '{"logset": {"id": "XXXXXXXX-XXXX-YYYY-XXXX-XXXXXXXX","logs_info": [],"name": "new logset name"}}'

    httpretty.register_uri(httpretty.GET, MOCK_API_URL, status=200,
                           content_type='application/json',
                           body=response_body)

    httpretty.register_uri(httpretty.PUT, MOCK_API_URL, status=200,
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
        mocked_url.return_value = '', MOCK_API_URL
        mocked_rw_apikey.return_value = str(uuid.uuid4())

        httpretty.register_uri(httpretty.GET, MOCK_API_URL, status=404,
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
    mocked_url.return_value = '', MOCK_API_URL
    mocked_ro_apikey.return_value = str(uuid.uuid4())
    mocked_rw_apikey.return_value = str(uuid.uuid4())

    httpretty.register_uri(httpretty.GET, MOCK_API_URL, status=200, content_type='application/json',
                           body=json.dumps(LOGSET_RESPONSE))

    httpretty.register_uri(httpretty.PUT, MOCK_API_URL, status=200, content_type='application/json',
                           body=json.dumps(LOGSET_RESPONSE))

    api.add_log('XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX', 'XXXXXXXX-ABCD-YYYY-DCBA-XXXXXXXXXXXX')
    out, err = capsys.readouterr()

    assert "XXXXXXXX-ABCD-YYYY-DCBA-XXXXXXXXXXXX" in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.logset.api._url')
def test_add_unknown_log_to_logset(mocked_url, mocked_ro_apikey, mocked_rw_apikey, capsys):
    with pytest.raises(SystemExit) as exit:
        mocked_url.return_value = '', MOCK_API_URL
        mocked_rw_apikey.return_value = str(uuid.uuid4())
        mocked_ro_apikey.return_value = str(uuid.uuid4())

        httpretty.register_uri(httpretty.GET, MOCK_API_URL, status=200,
                               content_type='application/json', body=json.dumps(LOGSET_RESPONSE))

        httpretty.register_uri(httpretty.PUT, MOCK_API_URL, status=400,
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
       mocked_url.return_value = '', MOCK_API_URL
       mocked_ro_apikey.return_value = str(uuid.uuid4())
       mocked_rw_apikey.return_value = str(uuid.uuid4())

       httpretty.register_uri(httpretty.GET, MOCK_API_URL,
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
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_ro_apikey.return_value = str(uuid.uuid4())

    httpretty.register_uri(httpretty.GET, MOCK_API_URL ,
                           status=200,
                           content_type='application/json',
                           body=json.dumps(LOGSET_RESPONSE))

    httpretty.register_uri(httpretty.PUT, MOCK_API_URL,
                           status=200,
                           content_Type='application/json',
                           body=json.dumps(LOGSET_RESPONSE))
    api.delete_log('123', str(uuid.uuid4()))
    out, err = capsys.readouterr()

    assert not err


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_delete_logset(mocked_url, mocked_rw_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())

    httpretty.register_uri(httpretty.DELETE, MOCK_API_URL,
                           status=204,
                           content_type='application/json')

    api.delete_logset('123')
    out, err = capsys.readouterr()

    assert not err
    assert "Deleted logset with id: 123" in out


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_delete_unknown_logset(mocked_url, mocked_rw_apikey, capsys):
    with pytest.raises(SystemExit) as exit:
        mocked_url.return_value = '', MOCK_API_URL
        mocked_rw_apikey.return_value = str(uuid.uuid4())

        httpretty.register_uri(httpretty.DELETE, MOCK_API_URL,
                               status=404,
                               content_type='application/json')

        api.delete_logset('123')
        out, err = capsys.readouterr()

        assert err
        assert "404" in out
        assert exit.code is 1


@httpretty.activate
@patch('lecli.api_utils.get_ro_apikey')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_delete_logset_with_log_in_another_logset(mocked_url, mocked_rw_apikey, mocked_ro_apikey, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_ro_apikey.return_value = str(uuid.uuid4())

    httpretty.register_uri(httpretty.DELETE, MOCK_API_URL,
                           status=204, content_type='application/json')

    httpretty.register_uri(httpretty.GET, MOCK_API_URL,
                           status=200, content_type='application/json',
                           body=json.dumps({}))

    api.delete_logset('123')
    api.get_logset('456')
    out, err = capsys.readouterr()

    assert not err


@httpretty.activate
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.logset.api._url')
def test_replace_logset(mocked_url, mocked_rw_apikey, capsys):
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL

    httpretty.register_uri(httpretty.PUT, MOCK_API_URL,
                           status=200,
                           body=json.dumps({}),
                           content_type='application/json')

    api.replace_logset('123', params=LOGSET_RESPONSE)

    out, err = capsys.readouterr()
    assert not err
