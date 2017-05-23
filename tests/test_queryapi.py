import json
import uuid

import httpretty
import requests
from mock import patch, Mock

from lecli.query import api

DATE_FROM = '2016-05-18 11:04:00'
DATE_TO = '2016-05-18 11:09:59'
MOCK_API_URL = 'http://mydummylink.com'
SAMPLE_EVENTS_RESPONSE = {
    'events': [
        {'timestamp': 1432080000011, 'message': 'Message contents1'},
        {'timestamp': 1432080000021, 'message': 'Message contents2'},
        {'timestamp': 1432080000033, 'message': 'Message contents3'}
    ]
}


def setup_httpretty():
    httpretty.enable()


def teardown_httpretty():
    httpretty.disable()
    httpretty.reset()


def test_prettyprint_statistics_groups(capsys):
    setup_httpretty()

    sample_group_response = {
        'statistics': {
            'from': 123123,
            'to': 1231323,
            'granularity': 0,
            'count': 1234,
            'timeseries': {},
            'groups': [{
                '200': {
                    'count': 802.0,
                    'min': 802.0,
                    'max': 802.0,
                    'sum': 802.0,
                    'bytes': 802.0,
                    'percentile': 802.0,
                    'unique': 802.0,
                    'average': 802.0
                }
            }, {
                '400': {
                    'count': 839.0,
                    'min': 839.0,
                    'max': 839.0,
                    'sum': 839.0,
                    'bytes': 839.0,
                    'percentile': 839.0,
                    'unique': 839.0,
                    'average': 839.0
                }
            }, {
                '404': {
                    'count': 839.0,
                    'min': 839.0,
                    'max': 839.0,
                    'sum': 839.0,
                    'bytes': 839.0,
                    'percentile': 839.0,
                    'unique': 839.0,
                    'average': 839.0
                }
            }, {
                'status': {
                    'count': 205.0,
                    'min': 205.0,
                    'max': 205.0,
                    'sum': 205.0,
                    'bytes': 205.0,
                    'percentile': 205.0,
                    'unique': 205.0,
                    'average': 205.0
                }
            }],
            'stats': {}
        }
    }

    httpretty.register_uri(httpretty.GET, MOCK_API_URL, content_type='application/json',
                           body=json.dumps(sample_group_response))
    response = requests.get(MOCK_API_URL)
    api.prettyprint_statistics(response)

    out, err = capsys.readouterr()
    for group in response.json()['statistics']['groups']:
        for key, value in group.iteritems():
            assert key in out

    teardown_httpretty()


def test_prettyprint_statistics_timeseries(capsys):
    setup_httpretty()

    sample_ts_response = {
        'statistics': {
            'from': 123123,
            'to': 123123,
            'count': 1234,
            'stats': {
                'global_timeseries':
                    {'count': 27733.0}
            },
            'granularity': 120000,
            'timeseries': {
                'global_timeseries': [
                    {'count': 2931.0},
                    {'count': 2869.0},
                    {'count': 2852.0},
                    {'count': 2946.0},
                    {'count': 2733.0},
                    {'count': 2564.0},
                    {'count': 2801.0},
                    {'count': 2773.0},
                    {'count': 2698.0},
                    {'count': 2566.0}
                ]
            }
        }
    }

    httpretty.register_uri(httpretty.GET, MOCK_API_URL,
                           content_type='application/json',
                           body=json.dumps(sample_ts_response))
    response = requests.get(MOCK_API_URL)
    api.prettyprint_statistics(response)

    out, err = capsys.readouterr()
    assert "Total" in out
    assert "Timeseries" in out

    teardown_httpretty()


def test_prettyprint_statistics_timeseries_with_empty_result(capsys):
    setup_httpretty()

    sample_empty_ts_response = {
        'statistics': {
            'from': 123123,
            'to': 123123,
            'count': 0.0,
            'stats': {
                'global_timeseries':
                    {}  # empty global timeseries object
            },
            'granularity': 120000,
            'timeseries': {
                'global_timeseries': [
                    {'count': 0.0},
                    {'count': 0.0},
                    {'count': 0.0},
                    {'count': 0.0},
                    {'count': 0.0},
                    {'count': 0.0},
                    {'count': 0.0},
                    {'count': 0.0},
                    {'count': 0.0},
                    {'count': 0.0}
                ]
            }
        }
    }

    httpretty.register_uri(httpretty.GET, MOCK_API_URL, content_type='application/json',
                           body=json.dumps(sample_empty_ts_response))
    response = requests.get(MOCK_API_URL)
    api.prettyprint_statistics(response)

    out, err = capsys.readouterr()
    assert "Total" in out
    assert "Timeseries" in out

    teardown_httpretty()


def test_prettyprint_events(capsys):
    setup_httpretty()

    httpretty.register_uri(httpretty.GET, MOCK_API_URL, content_type='application/json',
                           body=json.dumps(SAMPLE_EVENTS_RESPONSE))
    response = requests.get(MOCK_API_URL)
    api.prettyprint_events(response)

    out, err = capsys.readouterr()

    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.api_utils.generate_headers')
