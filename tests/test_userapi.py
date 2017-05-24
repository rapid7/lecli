import json
import uuid

import httpretty
import requests
from mock import patch
from tabulate import tabulate

from lecli.user import api

MOCK_API_URL = 'http://mydummylink.com'
DUMMY_USER_RESPONSE = {"user": {"first_name": "",
                                "last_name": "",
                                "login_name": "",
                                "email": "",
                                "id": ""}}


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_owner_apikey_id')
@patch('lecli.api_utils.get_owner_apikey')
@patch('lecli.user.api._url')
def test_get_owner(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                   mocked_account_resource_id, capsys):
    mocked_owner_apikey.return_value = str(uuid.uuid4())
    mocked_owner_apikey_id.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL

    httpretty.register_uri(httpretty.GET, MOCK_API_URL, body='{"owners": "ownerinfo"}',
                           content_type='application/json', )

    api.get_owner()

    out, err = capsys.readouterr()
    assert tabulate("ownerinfo") in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_owner_apikey_id')
@patch('lecli.api_utils.get_owner_apikey')
@patch('lecli.user.api._url')
def test_delete_user(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                     mocked_account_resource_id, capsys):
    mocked_owner_apikey.return_value = str(uuid.uuid4())
    mocked_owner_apikey_id.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL

    user_key = str(uuid.uuid4())
    httpretty.register_uri(httpretty.DELETE, MOCK_API_URL, status=204)

    api.delete_user(user_key)

    out, err = capsys.readouterr()
    assert 'Deleted user' in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_owner_apikey_id')
@patch('lecli.api_utils.get_owner_apikey')
@patch('lecli.user.api._url')
def test_add_existing_user(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                           mocked_account_resource_id, capsys):
    mocked_owner_apikey.return_value = str(uuid.uuid4())
    mocked_owner_apikey_id.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL

    user_key = str(uuid.uuid4())
    httpretty.register_uri(httpretty.POST, MOCK_API_URL, body=json.dumps(DUMMY_USER_RESPONSE),
                           status=200, content_type='application/json')

    api.add_existing_user(user_key)

    out, err = capsys.readouterr()
    assert "Added user to account" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_owner_apikey_id')
@patch('lecli.api_utils.get_owner_apikey')
@patch('lecli.user.api._url')
def test_add_new_user(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                      mocked_account_resource_id, capsys):
    mocked_owner_apikey.return_value = str(uuid.uuid4())
    mocked_owner_apikey_id.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL

    httpretty.register_uri(httpretty.POST, MOCK_API_URL, body=json.dumps(DUMMY_USER_RESPONSE),
                           status=200, content_type='application/json')

    api.add_new_user("first_name", "last_name", "email")

    out, err = capsys.readouterr()
    assert "Added user to account" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_owner_apikey_id')
@patch('lecli.api_utils.get_owner_apikey')
@patch('lecli.user.api._url')
def test_list_users(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                    mocked_account_resource_id, capsys):
    mocked_owner_apikey.return_value = str(uuid.uuid4())
    mocked_owner_apikey_id.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL

    httpretty.register_uri(httpretty.GET, MOCK_API_URL, body='{"users":"userinfo"}',
                           content_type="application/json")

    api.list_users()

    out, err = capsys.readouterr()
    assert tabulate("userinfo") in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
def test_handle_create_user_response_status_200_with_success(mocked_account_resource_id, capsys):
    httpretty.register_uri(httpretty.GET, MOCK_API_URL, content_type="application/json",
                           status=200, body=json.dumps(DUMMY_USER_RESPONSE))
    response = requests.get(MOCK_API_URL)

    api.handle_create_user_response(response)

    out, err = capsys.readouterr()
    assert "Added user to account" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
def test_handle_create_user_response_status_200_with_already_exists_error(
        mocked_account_resource_id, capsys):
    httpretty.register_uri(httpretty.GET, MOCK_API_URL, content_type="application/json",
                           status=201, body=json.dumps(DUMMY_USER_RESPONSE))
    response = requests.get(MOCK_API_URL)

    api.handle_create_user_response(response)

    out, err = capsys.readouterr()
    assert "Added user to account" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
def test_handle_create_user_response_status_201(mocked_account_resource_id, capsys):
    httpretty.register_uri(httpretty.GET, MOCK_API_URL, content_type="application/json",
                           status=201, body=json.dumps(DUMMY_USER_RESPONSE))
    response = requests.get(MOCK_API_URL)

    api.handle_create_user_response(response)

    out, err = capsys.readouterr()
    assert "Added user to account" in out
