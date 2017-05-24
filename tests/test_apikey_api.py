import json
import uuid

import httpretty
from mock import patch

from lecli.api_key import api

MOCK_API_URL = 'http://mydummylink.com'


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.api_key.api._url')
def test_get_api_keys(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_rw_apikey.return_value = uuid.uuid4()
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.GET, MOCK_API_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({}))

    api.get_all()

    out, err = capsys.readouterr()
    assert out
    assert not err


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.api_key.api._url')
def test_get_api_key(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    api_key_id = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL + '/' + api_key_id
    mocked_rw_apikey.return_value = uuid.uuid4()
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.GET, MOCK_API_URL + '/' + api_key_id,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({}))

    api.get(api_key_id)

    out, err = capsys.readouterr()
    assert not err


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_owner_apikey_id')
@patch('lecli.api_utils.get_owner_apikey')
@patch('lecli.api_key.api._url')
def test_delete_api_key(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                        mocked_account_resource_id, capsys):
    api_key_id = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL + '/' + api_key_id
    mocked_owner_apikey.return_value = str(uuid.uuid4())
    mocked_owner_apikey_id.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.DELETE, MOCK_API_URL + '/' + api_key_id,
                           status=204,
                           content_type='application/json')

    api.delete(api_key_id)

    out, err = capsys.readouterr()
    assert not err
    assert 'Deleted api key with id: %s' % api_key_id in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_owner_apikey_id')
@patch('lecli.api_utils.get_owner_apikey')
@patch('lecli.api_key.api._url')
def test_create_api_key(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                        mocked_account_resource_id, capsys):
    mocked_url.return_value = '', MOCK_API_URL
    mocked_owner_apikey.return_value = str(uuid.uuid4())
    mocked_owner_apikey_id.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.POST, MOCK_API_URL,
                           status=201,
                           content_type='application/json',
                           body=json.dumps({}))

    api.create({})

    out, err = capsys.readouterr()
    assert not err


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_owner_apikey_id')
@patch('lecli.api_utils.get_owner_apikey')
@patch('lecli.api_key.api._url')
def test_disable_api_key(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                         mocked_account_resource_id, capsys):
    api_key_id = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL
    mocked_owner_apikey.return_value = str(uuid.uuid4())
    mocked_owner_apikey_id.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.PATCH, MOCK_API_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({}))

    api.update(api_key_id, False)

    out, err = capsys.readouterr()
    assert {'apikey': {'active': False}} == json.loads(httpretty.last_request().body)
    assert not err
    assert 'Disabled api key with id: %s' % api_key_id in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_owner_apikey_id')
@patch('lecli.api_utils.get_owner_apikey')
@patch('lecli.api_key.api._url')
def test_enable_api_key(mocked_url, mocked_owner_apikey, mocked_owner_apikey_id,
                        mocked_account_resource_id, capsys):
    api_key_id = str(uuid.uuid4())
    mocked_url.return_value = '', MOCK_API_URL
    mocked_owner_apikey.return_value = str(uuid.uuid4())
    mocked_owner_apikey_id.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.PATCH, MOCK_API_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({}))

    api.update(api_key_id, True)

    out, err = capsys.readouterr()
    assert {'apikey': {'active': True}} == json.loads(httpretty.last_request().body)
    assert not err
    assert 'Enabled api key with id: %s' % api_key_id in out