@patch('lecli.query.api._url')
def test_post_query_with_time(mocked_url, mocked_generate_headers, capsys):
    setup_httpretty()
    mocked_url.return_value = '', MOCK_API_URL

    httpretty.register_uri(httpretty.POST, MOCK_API_URL,
                           content_type='application/json',
                           body=json.dumps(SAMPLE_EVENTS_RESPONSE))
    api.post_query('', '', time_from='from', time_to='to')

    out, err = capsys.readouterr()

    assert mocked_generate_headers.called
    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.api_utils.generate_headers')
@patch('lecli.query.api._url')
def test_post_query_with_date(mocked_url, mocked_generate_headers, capsys):
    setup_httpretty()
    mocked_url.return_value = '', MOCK_API_URL
    httpretty.register_uri(httpretty.POST, MOCK_API_URL,
                           content_type='application/json',
                           body=json.dumps(SAMPLE_EVENTS_RESPONSE))
    api.post_query('', '', date_from=DATE_FROM, date_to=DATE_TO)

    out, err = capsys.readouterr()

    assert mocked_generate_headers.called
    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.api_utils.generate_headers')
@patch('lecli.query.api._url')
def test_post_query_with_relative_range(mocked_url, mocked_generate_headers, capsys):
    setup_httpretty()
    mocked_url.return_value = '', MOCK_API_URL
    httpretty.register_uri(httpretty.POST, MOCK_API_URL,
                           content_type='application/json',
                           body=json.dumps(SAMPLE_EVENTS_RESPONSE))
    api.post_query('', '',
                   time_range='last 3 min', date_to=DATE_TO)

    out, err = capsys.readouterr()

    assert mocked_generate_headers.called
    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.api_utils.generate_headers')
@patch('lecli.query.api._url')
def test_get_events(mocked_url, mocked_generate_headers, capsys):
    setup_httpretty()
    mocked_url.return_value = '', MOCK_API_URL

    httpretty.register_uri(httpretty.POST, MOCK_API_URL,
                           content_type='application/json',
                           body=json.dumps(SAMPLE_EVENTS_RESPONSE))
    api.get_events('', '', date_from=DATE_FROM, date_to=DATE_TO)

    out, err = capsys.readouterr()

    assert mocked_generate_headers.called
    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.api_utils.generate_headers')
@patch('lecli.query.api._url')
def test_get_recent_events(mocked_url, mocked_generate_headers, capsys):
    setup_httpretty()
    mocked_url.return_value = '', MOCK_API_URL

    httpretty.register_uri(httpretty.POST, MOCK_API_URL,
                           content_type='application/json',
                           body=json.dumps(SAMPLE_EVENTS_RESPONSE))
    api.get_recent_events('')

    out, err = capsys.readouterr()

    assert mocked_generate_headers.called
    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.api_utils.generate_headers')
def test_fetch_results(mocked_generate_headers):
    setup_httpretty()
    dest_url = MOCK_API_URL + "_some_arbitrary_url_suffix"
    httpretty.register_uri(httpretty.GET, dest_url, content_type='application/json',
                           body=json.dumps(SAMPLE_EVENTS_RESPONSE))

    response = api.fetch_results(dest_url).json()

    assert mocked_generate_headers.called
    assert "Message contents1" in response['events'][0]['message']
    assert "Message contents2" in response['events'][1]['message']
    assert "Message contents3" in response['events'][2]['message']

    teardown_httpretty()


@patch('lecli.api_utils.generate_headers')
@patch('lecli.query.api.handle_response')
def test_continue_request(mocked_headers, mocked_response_handle):
    setup_httpretty()

    links_response = {
        'links': [
            {
                'rel': 'Self',
                'href': 'http://mydummylink.com/query/sample-continuity-suffix'
            }
        ],
        'id': 'sample-continuity-id',
    }

    httpretty.register_uri(httpretty.GET, MOCK_API_URL, content_type='application/json',
                           body=json.dumps(links_response))

    dest_url = links_response['links'][0]['href']
    httpretty.register_uri(httpretty.GET, dest_url, content_type='application/json')

    resp = requests.get(MOCK_API_URL)
    api.continue_request(resp, Mock())

    assert mocked_response_handle.called
    assert mocked_headers.called

    teardown_httpretty()


@patch('lecli.api_utils.generate_headers')
@patch('lecli.query.api.handle_tail')
@patch('lecli.query.api._url')
def test_live_tail_api(mocked_url, mocked_handle_tail, mocked_generate_headers):
    setup_httpretty()

    mocked_url.return_value = '', MOCK_API_URL
    httpretty.register_uri(httpretty.POST, MOCK_API_URL, content_type='application/json',
                           body=json.dumps({}))

    api.tail_logs(logkeys=str(uuid.uuid4()), label=None, leql=None, poll_interval=0.5)

    assert mocked_generate_headers.called
    assert mocked_handle_tail.called

    teardown_httpretty()


def test_handle_response(capsys):
    setup_httpretty()

    httpretty.register_uri(httpretty.GET, MOCK_API_URL, content_type='application/json',
                           body=json.dumps(SAMPLE_EVENTS_RESPONSE))
    resp = requests.get(MOCK_API_URL)

    api.handle_response(resp, Mock())

    out, err = capsys.readouterr()

    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()

