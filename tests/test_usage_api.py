import json
import uuid

import httpretty
from mock import patch

from lecli.usage import api

MOCK_API_URL = 'http://mydummylink.com'
SAMPLE_USAGE_RESPONSE = {
    "id": "123456789012345678901234567890123456",
    "name": "Test",
    "period": {
        "to": "2016-06-01",
        "from": "2016-01-01"
    },
    "period_usage": 170129010,
    "daily_usage": [
        {
            "usage": 30618,
            "day": "2016-06-01"
        },
        {
            "usage": 6397,
            "day": "2016-05-31"
        },
        {
            "usage": 1606,
            "day": "2016-05-30"
        },
        {
            "usage": 2406,
            "day": "2016-05-29"
        }
    ]
}


@httpretty.activate
@patch('lecli.api_utils.get_account_resource_id')
@patch('lecli.api_utils.get_rw_apikey')
@patch('lecli.usage.api._url')
def test_get_usage(mocked_url, mocked_rw_apikey, mocked_account_resource_id, capsys):
    mocked_url.return_value = MOCK_API_URL
    mocked_rw_apikey.return_value = str(uuid.uuid4())
    mocked_account_resource_id.return_value = str(uuid.uuid4())
    httpretty.register_uri(httpretty.GET, MOCK_API_URL,
                           status=200,
                           content_type='application/json',
                           body=json.dumps(SAMPLE_USAGE_RESPONSE))

    api.get_usage('start', 'end')

    out, err = capsys.readouterr()
    assert "Total usage:\t" in out
    assert "Account name:\t" in out
    assert "Account ID:\t" in out
