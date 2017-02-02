"""
Configuration and api keys util module.
"""
import sys
import ConfigParser
import base64
import hashlib
import hmac
import os
import json

import datetime
import validators
from appdirs import user_config_dir

import lecli

AUTH_SECTION = 'Auth'
URL_SECTION = 'Url'
CONFIG = ConfigParser.ConfigParser()
CONFIG_FILE_PATH = os.path.join(user_config_dir(lecli.__name__), 'config.ini')


def print_config_error_and_exit(section=None, config_key=None, value=None):
    """
    Print appropriate apiutils error message and exit.
    """
    if not section:
        print "Error: Configuration file '%s' not found" % CONFIG_FILE_PATH
    elif not config_key:
        print "Error: Section '%s' was not found in configuration file(%s)" % (
            section, CONFIG_FILE_PATH)
    elif not value:
        print "Error: Configuration key for %s was not found in configuration file(%s) in '%s' " \
              "section" % (config_key, CONFIG_FILE_PATH, section)
    else:
        print "Error: %s = '%s' is not of correct length in section: '%s' of your configuration " \
              "file: '%s'" % (config_key, value, section, CONFIG_FILE_PATH)

    sys.exit(1)


def init_config():
    """
    Initialize config file in the OS specific config path if there is no config file exists.
    """
    config_dir = user_config_dir(lecli.__name__)

    if not os.path.exists(CONFIG_FILE_PATH):
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        dummy_config = ConfigParser.ConfigParser()
        config_file = open(CONFIG_FILE_PATH, 'w')
        dummy_config.add_section(AUTH_SECTION)
        dummy_config.set(AUTH_SECTION, 'account_resource_id', '')
        dummy_config.set(AUTH_SECTION, 'owner_api_key_id', '')
        dummy_config.set(AUTH_SECTION, 'owner_api_key', '')
        dummy_config.set(AUTH_SECTION, 'rw_api_key', '')


        dummy_config.add_section('LogNicknames')
        dummy_config.add_section("LogGroups")
        dummy_config.add_section('Url')
        dummy_config.set(URL_SECTION, 'log_management_url',
                         'https://rest.logentries.com/management')


        dummy_config.write(config_file)
        config_file.close()
        print "An empty config file created in path %s, please check and configure it. To learn " \
              "how to get necessary api keys, go to this Logentries documentation page: " \
              "https://docs.logentries.com/docs/api-keys" % \
              CONFIG_FILE_PATH
    else:
        print "Config file exists in the path: " + CONFIG_FILE_PATH

    sys.exit(1)


def load_config():
    """
    Load config from OS specific config path into ConfigParser object.
    :return:
    """
    files_read = CONFIG.read(CONFIG_FILE_PATH)
    if len(files_read) != 1:
        print "Error: Config file '%s' not found, generating one..." % CONFIG_FILE_PATH
        init_config()
        sys.exit(1)
        print_config_error_and_exit()
    if not CONFIG.has_section(AUTH_SECTION):
        print_config_error_and_exit(section=AUTH_SECTION)


def get_ro_apikey():
    """
    Get read-only api key from the config file.
    """

    config_key = 'ro_api_key'
    try:
        ro_api_key = CONFIG.get(AUTH_SECTION, config_key)
        if len(ro_api_key) != 36:
            print_config_error_and_exit(AUTH_SECTION, 'Read-only API key(%s)' % config_key,
                                        ro_api_key)
        else:
            return ro_api_key
    except ConfigParser.NoOptionError:
        print_config_error_and_exit(AUTH_SECTION, 'Read-only API key(%s)' % config_key)


def get_rw_apikey():
    """
    Get read-write api key from the config file.
    """

    config_key = 'rw_api_key'
    try:
        rw_api_key = CONFIG.get(AUTH_SECTION, config_key)
        if len(rw_api_key) != 36:
            print_config_error_and_exit(AUTH_SECTION, 'Read/Write API key(%s)' % config_key,
                                        rw_api_key)
        else:
            return rw_api_key
    except ConfigParser.NoOptionError:
        print_config_error_and_exit(AUTH_SECTION, 'Read/Write API key(%s)' % config_key)


