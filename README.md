**Logentries Command Line Interface**
==================
This document provides an overview of installing and using the Logentries Command Line Interface.
The CLI is build on the Logentries REST APIs and provides a tool to interact directly with the Logentries service outside of the UI. It is in beta and currently supports log event querying and account user management. New functionality will be continually added.

**Installation**
----------------

`pip install logentries-lecli`

or

`pip install git+https://github.com/rapid7/lecli`

or 

`pip install <path to project directory>`

**Note** 


If there is no lecli configuration file, a dummy config file will be created in config directory at first use of any lecli command. You should edit the file in the provided path on your shell with your API keys and other configurations after this first use.

Depending on your operating system the Lecli config can be located at the following paths:

If you're running on OSX, path to your configuration file should be:
    
    /Users/<username>/Library/Application Support/lecli/config.ini
    
If you're running on Debian, path to your configuration file should be:
    
    /home/<username>/.config/lecli/config.ini

We are using `appdirs` library for this and you can always refer to its user_config_dir attribute for locating the configuration file.

**Supported Platforms**

 * Linux - Tested on `Debian 8`
 * OSX   - Tested on `El Capitan`

**Configuration File**
----------------
In order to use the CLI you must first setup the configuration file with your API keys. 
Your account API keys are available at logentries.com. Under the account management section select the API Keys tab. For more information: [https://docs.logentries.com/docs/api-keys](https://docs.logentries.com/docs/api-keys)
Here you will get access to your account resource Id and be able to generate your Owner, Read/Write and Read-Only API keys. Note that only the account owner is allowed to generate an Owner API key. 

In order to do User and account management via the CLI an owner API key and account resource Id is required. Querying of events and logs can be done using the Read/Write API key.

Copy and paste your API keys into the AUTH section of the CLI configuration file 'config.ini'
```
[Auth]
account_resource_id = 912345678-aaaa-bbbb-1234-1234cb12345a
owner_api_key_id = 12345678-aaaa-bbbb-1234-1234cb12345b
owner_api_key = 12345678-aaaa-bbbb-1234-1234cb12345c
rw_api_key = 12345678-aaaa-bbbb-1234-1234cb12345d
```

You will also need to set your log management URL. This defaults to:
    
    https://rest.logentries.com/management

This value can be updated in the URL section of the CLI configuration file:

    [Url]
    log_management_url=https://<some_url>/management

**Query and Events**
--------------------
The event and query functionality of the CLI supports a number of different ways to query events and statistics.

####Recent Events

The 'get recentevents' command allows you to retrieve the most recent log events that have been sent to Logentries.
The logs to retrieve events from can be specified in a few ways. The Log IDs can be passed directly as a space separated list of log Ids, or you can take advantage of log groups and log nicknames. Log Ids can be obtained from the settings page or log set page of a log in the Logentries UI (https://logentries.com). Log nicknames can be passed using the '--lognick' '-n' arguments, log groups can be passed using the '--loggroup' '-g' arguments. For more information in setting up log nicknames and log groups, see the 'Log Nicknames and Groups' section below.
By default the 'get recentevents' command will return events for the last 20 minutes. The command also takes an optional time argument that allows you to specify how far back in time you wish to get events from; this is passed using '--last' or '-l' argument.
It is also possible to provide '-r' (--relative_range) to use relative time range functionality of the Logentries REST API. Check [supported patterns](#supported-relative-time-patterns).

Example usage: 
```
lecli get recentevents 12345678-aaaa-bbbb-1234-1234cb123456 -l 200
lecli get recentevents 12345678-aaaa-bbbb-1234-1234cb123456 -r 'last 2 hours'
lecli get recentevents -n mynicknamedlog -l 200
lecli get recentevents -g myloggroup -l 200
lecli get recentevents -g myloggroup -r 'last 1 week'
```

####Events
The 'get events' command allows for the retrieval of log events within defined time ranges. As with 'get recentevents', logs can be passed to the 'get events' command as a space separated list of log Ids, or you can take advantage of log groups and log nicknames.
The 'get events' command accepts time ranges in ISO-8601 human readable time format (YYYY-MM-DD HH:MM:SS); time ranges in this format can be passed using the '--datefrom' and '--dateto' arguments. Note, all time values are in UTC timezone. 
The command also accepts epoch time with second granularity. Epoch format time parameters can be passed using the '--timefrom' '-f' and '--timeto' '-t' arguments. 
It is also possible to provide '-r' (--relative_range) to use relative time range functionality of the Logentries REST API. Check [supported patterns](#supported-relative-time-patterns).

Example usage: 
```
lecli get events 12345678-aaaa-bbbb-1234-1234cb123456 -f 1465370400 -t 1465370500
lecli get events 12345678-aaaa-bbbb-1234-1234cb123456 --datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'
lecli get events 12345678-aaaa-bbbb-1234-1234cb123456 -r 'yesterday'
lecli get events --loggroup myloggroup --datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'
lecli get events --lognick mynicknamedlog --datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'
lecli get events --lognick mynicknamedlog -r 'last 3 weeks'
```

####Query
The 'query' command allows you to run LEQL queries on logs from the command line. Logs can be passed to the 'query' command using a space separated list of log Ids, log groups or log nicknames.
As with the 'events' command, 'query' accepts time ranges in ISO-8601 human readable time format (YYYY-MM-DD HH:MM:SS); time ranges in this format can be passed using the '--datefrom' and '--dateto' arguments.
It also accepts epoch time with second granularity. Epoch format time parameters can be passed using the '--timefrom' '-f' and '--timeto' '-t' arguments.
It is also possible to provide '-r' (--relative_range) to use relative time range functionality of the Logentries REST API. Check [supported patterns](#supported-relative-time-patterns).

Any LEQL query type that can be used in the advanced mode in the Logentries UI can also be used with the 'query' command. The LEQL query is passed as a string using the '--leql' '-l' argument. For detailed information on using LEQL see https://logentries.com/doc/search/
A query can return three types of results. For searches just using a where() and without any calculate or groupby functions then the CLI will print the list of matching log events. Other queries will return either statistical or timeseries data, the CLI willretty print both of these.

Similar to log nicknames, query nicknames allow well known queries to be set in the configuration file and easily used as part of a query command. A query shortcut can be used instead of a leql query using the '--querynick' '-q' argument.

Example usage:
```
lecli query 12345678-aaaa-bbbb-1234-1234cb123456 -q 'where(method=GET) calculate(count)' -f 1465370400 -t 1465370500
lecli query 12345678-aaaa-bbbb-1234-1234cb123456 -q 'where(method=GET) calculate(count)'  --datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'
lecli query 12345678-aaaa-bbbb-1234-1234cb123456 -q 'where(method=GET) calculate(count)'  -r 'last 2 days'
lecli query --loggroup myloggroup --leql 'where(method=GET) calculate(count)' --datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'
lecli query --lognick mynicknamedlog --leql 'where(method=GET) calculate(count)' --datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'
lecli query --lognick mynicknamedlog -q testquery --datefrom '2016-05-18 11:04:00' --dateto '2016-05-18 11:09:59'
lecli query --lognick mynicknamedlog -q testquery -r 'last 15 mins'
```

####Supported Relative Time Patterns
Logentries REST API also supports relative time ranges instead of absolute `start` and `end` dates. All relative times are case insensitive and supported patterns are like these: 

- `today`
- `yesterday`
- `last n timeunits` where timeunits can be:
  - min, mins, minute, minutes
  - hr, hrs, hour, hours
  - day, days
  - week, weeks
  - month, months
  - year, years
    

**Log Nicknames, Log Groups, and Query Nicknames**
--------------------------------------------------
The CLI supports the use of log nicknames and log groups via the configuration file. This makes searching well known or large lists of logs much simpler as you do not need to pass in lists of log Ids.

####Log Nicknames
Log nicknames allow an alias for a single log to be configured, this is done in the LogNicknames section of the configuration file. 
```
[LogNicknames]
testlog = 12345678-aaaa-bbbb-1234-1234cb123456
```

####Log Groups
Log groups allow an alias for a list of log Ids to be created. These can be setup in the LogGroups section of the configuration file. 
```
[LogGroups]
testgroup =
    12345678-aaaa-bbbb-1234-1234cb123456
    12345678-aaaa-bbbb-1234-1234cb123457
```

####Query Nicknames
Query nicknames provide an easy way to add aliases for long or frequently run queries. These are setup in the QueryNicknames section of the configuration file.
```
[QueryNicknames]
testquery = where(logID) groupby(logID) calculate(count) sort(desc) limit(3)
```

**User and Account Management**
-------------------------------
The user and account management functionality of the CLI can only be used with a valid owner API key. The configuration file must contain the account_resource_id, owner_api_key_id and owner_api_key in the Auth section. These are all available from the account management and API keys section at https://logentries.com.
It is worth noting that if your account does not have a specific owner set then some user management functions may fail with a 500 error; to check if an owner is set the 'getowner' command below can be used. If no owner is set then you must regenerate the owner API key, at which point you will be asked to set an account owner.

####Get Users
The 'get users' command will return a list of all users that have access to the account for which the CLI has been configured. The command will return the users first and last name, email address, user key and the last time they logged in. The 'get users' command does not accept any arguments.

Example usage:
```
lecli get users
```

####Add User
The 'create user' command allows you to add a user to your account. There are two ways to add users, depending on whether they are a new or existing user. 
A new user is a user that has no Logentries account. 

To add a new user you must provide their first and last name, and email address. If successfully added the CLI will print the users account information, including their newly generated user key. A user added via the CLI must then go to https://logentries.com/user/password-reset/ and enter their email address. They will then be sent a link that they can use to setup the password for their new account.

A new user can be added using the following command
```
lecli create user -f John -l Smith -e john.smith@email.com
```

To add an existing user (i.e. a user that already has a Logentries account, even if not associated with your account), you must first obtain their user key. The user can obtain their user key from the account management page of the Logentries application at https://logentries.com

An existing user can be added to your account use the following command
```
lecli create user -u 12345678-aaaa-bbbb-1234-1234cb123456
```

####Delete User
The 'delete user' command allows for the removal of a user from your account and deletion of the users account from Logentries.
If the user is associated with only your account then the users access to your account will be removed and the users account deleted. 
However, if the user is associated to any other account then access to your account will be removed but the users Logentries account and any association to other accounts will remain.

To delete a user use the following command
```
lecli delete user -u 12345678-aaaa-bbbb-1234-1234cb123456
```

####Get Account Owner
The 'get owner' command allows you to retrieve the details of the account owner, this  is done using the following command
```
lecli get owner
```

**Team Management**
-------------------
Team management requires a valid read-write API key in your configuration file. The configuration file must contain a valid account_resource_id and rw_api_key in Auth section.

####Get Teams
Get all teams associated with this accounts.

     lecli get teams
     
####Get a Specific Team
Get a specific team by providing team UUID.

    lecli get team <team id>
    
####Create a New Team
Create a new team with the given name.

    lecli create team <new name>
    
####Delete a Team
Delete a team with the given UUID.

    lecli delete team <team id>
    
####Rename a Team
Rename a team with the given UUID to given name.

    lecli rename team <team id> <team name>

####Add User to a Team
Add a new user to a team with the given UUID and user UUID respectively.

    lecli update team add_user <team id> <user key>

####Delete User from a Team
Add a new user to a team with the given UUID and user UUID respectively.

    lecli update team delete_user <team id> <user key>


**Account Usage**
-----------------
Account usage can be retrieved using lecli 'get usage' command along with 'start' and 'end' date ranges to be queried. 
A valid read-write api key in configuration file is required for this operation.
*Note:* 'start' and 'end' dates should be in ISO-8601 format: 'YYYY-MM-DD', example: '2016-01-01'

    lecli get usage -s <start date> -e <end date>


**Saved Query Management**
--------------------------
Saved queries that belong to an account can be managed via lecli. Lecli supports creating(POST), listing(GET ALL), retrieving(GET), deleting(DELETE) and updating(PATCH) saved queries via command line. 
This operation required read-write api key to be in lecli config file.

####List saved queries
Get a list of saved queries belongs to the used account.

Example:

    lecli get savedqueries

####Get a saved query
Get a specific saved query
Mandatory positional argument:
- UUID of the saved query to be retrieved.

Example:

    lecli get savedquery <uuid of the saved query>

####Create a new saved query
Create a new saved query with the given arguments:

Mandatory positional arguments:
- Name: Name of the saved query
- Statement: LEQL statement of the saved query
Optional named arguments:
- '-f': From timestamp - epoch in milliseconds
- '-t': To timestamp - epoch in milliseconds
- '-r': Relative time range(cannot be defined with from and/or to fields)
- '-l': Logs of the saved query. Multiple logs can be provided with a colon(:) separated logs string.

Examples:

    lecli create savedquery 'new_saved_query' 'where(event)'
    lecli create savedquery 'new_saved_query' 'where(event)' -l '123456789012345678901234567890123456'
    lecli create savedquery 'new_saved_query' 'where(event)' -r 'last 5 min' -l '123456789012345678901234567890123456:123456789012345678901234567890123457'
    lecli create savedquery 'new_saved_query' 'where(event)' -f 1481558514334 -t 1481562814000 -l '123456789012345678901234567890123456:123456789012345678901234567890123457'

####Update a saved query
Update a saved query with the given arguments.

Mandatory positional argument:
- UUID of the saved query to be updated.

Optional named arguments:
- '-n': Name of the saved query
- '-s': LEQL statement of the saved query
- '-f': From timestamp - epoch in milliseconds
- '-t': To timestamp - epoch in milliseconds
- '-r': Relative time range(cannot be defined with from and/or to fields) 
- '-l': Logs of the saved query. To provide multiple logs, colon(:) separated logs can be used.
    
Examples:

    lecli update savedquery -n 'new_name_for_query' -s 'where(/*/)'
    lecli update savedquery -n 'new_name_for_query' -s 'where(/*/)' -r 'last 10 days'
    lecli update savedquery -n 'new_name_for_query' -f 1481558514334 -t 1481562814000
    lecli update savedquery -n 'new_name_for_query' -l '123456789012345678901234567890123456'

####Delete a saved query
Delete a saved query.
Mandatory positional argument:
- UUID of the saved query to be deleted.

Example:

    lecli delete savedquery <uuid of the saved query>
    
     
**Log Management**
----------------------

The CLI allows you to retrieve and manage logs. You can retrieve a specific or all logs, as well as create, delete, replace and rename logs. 
Retrieving logs requires a valid read-only API key in your configuration file.
The remaining actions also require a valid read-write API key.

####Retrieve all logs
Retrieve all logs:

Example:
    
    lecli get logs
    
####Retrieve a specific log
Retrieve a log with a given ID.

Mandatory positional argument:
- UUID of the log to the retrieved.

Example:
    
    lecli get log <log_id>
    
####Create a new log
Create a new log with a given name or from a provided JSON file.

Logs can be created with a given name and default values by providing the name. 
If you wish to supply additional information, the (relative or full) path to a JSON file can be provided.

Note that only creation of a single log object is supported at this time.

Example JSON:

    {
        "name": "log name",
        "logsets_info": [
            {
                "id": "logset id",
                "name": "logset name"
            }
         ]
     }
     
Example:

    lecli create log -n <name>
    lecli create log -f <path_to_json_file>
    
    
####Rename a log
Rename a log with the provided ID.

Mandatory positional arguments:
- UUID of the log to be renamed
- New name of the log

Example:
    
    lecli rename log <log_id> <new_name>
    
####Update a log
Add information to a given log.

Mandatory positional arguments:
- UUID of the log to be updated
- Full or relative path to a JSON file containing the updated log information

Example:
    
    lecli update log <log_id> <path_to_json_file>
    

####Delete a log
Deletes a log with the provided ID.

Mandatory positional argument:
- UUID of the log to be deleted

Example:

    lecli delete log <log_id>
    
    
####Replace a log
Replaces a log with the provided log.

Mandatory positional argument:
- UUID of the log to be replaced
- Full or relative path to JSON file containing a valid log object

Example:

    lecli replace log <log_id> <path_to_json_file>