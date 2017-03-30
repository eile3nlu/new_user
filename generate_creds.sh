#!/bin/bash 
# generate credentials

#SecretServer
ssusername=$1
sspassword=$2
jcapikey=$3

cat > .credentials.json <<- EOM
{
    "secretserver":{
        "username": "$ssusername",
        "password": "$sspassword",
        "orgcode": "JKGD9",
        "domain": "keypr.com"
    },
    "jumpcloud":{
        "apikey": "$jcapikey"
    }
}
EOM
