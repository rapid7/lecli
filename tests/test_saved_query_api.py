import json
import uuid

import httpretty
from mock import patch
from examples import misc_examples as misc_ex
from examples import response_examples as resp_ex
from lecli import saved_query_api


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.saved_query_api._url')
def test_get_saved_queries(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    mocked_url.return_value = misc_ex.MOCK_SAVED_QUERY_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_SAVED_QUERY_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({'saved_queries': [resp_ex.saved_query_response]}))

    saved_query_api.get_saved_query()
    out, err = capsys.readouterr()

    assert "Name:" in out
    assert "Logs:" in out
    assert "ID:" in out
    assert "Statement:" in out
    assert "Time range:" in out
    assert "From:" in out
    assert "To:" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.saved_query_api._url')
def test_get_saved_query(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    saved_query_id = str(uuid.uuid4())
    mocked_url.return_value = misc_ex.MOCK_SAVED_QUERY_URL + "/" + saved_query_id
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_SAVED_QUERY_URL + "/" + saved_query_id,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({'saved_query': resp_ex.saved_query_response}))

    saved_query_api.get_saved_query()
    out, err = capsys.readouterr()

    assert "Name:" in out
    assert "Logs:" in out
    assert "ID:" in out
    assert "Statement:" in out
    assert "Time range:" in out
    assert "From:" in out
    assert "To:" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.saved_query_api._url')
def test_create_saved_query(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    saved_query_name = "my_saved_query"
    mocked_url.return_value = misc_ex.MOCK_SAVED_QUERY_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_SAVED_QUERY_URL,
                           status=201,
                           content_type='application/json',
                           body=json.dumps({"saved_query": resp_ex.saved_query_response}))

    saved_query_api.create_saved_query(saved_query_name, "where(/*/)")
    out, err = capsys.readouterr()

    assert "Saved query created with name: %s" % saved_query_name in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.saved_query_api._url')
def test_delete_saved_query(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    test_saved_query_id = str(uuid.uuid4())
    mocked_url.return_value = misc_ex.MOCK_SAVED_QUERY_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.DELETE, misc_ex.MOCK_SAVED_QUERY_URL + "/" +
                           test_saved_query_id, status=204)

    saved_query_api.delete_saved_query(test_saved_query_id)
    out, err = capsys.readouterr()

    assert "Deleted saved query with id: %s" % test_saved_query_id in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.saved_query_api._url')
def test_patch_saved_query(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    test_saved_query_id = str(uuid.uuid4())
    mocked_url.return_value = misc_ex.MOCK_SAVED_QUERY_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(
        httpretty.PATCH, misc_ex.MOCK_SAVED_QUERY_URL + "/" + test_saved_query_id, status=200,
        content_type='application/json', body=json.dumps({"saved_query":
                                                                  resp_ex.saved_query_response}))

    saved_query_api.update_saved_query(test_saved_query_id, name="new_query_name",
                                       statement="new_statement", from_ts=123, to_ts=123456)
    out, err = capsys.readouterr()

    assert "Saved query with id %s updated" % test_saved_query_id in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.saved_query_api._url')
def test_patch_saved_query_none_fields(mocked_url, mocked_rw_apikey, mocked_account_resource_id,
                                       capsys):
    test_saved_query_id = str(uuid.uuid4())
    mocked_url.return_value = misc_ex.MOCK_SAVED_QUERY_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(
        httpretty.PATCH, misc_ex.MOCK_SAVED_QUERY_URL + "/" + test_saved_query_id, status=200,
        content_type='application/json', body=json.dumps({"saved_query":
                                                              resp_ex.saved_query_response}))

    saved_query_api.update_saved_query(test_saved_query_id, name=None,
                                       statement="new_statement")
    out, err = capsys.readouterr()

    assert "Saved query with id %s updated" % test_saved_query_id in out
    body = json.loads(httpretty.last_request().body)['saved_query']
    assert "name" not in body
    assert "statement" in body['leql']


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.saved_query_api._url')
def test_failing_patch_saved_query(mocked_url, mocked_rw_apikey, mocked_account_resource_id,
                                   capsys):
    test_saved_query_id = str(uuid.uuid4())
    mocked_url.return_value = misc_ex.MOCK_SAVED_QUERY_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(
        httpretty.PATCH, misc_ex.MOCK_SAVED_QUERY_URL + "/" + test_saved_query_id, status=400,
        content_type='application/json', body=json.dumps(resp_ex.saved_query_error_response))

    saved_query_api.update_saved_query(
        test_saved_query_id, name="new_query_name", statement="new_statement", from_ts=123,
        to_ts=123456, time_range="last 10 days")
    out, err = capsys.readouterr()

    assert "Invalid field: time_range\n" in out
    assert "Message: Invalid query: time_range cannot be specified with from and/or to fields" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.saved_query_api._url')
def test_failing_create_saved_query(mocked_url, mocked_rw_apikey, mocked_account_resource_id,
                                   capsys):
    mocked_url.return_value = misc_ex.MOCK_SAVED_QUERY_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(
        httpretty.POST, misc_ex.MOCK_SAVED_QUERY_URL, status=400,
        content_type='application/json', body=json.dumps(resp_ex.saved_query_error_response))

    saved_query_api.create_saved_query(name="new_query_name", statement="new_statement",
                                       from_ts=123, to_ts=123456, time_range="last 10 days")
    out, err = capsys.readouterr()

    assert "Invalid field: time_range\n" in out
    assert "Message: Invalid query: time_range cannot be specified with from and/or to fields" in out

