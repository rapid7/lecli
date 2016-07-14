import ConfigParser
import base64
import hashlib
import hmac
import os

import datetime
from appdirs import user_config_dir

import lecli

CONFIG = ConfigParser.ConfigParser()


def load_config():
    config_file = os.path.join(user_config_dir(lecli.__name__), 'config.ini')
    files_read = CONFIG.read(config_file)
    if len(files_read) != 1:
        print "Error: Config file '%s' not found" % config_file
        exit(1)
    if not CONFIG.has_section('Auth'):
        print "Error: Config file '%s' is missing Auth section" % config_file
        exit(1)


def get_ro_apikey():
    """
    Get read-only api key from the config file.
    """

    ro_apikey = None
    try:
        ro_apikey = CONFIG.get('Auth', 'ro_api_key')
        if len(ro_apikey) != 36:
            print 'Error: Read-only API Key not of correct length'
    except ConfigParser.NoOptionError:
        print 'Error: Read-only API Key not configured in configuration file'
        exit(1)
    return ro_apikey


def get_rw_apikey():
    """
    Get read-write api key from the config file.
    """

    rw_apikey = None
    try:
        rw_apikey = CONFIG.get('Auth', 'rw_api_key')
        if len(rw_apikey) != 36:
            print 'Error: Read/Write API Key not of correct length'
    except ConfigParser.NoOptionError:
        print 'Error: Read/Write API Key not configured in configuration file'
        exit(1)
    return rw_apikey


def get_owner_apikey():
    """
    Get owner api key from the config file.
    """

    owner_apikey = None
    try:
        owner_apikey = CONFIG.get('Auth', 'owner_api_key')
        if len(owner_apikey) != 36:
            print 'Error: Owner API Key not of correct length'
    except ConfigParser.NoOptionError:
        print 'Error: Owner API Key not configured in configuration file'
        exit(1)
    return owner_apikey


def get_owner_apikey_id():
    """
    Get owner api key id from the config file.
    """

    owner_apikey_id = None
    try:
        owner_apikey_id = CONFIG.get('Auth', 'owner_api_key_id')
        if len(owner_apikey_id) != 36:
            print 'Error: Owner API Key ID not of correct length'
    except ConfigParser.NoOptionError:
        print 'Error: Owner API Key ID not configured in configuration file'
        exit(1)
    return owner_apikey_id


def get_account_resource_id():
    """
    Get account resource id from the config file.
    """

    account_resource_id = None
    try:
        account_resource_id = CONFIG.get('Auth', 'account_resource_id')
        if len(account_resource_id) != 36:
            print 'Error: Account Resource ID not of correct length'
    except ConfigParser.NoOptionError:
        print 'Error: Account Resource ID not configured in configuration file'
        exit(1)
    return account_resource_id


def get_named_logkey_group(name):
    """
    Get named log-key group from the config file.

    :param name: name of the group
    """

    groups = dict(CONFIG.items('LogGroups'))
    if name in groups:
        logkeys = filter(None, str(groups[name]).splitlines())
        for logkey in logkeys:
            if len(logkey) != 36:
                print 'Error: Logkey is not of correct length.'
                return
        return logkeys
    else:
        print "Error: No group with name '%s'" % name
        return None


def get_named_logkey(name):
    """
    Get named log-key from the config file.

    :param name: name of the log key
    """

    nicknames = dict(CONFIG.items('LogNicknames'))

    if name in nicknames:
        logkey = (nicknames[name],)
        if len(logkey[0]) != 36:
            print 'Error: Logkey is not of correct length. '
        else:
            return logkey
    else:
        print "Error: No nickname with name '%s'" % name
        return None


def get_query_from_nickname(qnick):
    """
    Get named query from config file.

    :param qnick: query nick
    """

    qnicknames = dict(CONFIG.items('QueryNicknames'))

    if qnick in qnicknames:
        query = qnicknames[qnick]
        return query
    else:
        print "Error: No query nickname with name '%s'" % qnick
        return None


def generate_headers(api_key_type, method=None, action=None, body=None):
    """
    Generate request headers according to api_key_type that is being used.
    """
    headers = None

    if api_key_type is 'ro':
        headers = {
            'x-api-key': get_ro_apikey(),
            "Content-Type": "application/json"
        }
    elif api_key_type is 'rw':
        headers = {
            'x-api-key': get_rw_apikey(),
            "Content-Type": "application/json"
        }
    elif api_key_type is 'owner':  # Uses the owner-api-key
        date_h = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        content_type_h = "application/json"
        signature = gensignature(get_owner_apikey(), date_h, content_type_h, method, action, body)
        headers = {
            "Date": date_h,
            "Content-Type": content_type_h,
            "authorization-api-key": "%s:%s" % (
                get_owner_apikey_id().encode('utf8'), base64.b64encode(signature))
        }

    headers['User-Agent'] = 'lecli'

    return headers


def gensignature(api_key, date, content_type, request_method, query_path, request_body):
    """
    Generate owner access signature.

    """
    hashed_body = base64.b64encode(hashlib.sha256(request_body).digest())
    canonical_string = request_method + content_type + date + query_path + hashed_body

    # Create a new hmac digester with the api key as the signing key and sha1 as the algorithm
    digest = hmac.new(api_key, digestmod=hashlib.sha1)
    digest.update(canonical_string)

    return digest.digest()
