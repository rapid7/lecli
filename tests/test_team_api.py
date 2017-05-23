import json
import uuid

import httpretty
from mock import patch

from lecli.team import api

MOCK_API_URL = 'http://mydummylink.com'
TEAM_RESPONSE = {
    'id': '123456789012345678901234567890123456',
    'name': 'my_team',
    'users': [
        {
            'id': '123456789012345678901234567890123456',
            'links': {
                'href': 'https://dummy.link',
                'ref': 'Self'
            }
        }
    ]
}


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team.api._url')
def test_get_teams(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    mocked_url.return_value = MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.GET, MOCK_API_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({'teams': [TEAM_RESPONSE]}))

    api.get_teams()
    out, err = capsys.readouterr()

    assert "my_team" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team.api._url')
def test_get_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    team_id = str(uuid.uuid4())
    mocked_url.return_value = MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.GET, MOCK_API_URL + '/' + team_id,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({'team': TEAM_RESPONSE}))

    api.get_team(team_id)
    out, err = capsys.readouterr()

    assert "my_team" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team.api._url')
def test_create_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    mocked_url.return_value = MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.POST, MOCK_API_URL,
                           status=201,
                           content_type='application/json')

    api.create_team("test team")
    out, err = capsys.readouterr()

    assert "Team created with name: test team\n" == out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team.api._url')
def test_delete_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    test_team_id = str(uuid.uuid4())
    mocked_url.return_value = MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.DELETE, MOCK_API_URL + "/" + test_team_id,
                           status=204)

    api.delete_team(test_team_id)
    out, err = capsys.readouterr()

    assert "Deleted team with id: %s\n" % test_team_id == out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team.api._url')
def test_rename_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    test_team_id = str(uuid.uuid4())
    mocked_url.return_value = MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.PATCH, MOCK_API_URL + "/" + test_team_id, status=200,
                           content_type='application/json')

    new_name_for_team = "new_test_team_name"
    api.rename_team(test_team_id, new_name_for_team)
    out, err = capsys.readouterr()

    assert new_name_for_team in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team.api._url')
def test_add_user_to_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    test_team_id = str(uuid.uuid4())
    mocked_url.return_value = MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.GET, MOCK_API_URL + "/" + test_team_id, status=200,
                           body=json.dumps({'team': TEAM_RESPONSE}),
                           content_type='application/json')
    httpretty.register_uri(httpretty.PATCH, MOCK_API_URL + "/" + test_team_id, status=200,
                           content_type='application/json')

    user_id_to_add = "user_id"
    api.add_user_to_team(test_team_id, user_id_to_add)
    out, err = capsys.readouterr()

    assert "Added user with key: '%s' to team\n" % user_id_to_add == out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team.api._url')
def test_delete_user_from_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    test_team_id = str(uuid.uuid4())
    mocked_url.return_value = MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.GET, MOCK_API_URL + "/" + test_team_id, status=200,
                           body=json.dumps({'team': TEAM_RESPONSE}),
                           content_type='application/json')
    httpretty.register_uri(httpretty.PUT, MOCK_API_URL + "/" + test_team_id, status=200,
                           content_type='application/json')

    user_id_to_add = "user_id"
    api.delete_user_from_team(test_team_id, user_id_to_add)
    out, err = capsys.readouterr()

    assert "Deleted user with key: '%s' from team" % user_id_to_add in out