def get_owner_apikey():
    """
    Get owner api key from the config file.
    """

    config_key = 'owner_api_key'
    try:
        owner_api_key = CONFIG.get(AUTH_SECTION, config_key)
        if len(owner_api_key) != 36:
            print_config_error_and_exit(AUTH_SECTION, 'Owner API key(%s)' % config_key,
                                        owner_api_key)
            return
        else:
            return owner_api_key
    except ConfigParser.NoOptionError:
        print_config_error_and_exit(AUTH_SECTION, 'Owner API key(%s)' % config_key)


def get_owner_apikey_id():
    """
    Get owner api key id from the config file.
    """

    config_key = 'owner_api_key_id'
    try:
        owner_apikey_id = CONFIG.get(AUTH_SECTION, config_key)
        if len(owner_apikey_id) != 36:
            print_config_error_and_exit(AUTH_SECTION, 'Owner API key ID(%s)' % config_key,
                                        owner_apikey_id)
            return
        else:
            return owner_apikey_id
    except ConfigParser.NoOptionError:
        print_config_error_and_exit(AUTH_SECTION, 'Owner API key ID(%s)' % config_key)


def get_account_resource_id():
    """
    Get account resource id from the config file.
    """

    config_key = 'account_resource_id'
    try:
        account_resource_id = CONFIG.get(AUTH_SECTION, config_key)
        if len(account_resource_id) != 36:
            print_config_error_and_exit(AUTH_SECTION, 'Account Resource ID(%s)' % config_key,
                                        account_resource_id)
            return
        else:
            return account_resource_id
    except ConfigParser.NoOptionError:
        print_config_error_and_exit(AUTH_SECTION, 'Account Resource ID(%s)' % config_key)


def get_named_logkey_group(name):
    """
    Get named log-key group from the config file.

    :param name: name of the group
    """

    section = 'LogGroups'
    try:
        groups = dict(CONFIG.items(section))
        name = name.lower()
        if name in groups:
            logkeys = [line for line in str(groups[name]).splitlines() if line is not None]
            for logkey in logkeys:
                if len(logkey) != 36:
                    print_config_error_and_exit(section, 'Named Logkey Group(%s)' % name, logkey)
            return logkeys
        else:
            print_config_error_and_exit(section, 'Named Logkey Group(%s)' % name)
    except ConfigParser.NoSectionError:
        print_config_error_and_exit(section)


def get_named_logkey(name):
    """
    Get named log-key from the config file.

    :param name: name of the log key
    """

    section = 'LogNicknames'

    try:
        named_logkeys = dict(CONFIG.items(section))
        name = name.lower()
        if name in named_logkeys:
            logkey = (named_logkeys[name],)
            if len(logkey[0]) != 36:
                print_config_error_and_exit(section, 'Named Logkey(%s)' % name, logkey)
            else:
                return logkey
        else:
            print_config_error_and_exit(section, 'Named Logkey(%s)' % name)
    except ConfigParser.NoSectionError:
        print_config_error_and_exit(section)


def get_named_query(name):
    """
    Get named query from config file.

    :param name: query nick
    """

    section = 'QueryNicknames'

    try:
        named_queries = dict(CONFIG.items(section))
        name = name.lower()
        if name in named_queries:
            query = named_queries[name]
            return query
        else:
            print_config_error_and_exit(section, 'Named Query(%s)' % name)
    except ConfigParser.NoSectionError:
        print_config_error_and_exit(section)


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


def get_management_url():
    """
    Get management url from the config file
    """
    config_key = 'management_url'
    try:
        url = CONFIG.get(URL_SECTION, config_key)
        if validators.url(str(url)):
            return url
        else:
            print_config_error_and_exit(URL_SECTION, 'Log Management URL(%s)' % config_key)
    except ConfigParser.NoOptionError:
        print_config_error_and_exit(URL_SECTION, 'Log Management URL(%s)' % config_key)


def pretty_print_string_as_json(text):
    """
    Pretty prints a json string
    """
    print json.dumps(json.loads(text), indent=4, sort_keys=True)


def combine_objects(left, right):
    """
    Merge two objects
    """
    if isinstance(left, dict) and isinstance(right, dict):
        result = {}
        for key, value in left.iteritems():
            if key not in right:
                result[key] = value
            else:
                result[key] = combine_objects(value, right[key])
        for key, value in right.iteritems():
            if key not in left:
                result[key] = value
        return result
    if isinstance(left, list) and isinstance(right, list):
        return left + right
    return right
