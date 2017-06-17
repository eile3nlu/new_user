#!/bin/bash

# get user information from .new_user.json
apikey=$(cat .credentials.json | jq ".jumpcloud.apikey" | sed "s/\"//g")
fName=$(cat .new_user.json | jq ".fName")
lName=$(cat .new_user.json | jq ".lName")
email=$(cat .new_user.json | jq ".email")
emailPersonal=$(cat .new_user.json | jq ".emailPersonal")
username=$(cat .new_user.json | jq ".username")
password=$(cat .new_user.json | jq ".password")
unixid=$(cat .new_user.json | jq ".unixid")
group=$(cat .new_user.json | jq ".role" | tr -d \")
contractor=$(cat .new_user.json | jq ".contractor" | tr -d \")
note=$(cat .new_user.json | jq ".note" | tr -d \")

# Contractors do not get jumpcloud accounts, on a as needed basis
if [ "$note" == 'Delete' ]
then

    # get user ID
    id=$(curl \
        -d '{"filter": [{"username" : '$username'}]}' \
        -X 'POST' \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json' \
        -H 'x-api-key: '$apikey'' \
        "https://console.jumpcloud.com/api/search/systemusers" | jq ".results[0]._id" | tr -d \")

    # update user information in jumpcloud
    curl \
        -d '{"password": '$password', "email": '$emailPersonal', "tags": []}' \
        -X 'PUT' \
        -H 'Content-Type: application/json' \
        -H 'Accespt: application/json' \
        -H 'x-api-key: '$apikey'' \
        'https://console.jumpcloud.com/api/systemusers/'$id

    echo "JumpCloud: user password changed, user email changed, user tags removed"

elif [ "$note" != 'Delete' ]
then

    if [ "$contractor" == 'f' ]
    then
        # modify group settings when role is defined
        if [ "$group" == "staff" ] || [ "$group" == "cs" ] || [ "$group" == "fs" ] || [ "$group" == "sales" ]  
        then
            groupid=6001
            tags=()
            echo "JumpCloud : Tags added - "
        else
            groupid=5002
            tags=(
                '"artifactory"',
                '"keyprdev-group"'
            )
            echo "JumpCloud: Tags added - keyprdev-group, artifactory"
        fi

        # create string for tags
        tag="["
        for x in "${tags[@]}"
        do
            tag+="$x"
        done
        tag+="]"

        # create new user in jumpcloud
        curl \
            -d '{"unix_guid": '$groupid', "unix_uid": '$unixid', "firstname": '$fName', "lastname": '$lName', "email" : '$email', "username" : '$username', "password": '$password', "ldap_binding_user": "true", "tags": '$tag'}' \
            -X 'POST' \
            -H 'Content-Type: application/json' \
            -H 'Accespt: application/json' \
            -H 'x-api-key: '$apikey'' \
            'https://console.jumpcloud.com/api/systemusers'
    fi
fi
