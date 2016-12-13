links = {
    'links': [
        {
            'rel': 'Self',
            'href': 'http://mydummylink.com/query/sample-continuity-suffix'
        }
    ],
    'id': 'sample-continuity-id',
}

group_response = {
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

ts_response = {
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

empty_ts_response = {
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

events_response = {
    'events': [
        {'timestamp': 1432080000011, 'message': 'Message contents1'},
        {'timestamp': 1432080000021, 'message': 'Message contents2'},
        {'timestamp': 1432080000033, 'message': 'Message contents3'}
    ]
}

team_response = {
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

usage_response = {
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

saved_query_response = {
    "id": "123456789012345678901234567890123456",
    "name": "test",
    "leql": {
        "statement": "where(/*/)",
        "during": {
            "time_range": None,
            "to": 123123,
            "from": 123
        }
    },
    "logs": ['123456789012345678901234567890123456']
}

saved_query_error_response = {
    "fields": ["time_range"],
    "messages": ["Invalid query: time_range cannot be specified with from and/or to fields"]
}
