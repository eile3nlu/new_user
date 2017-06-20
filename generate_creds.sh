#!/bin/bash 
# generate credentials

ssusername=$1 #Secret Server
sspassword=$2
jcapikey=$3 #JumpCloud
jirausername=$4 #Jira/Confluence
jirapassword=$5

cat > scripts/.credentials.json <<- EOM
{
    "secretserver":{
        "username": "$ssusername",
        "password": "$sspassword",
        "orgcode": "JKGD9",
        "domain": "keypr.com"
    },
    "jumpcloud":{
        "apikey": "$jcapikey"
    },
    "jira":{
        "server": "https://keyprprojects.atlassian.net",
        "username": "$jirausername",
        "password": "$jirapassword"
    }
}
EOM
