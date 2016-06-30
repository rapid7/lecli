import ConfigParser
import base64
import datetime
import hashlib
import hmac


configfile = 'config.ini'
config = ConfigParser.ConfigParser()

def load_config():
  files_read = config.read(configfile)
  if len(files_read) != 1:
    print "Error: Config file '%s' not found" % configfile
    exit(1)
  if not config.has_section('Auth'):
    print "Error: Config file '%s' is missing Auth section" % configfile
    exit(1)

def get_ro_apikey():
    ro_apikey = None
    try:
        ro_apikey = config.get('Auth', 'ro_api_key')
        if len(ro_apikey) != 36:
            print 'Error: Read-only API Key not of correct length'
    except ConfigParser.NoOptionError:
        print 'Error: Read-only API Key not configured in configuration file'
        exit(1)
    return ro_apikey


def get_rw_apikey():
    rw_apikey = None
    try:
        rw_apikey = config.get('Auth', 'rw_api_key')
        if len(rw_apikey) != 36:
            print 'Error: Read/Write API Key not of correct length'
    except ConfigParser.NoOptionError:
        print 'Error: Read/Write API Key not configured in configuration file'
        exit(1)
    return rw_apikey


def get_owner_apikey():
    owner_apikey = None
    try:
        owner_apikey = config.get('Auth', 'owner_api_key')
        if len(owner_apikey) != 36:
            print 'Error: Owner API Key not of correct length'
    except ConfigParser.NoOptionError:
        print 'Error: Owner API Key not configured in configuration file'
        exit(1)
    return owner_apikey


def get_owner_apikey_id():
    owner_apikey_id = None
    try:
        owner_apikey_id = config.get('Auth', 'owner_api_key_id')
        if len(owner_apikey_id) != 36:
            print 'Error: Owner API Key ID not of correct length'
    except ConfigParser.NoOptionError:
        print 'Error: Owner API Key ID not configured in configuration file'
        exit(1)
    return owner_apikey_id


def get_account_resource_id():
    account_resource_id = None
    try:
        account_resource_id = config.get('Auth', 'account_resource_id')
        if len(account_resource_id) != 36:
            print 'Error: Account Resource ID not of correct length'
    except ConfigParser.NoOptionError:
        print 'Error: Account Resource ID not configured in configuration file'
        exit(1)
    return account_resource_id


def get_named_logkey_group(group):
    groups = dict(config.items('LogGroups'))

    if group in groups:
        logkeys = filter(None, str(groups[group]).splitlines())
        for logkey in logkeys:
            if len(logkey) != 36:
                print 'Error: Logkey is not of correct length.'
                return
        return logkeys
    else:
        print 'Error: No group with name ' + '\'' + group + '\''
        return None


def get_named_logkey(nick):
    nicknames = dict(config.items('LogNicknames'))

    if nick in nicknames:
        logkey = (nicknames[nick],)
        if len(logkey[0]) != 36:
            print 'Error: Logkey is not of correct length. '
        else:
            return logkey
    else:
        print 'Error: No nickname with name ' + '\'' + nick + '\''
        return None


def get_query_from_nickname(qnick):
    qnicknames = dict(config.items('QueryNicknames'))

    if qnick in qnicknames:
        query = qnicknames[qnick]
        return query
    else:
        print 'Error: No query nickname with name ' + '\'' + qnick + '\''
        return None


def generate_headers(api_key_type, method=None, action=None, body=None):
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
            "authorization-api-key": "%s:%s" % (get_owner_apikey_id().encode('utf8'), base64.b64encode(signature))
        }
    return headers


def gensignature(api_key, date, content_type, request_method, query_path, request_body):
    hashed_body = base64.b64encode(hashlib.sha256(request_body).digest())
    canonical_string = request_method + content_type + date + query_path + hashed_body

    # Create a new hmac digester with the api key as the signing key and sha1 as the algorithm
    digest = hmac.new(api_key, digestmod=hashlib.sha1)
    digest.update(canonical_string)

    return digest.digest()

load_config()
