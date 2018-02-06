#!/bin/bash

display_usage() {
	echo "Require JQ(https://stedolan.github.io/jq/) and lecli(https://github.com/rapid7/lecli)"
	echo -e "\nUsage:\n ./logentries_tail.sh [logset_name] \n"
	echo -e "\nUsage:\n ./logentries_tail.sh my_production_logset_name \n"
}

# if less than two arguments supplied, display usage
if [  $# -le 0 ]
then
    display_usage
    exit 1
fi

# check whether user had supplied -h or --help . If yes display usage
if [[ ( $# == "--help") ||  $# == "-h" ]]
then
    display_usage
    exit 0
fi

logset_name=$1

echo -e "tail of ${logset_name}"

# https://github.com/stedolan/jq/issues/1124#issuecomment-205346895
jq_logset_key_query=(jq -r '.logsets[] | select(has("logs_info")) | select(.logs_info | length > 0) | .logs_info[] | select(.name | contains("'${logset_name}'") ) .id')
logset_key=`lecli get logsets | "${jq_logset_key_query[@]}" | uniq | sort | paste -s -`

echo -e "${logset_name} log key: ${logset_key}\n"

lecli tail events ${logset_key}