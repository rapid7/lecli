import json

import httpretty
import requests
from mock import patch, Mock

from lecli import query_api
from examples import response_examples as resp_ex
from examples import misc_examples as misc_ex


def setup_httpretty():
    httpretty.enable()


def teardown_httpretty():
    httpretty.disable()
    httpretty.reset()


def test_prettyprint_statistics_groups(capsys):
    setup_httpretty()

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           body=json.dumps(resp_ex.group_response))
    response = requests.get(misc_ex.MOCK_QUERYAPI_URL)
    query_api.prettyprint_statistics(response)

    out, err = capsys.readouterr()
    for group in response.json()['statistics']['groups']:
        for key, value in group.iteritems():
            assert key in out

    teardown_httpretty()


def test_prettyprint_statistics_timeseries(capsys):
    setup_httpretty()

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           body=json.dumps(resp_ex.ts_response))
    response = requests.get(misc_ex.MOCK_QUERYAPI_URL)
    query_api.prettyprint_statistics(response)

    out, err = capsys.readouterr()
    assert "Total" in out
    assert "Timeseries" in out

    teardown_httpretty()


def test_prettyprint_events(capsys):
    setup_httpretty()

    httpretty.register_uri(httpretty.GET, misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           body=json.dumps(resp_ex.events_response))
    response = requests.get(misc_ex.MOCK_QUERYAPI_URL)
    query_api.prettyprint_events(response)

    out, err = capsys.readouterr()

    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.apiutils.generate_headers')
@patch('lecli.query_api._url')
def test_post_query_with_time(mocked_url, mocked_generate_headers, capsys):
    setup_httpretty()
    mocked_url.return_value = misc_ex.MOCK_QUERYAPI_URL

    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           body=json.dumps(resp_ex.events_response))
    query_api.post_query(misc_ex.TEST_LOG_GROUP, misc_ex.TEST_QUERY, time_from=misc_ex.TIME_FROM,
                         time_to=misc_ex.TIME_TO)

    out, err = capsys.readouterr()

    assert mocked_generate_headers.called
    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.apiutils.generate_headers')
@patch('lecli.query_api._url')
def test_post_query_with_date(mocked_url, mocked_generate_headers, capsys):
    setup_httpretty()
    mocked_url.return_value = misc_ex.MOCK_QUERYAPI_URL
    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           body=json.dumps(resp_ex.events_response))
    query_api.post_query(misc_ex.TEST_LOG_GROUP, misc_ex.TEST_QUERY, date_from=misc_ex.DATE_FROM,
                         date_to=misc_ex.DATE_TO)

    out, err = capsys.readouterr()

    assert mocked_generate_headers.called
    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.apiutils.generate_headers')
@patch('lecli.query_api._url')
def test_post_query_with_relative_range(mocked_url, mocked_generate_headers, capsys):
    setup_httpretty()
    mocked_url.return_value = misc_ex.MOCK_QUERYAPI_URL
    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           body=json.dumps(resp_ex.events_response))
    query_api.post_query(misc_ex.TEST_LOG_GROUP, misc_ex.TEST_QUERY,
                         time_range=misc_ex.RELATIVE_TIME, date_to=misc_ex.DATE_TO)

    out, err = capsys.readouterr()

    assert mocked_generate_headers.called
    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.apiutils.generate_headers')
@patch('lecli.query_api._url')
def test_get_events(mocked_url, mocked_generate_headers, capsys):
    setup_httpretty()
    mocked_url.return_value = misc_ex.MOCK_QUERYAPI_URL

    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           body=json.dumps(resp_ex.events_response))
    query_api.get_events(misc_ex.TEST_LOG_GROUP, misc_ex.TEST_QUERY, date_from=misc_ex.DATE_FROM,
                         date_to=misc_ex.DATE_TO)

    out, err = capsys.readouterr()

    assert mocked_generate_headers.called
    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.apiutils.generate_headers')
@patch('lecli.query_api._url')
def test_get_recent_events(mocked_url, mocked_generate_headers, capsys):
    setup_httpretty()
    mocked_url.return_value = misc_ex.MOCK_QUERYAPI_URL

    httpretty.register_uri(httpretty.POST, misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           body=json.dumps(resp_ex.events_response))
    query_api.get_recent_events(misc_ex.TEST_LOG_GROUP)

    out, err = capsys.readouterr()

    assert mocked_generate_headers.called
    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


@patch('lecli.apiutils.generate_headers')
def test_fetch_results(mocked_generate_headers):
    setup_httpretty()
    dest_url = misc_ex.MOCK_QUERYAPI_URL + "_some_arbitrary_url_suffix"
    httpretty.register_uri(httpretty.GET, dest_url,
                           content_type='application/json',
                           body=json.dumps(resp_ex.events_response))

    response = query_api.fetch_results(dest_url).json()

    assert mocked_generate_headers.called
    assert "Message contents1" in response['events'][0]['message']
    assert "Message contents2" in response['events'][1]['message']
    assert "Message contents3" in response['events'][2]['message']

    teardown_httpretty()


@patch('lecli.apiutils.generate_headers')
@patch('lecli.query_api.handle_response')
def test_continue_request(mocked_headers, mocked_response_handle):
    setup_httpretty()

    httpretty.register_uri(httpretty.GET,
                           misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           body=json.dumps(resp_ex.links))

    dest_url = resp_ex.links['links'][0]['href']
    httpretty.register_uri(httpretty.GET,
                           dest_url,
                           content_type='application/json')

    resp = requests.get(misc_ex.MOCK_QUERYAPI_URL)
    query_api.continue_request(resp, Mock())

    assert mocked_response_handle.called
    assert mocked_headers.called

    teardown_httpretty()


def test_handle_response(capsys):
    setup_httpretty()

    httpretty.register_uri(httpretty.GET,
                           misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           body=json.dumps(resp_ex.events_response))
    resp = requests.get(misc_ex.MOCK_QUERYAPI_URL)

    query_api.handle_response(resp, Mock())

    out, err = capsys.readouterr()

    assert "Message contents1" in out
    assert "Message contents2" in out
    assert "Message contents3" in out

    teardown_httpretty()


def test_response_error_status(capsys):
    setup_httpretty()

    httpretty.register_uri(httpretty.GET,
                           misc_ex.MOCK_QUERYAPI_URL,
                           content_type='application/json',
                           status=405)
    resp = requests.get(misc_ex.MOCK_QUERYAPI_URL)
    query_api.response_error(resp)

    out, err = capsys.readouterr()
    assert "Request Error: " in out

    teardown_httpretty()


def test_response_error_content_type(capsys):
    setup_httpretty()

    httpretty.register_uri(httpretty.GET,
                           misc_ex.MOCK_QUERYAPI_URL,
                           content_type='text/html',
                           status=200)
    resp = requests.get(misc_ex.MOCK_QUERYAPI_URL)
    query_api.response_error(resp)

    out, err = capsys.readouterr()
    assert "Unexpected Content Type Received in Response: " in out

    teardown_httpretty()
