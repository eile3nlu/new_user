#!/bin/bash

# Usage: [First Name] [Last Name] [Personal Email] [Role] [Unix ID] [Jira Ticket Number]

fName=$1
lName=$2
emailPersonal=$3
role=$4
unixid=$5
ticketNum=$6
password=$(cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1)

cat > .new_user.json <<- EOM
{
    "fName": "$fName",
    "lName": "$lName",
    "fullName": "$fName $lName",
    "note": "https://keyprprojects.atlassian.net/browse/HD-$ticketNum",
    "email": "${fName:0:1}$lName@keypr.com",
    "emailPersonal": "$emailPersonal",
    "username": "${fName:0:1}$lName",
    "password": "$password",
    "role": "$role",
    "unixid": "$unixid"
}
EOM

python secret_server.py
python gmail.py
source jumpcloud.sh
python confluence.py

#rm .new_user.json
