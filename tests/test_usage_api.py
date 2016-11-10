import json

import httpretty
from mock import patch

from lecli import usage_api
from examples import misc_examples as misc_ex
from examples import response_examples as resp_ex


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.usage_api._url')
def test_get_usage(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    mocked_url.return_value = misc_ex.MOCK_USAGE_URL
    mocked_rw_apikey.return_value = misc_ex.TEST_APIKEY_WITH_VALID_LENGTH
    mocked_account_resource_id.return_value = misc_ex.TEST_ACCOUNT_RESOURCE_ID
    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_USAGE_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps(resp_ex.usage_response))
    expected_total = 170129010
    expected_name = 'Testing Account Part II'
    expected_id = '362e8659-e866-42dd-b2bf-f1b80166dd71'

    usage_api.get_usage(misc_ex.USAGE_DATE_FROM, misc_ex.USAGE_DATE_TO)

    out, err = capsys.readouterr()
    assert "Total usage:\t%s" % expected_total in out
    assert "Account name:\t%s" % expected_name in out
    assert "Account ID:\t%s" % expected_id in out
