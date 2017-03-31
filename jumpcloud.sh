#!/bin/bash

# get user information from .new_user.json
apikey=$(cat .credentials.json | jq ".jumpcloud.apikey" | sed "s/\"//g")
fName=$(cat .new_user.json | jq ".fName")
lName=$(cat .new_user.json | jq ".lName")
email=$(cat .new_user.json | jq ".email")
username=$(cat .new_user.json | jq ".username")
password=$(cat .new_user.json | jq ".password")
unixid=$(cat .new_user.json | jq ".unixid")
group=$(cat .new_user.json | jq ".role")

# modify group settings when role is defined
if [ "$group" == "staff" ]
then
    groupid=6001
else
    groupid=6001
fi

# create new user in jumpcloud
curl \
    -d '{"unix_guid": '$groupid', "unix_uid": '$unixid', "firstname": '$fName', "lastname": '$lName', "email" : '$email', "username" : '$username', "password": '$password'}' \
    -X 'POST' \
    -H 'Content-Type: application/json' \
    -H 'Accespt: application/json' \
    -H 'x-api-key: '$apikey'' \
    'https://console.jumpcloud.com/api/systemusers'
