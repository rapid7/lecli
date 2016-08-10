import json

import httpretty
import requests
from mock import patch
from tabulate import tabulate

from lecli import user_api
from examples import misc_examples as misc_ex


@httpretty.activate
@patch('lecli.apiutils.get_account_resource_id')
@patch('lecli.apiutils.get_owner_apikey_id')
@patch('lecli.apiutils.get_owner_apikey')
@patch('lecli.user_api._url')
def test_get_owner(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                   mocked_account_resource_id, capsys):
    mocked_owner_apikey.return_value = misc_ex.TEST_OWNER_APIKEY
    mocked_owner_apikey_id.return_value = misc_ex.TEST_OWNER_APIKEY_ID
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    mocked_url.return_value = misc_ex.MOCK_USERAPI_URL

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_USERAPI_URL,
                           body='{"owners": "ownerinfo"}',
                           content_type='application/json', )

    user_api.get_owner()

    out, err = capsys.readouterr()
    assert tabulate("ownerinfo") in out


@httpretty.activate
@patch('lecli.apiutils.get_account_resource_id')
@patch('lecli.apiutils.get_owner_apikey_id')
@patch('lecli.apiutils.get_owner_apikey')
@patch('lecli.user_api._url')
def test_delete_user(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                     mocked_account_resource_id, capsys):
    mocked_owner_apikey.return_value = misc_ex.TEST_OWNER_APIKEY
    mocked_owner_apikey_id.return_value = misc_ex.TEST_OWNER_APIKEY_ID
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    mocked_url.return_value = misc_ex.MOCK_USERAPI_URL

    dest_url = misc_ex.MOCK_USERAPI_URL + '/' + str(misc_ex.TEST_USER_KEY)
    httpretty.register_uri(httpretty.DELETE, dest_url, status=204)

    user_api.delete_user(misc_ex.TEST_USER_KEY)

    out, err = capsys.readouterr()
    assert 'Deleted user' in out


@httpretty.activate
@patch('lecli.apiutils.get_account_resource_id')
@patch('lecli.apiutils.get_owner_apikey_id')
@patch('lecli.apiutils.get_owner_apikey')
@patch('lecli.user_api._url')
def test_add_existing_user(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                           mocked_account_resource_id, capsys):
    mocked_owner_apikey.return_value = misc_ex.TEST_OWNER_APIKEY
    mocked_owner_apikey_id.return_value = misc_ex.TEST_OWNER_APIKEY_ID
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    mocked_url.return_value = misc_ex.MOCK_USERAPI_URL

    dest_url = misc_ex.MOCK_USERAPI_URL + '/' + str(misc_ex.TEST_USER_KEY)
    httpretty.register_uri(httpretty.POST, dest_url,
                           body=json.dumps(misc_ex.DUMMY_USER_CONTENT),
                           status=200,
                           content_type='application/json')

    user_api.add_existing_user(misc_ex.TEST_USER_KEY)

    out, err = capsys.readouterr()
    assert "Added user to account" in out


@httpretty.activate
@patch('lecli.apiutils.get_account_resource_id')
@patch('lecli.apiutils.get_owner_apikey_id')
@patch('lecli.apiutils.get_owner_apikey')
@patch('lecli.user_api._url')
def test_add_new_user(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                      mocked_account_resource_id, capsys):
    mocked_owner_apikey.return_value = misc_ex.TEST_OWNER_APIKEY
    mocked_owner_apikey_id.return_value = misc_ex.TEST_OWNER_APIKEY_ID
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    mocked_url.return_value = misc_ex.MOCK_USERAPI_URL

    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_USERAPI_URL,
                           body=json.dumps(misc_ex.DUMMY_USER_CONTENT),
                           status=200,
                           content_type='application/json')

    user_api.add_new_user("first_name", "last_name", "email")

    out, err = capsys.readouterr()
    assert "Added user to account" in out


@httpretty.activate
@patch('lecli.apiutils.get_account_resource_id')
@patch('lecli.apiutils.get_owner_apikey_id')
@patch('lecli.apiutils.get_owner_apikey')
@patch('lecli.user_api._url')
def test_list_users(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                    mocked_account_resource_id, capsys):
    mocked_owner_apikey.return_value = misc_ex.TEST_OWNER_APIKEY
    mocked_owner_apikey_id.return_value = misc_ex.TEST_OWNER_APIKEY_ID
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    mocked_url.return_value = misc_ex.MOCK_USERAPI_URL

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_USERAPI_URL,
                           body='{"users":"userinfo"}',
                           content_type="application/json")

    user_api.list_users()

    out, err = capsys.readouterr()
    assert tabulate("userinfo") in out


@httpretty.activate
@patch('lecli.apiutils.get_account_resource_id')
def test_handle_create_user_response_status_200_with_success(mocked_account_resource_id, capsys):
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_USERAPI_URL,
                           content_type="application/json",
                           status=200,
                           body=json.dumps(misc_ex.DUMMY_USER_CONTENT))
    response = requests.get(misc_ex.MOCK_USERAPI_URL)

    user_api.handle_create_user_response(response)

    out, err = capsys.readouterr()
    assert "Added user to account" in out


@httpretty.activate
@patch('lecli.apiutils.get_account_resource_id')
def test_handle_create_user_response_status_200_with_already_exists_error(mocked_account_resource_id, capsys):
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_USERAPI_URL,
                           content_type="application/json",
                           status=201,
                           body=json.dumps(misc_ex.DUMMY_USER_CONTENT))
    response = requests.get(misc_ex.MOCK_USERAPI_URL)

    user_api.handle_create_user_response(response)

    out, err = capsys.readouterr()
    assert "Added user to account" in out


@httpretty.activate
@patch('lecli.apiutils.get_account_resource_id')
def test_handle_create_user_response_status_201(mocked_account_resource_id, capsys):
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_USERAPI_URL,
                           content_type="application/json",
                           status=201,
                           body=json.dumps(misc_ex.DUMMY_USER_CONTENT))
    response = requests.get(misc_ex.MOCK_USERAPI_URL)

    user_api.handle_create_user_response(response)

    out, err = capsys.readouterr()
    assert "Added user to account" in out
