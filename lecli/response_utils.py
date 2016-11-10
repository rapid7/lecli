"""
Response utils
"""
import requests


def response_error(response):
    """
    Check response if it has any errors.
    """
    if response.headers.get('X-RateLimit-Remaining') is not None:
        if int(response.headers['X-RateLimit-Remaining']) == 0:
            print 'Error: Rate Limit Reached, will reset in ' + response.headers.get(
                'X-RateLimit-Reset') + ' seconds'
            return True
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print "Request Error:", error.message
        if response.status_code == 500:
            print 'Your account may have no owner assigned. ' \
                  'Please visit www.logentries.com for information on assigning an account owner.'
        return True

    if response.status_code == 200:
        if response.headers['Content-Type'] != 'application/json':
            print 'Unexpected Content Type Received in Response: ' + response.headers[
                'Content-Type']
            return True
        else:
            return False
    return False
