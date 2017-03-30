#!/bin/bash

apikey=$(cat .credentials.json | jq ".jumpcloud.apikey" | sed "s/\"//g")
fName=$(cat .new_user.json | jq ".fName")
lName=$(cat .new_user.json | jq ".lName")
email=$(cat .new_user.json | jq ".email")
username=$(cat .new_user.json | jq ".username")
password=$(cat .new_user.json | jq ".password")


curl \
    -d '{"firstname": '$fName', "lastname": '$lName', "email" : '$email', "username" : '$username', "password": '$password'}' \
    -X 'POST' \
    -H 'Content-Type: application/json' \
    -H 'Accespt: application/json' \
    -H 'x-api-key: '$apikey'' \
    "https://console.jumpcloud.com/api/systemusers"
