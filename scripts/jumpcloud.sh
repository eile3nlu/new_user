#!/bin/bash

# get user information from .new_user.json
apikey=$(cat .credentials.json | jq ".jumpcloud.apikey" | sed "s/\"//g")
fName=$1
lName=$2
email=$3
emailPersonal=$4
username=$5
password=$6
unixid=$7
group=$8
contractor=$9
note=${10}

echo $fName
echo $lName
echo $email
echo $emailPersonal
echo $username
echo $password
echo $unixid
echo $group
echo $contractor
echo $note

# Contractors do not get jumpcloud accounts, on a as needed basis
if [ "$note" == 'Delete' ]
then

    # get user ID
    id=$(curl -sS \
        -d '{"filter": [{"username" : '$username'}]}' \
        -X 'POST' \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json' \
        -H 'x-api-key: '$apikey'' \
        "https://console.jumpcloud.com/api/search/systemusers" | jq ".results[0]._id" | tr -d \" > temp.txt)

    # update user information in jumpcloud
    curl -sS \
        -d '{"password": '$password', "email": '$emailPersonal', "tags": []}' \
        -X 'PUT' \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json' \
        -H 'x-api-key: '$apikey'' \
        'https://console.jumpcloud.com/api/systemusers/'$id > temp.txt

    echo "JumpCloud: user password changed, user email changed, user tags removed"

elif [ "$note" != 'Delete' ]
then

    echo 1
    if [ "$contractor" == 'f' ]
    then
        echo 2
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

        echo $groupid
        echo $unixid
        echo $fName
        echo $lName
        echo $email
        echo $username
        echo $password
        echo $tag
        echo $apikey
        # create new user in jumpcloud

        curl -sS \
            -X 'POST' \
            -d '{"unix_guid": '$groupid', "unix_uid": '$unixid', "firstname": '$fName', "lastname": '$lName', "email" : '$email', "username" : '$username', "password": '$password', "ldap_binding_user": "false", "enable_managed_uid": "true", "tags": '$tag'}' \
            -H 'Content-Type: application/json' \
            -H 'Accept: application/json' \
            -H 'x-api-key: '$apikey'' \
            'https://console.jumpcloud.com/api/systemusers'


            echo "JumpCloud: Account Created for $username"
    fi
fi
