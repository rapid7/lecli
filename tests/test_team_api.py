import json

import httpretty
from mock import patch

from lecli import team_api
from examples import misc_examples as misc_ex
from examples import response_examples as resp_ex


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team_api._url')
def test_get_teams(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    mocked_url.return_value = misc_ex.MOCK_TEAMSAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_TEAMSAPI_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({'teams': [resp_ex.team_response]}))

    team_api.get_teams()
    out, err = capsys.readouterr()

    assert "my_team" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team_api._url')
def test_get_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    team_id = misc_ex.TEST_TEAM_ID
    mocked_url.return_value = misc_ex.MOCK_TEAMSAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_TEAMSAPI_URL + '/' + team_id,
                           status=200,
                           content_type='application/json',
                           body=json.dumps({'team': resp_ex.team_response}))

    team_api.get_team(team_id)
    out, err = capsys.readouterr()

    assert "my_team" in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team_api._url')
def test_create_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    mocked_url.return_value = misc_ex.MOCK_TEAMSAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_TEAMSAPI_URL,
                           status=201,
                           content_type='application/json')

    team_api.create_team("test team")
    out, err = capsys.readouterr()

    assert "Team created with name: test team\n" == out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team_api._url')
def test_delete_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    test_team_id = misc_ex.TEST_TEAM_ID
    mocked_url.return_value = misc_ex.MOCK_TEAMSAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.DELETE, misc_ex.MOCK_TEAMSAPI_URL + "/" + test_team_id,
                           status=204)

    team_api.delete_team(test_team_id)
    out, err = capsys.readouterr()

    assert "Deleted team with id: %s\n" % misc_ex.TEST_TEAM_ID == out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team_api._url')
def test_rename_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    test_team_id = misc_ex.TEST_TEAM_ID
    mocked_url.return_value = misc_ex.MOCK_TEAMSAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.PATCH,
                           misc_ex.MOCK_TEAMSAPI_URL + "/" + test_team_id,
                           status=200,
                           content_type='application/json')

    new_name_for_team = "new_test_team_name"
    team_api.rename_team(test_team_id, new_name_for_team)
    out, err = capsys.readouterr()

    assert new_name_for_team in out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team_api._url')
def test_add_user_to_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    test_team_id = misc_ex.TEST_TEAM_ID
    mocked_url.return_value = misc_ex.MOCK_TEAMSAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_TEAMSAPI_URL + "/" + test_team_id,
                           status=200,
                           body=json.dumps({'team': resp_ex.team_response}),
                           content_type='application/json')
    httpretty.register_uri(httpretty.PATCH, misc_ex.MOCK_TEAMSAPI_URL + "/" + test_team_id,
                           status=200,
                           content_type='application/json')

    user_id_to_add = "user_id"
    team_api.add_user_to_team(test_team_id, user_id_to_add)
    out, err = capsys.readouterr()

    assert "Added user with key: '%s' to team\n" % user_id_to_add == out


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.team_api._url')
def test_delete_user_from_team(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    test_team_id = misc_ex.TEST_TEAM_ID
    mocked_url.return_value = misc_ex.MOCK_TEAMSAPI_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_TEAMSAPI_URL + "/" + test_team_id,
                           status=200,
                           body=json.dumps({'team': resp_ex.team_response}),
                           content_type='application/json')
    httpretty.register_uri(httpretty.PUT, misc_ex.MOCK_TEAMSAPI_URL + "/" + test_team_id,
                           status=200,
                           content_type='application/json')

    user_id_to_add = "user_id"
    team_api.delete_user_from_team(test_team_id, user_id_to_add)
    out, err = capsys.readouterr()

    assert "Deleted user with key: '%s' from team" % user_id_to_add in out

