"""
Account usage API module.
"""
import sys
import requests
from tabulate import tabulate

from lecli import api_utils
from lecli import response_utils


def _url():
    """
    Get rest query url of account resource id.
    """
    return 'https://rest.logentries.com/usage/accounts/%s' % \
           api_utils.get_account_resource_id()


def _handle_get_usage_response(response):
    """
    Handle get usage response
    """
    response_json = response.json()
    daily_usage = response_json['daily_usage']
    total_usage = response_json['period_usage']
    acc_name = response_json['name']
    acc_id = response_json['id']

    print tabulate(sorted(daily_usage, key=lambda x: x['day']), headers='keys',
                   tablefmt='pipe')
    print "Total usage:\t%s" % total_usage
    print "Account name:\t%s" % acc_name
    print "Account ID:\t%s" % acc_id


def get_usage(start, end):
    """
    Get usage information for the account between start and end dates.
    """
    headers = api_utils.generate_headers('rw')
    params = {'from': start,
              'to': end}
    try:
        response = requests.get(_url(), params=params, headers=headers)
        if response_utils.response_error(response):
            sys.stderr.write("Getting account usage failed. Status code %s"
                             % response.status_code)
            sys.exit(1)
        else:
            _handle_get_usage_response(response)
    except requests.exceptions.RequestException as error:
        sys.stderr.write(error)
        sys.exit(1)
