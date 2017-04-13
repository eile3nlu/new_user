#!/bin/bash

# Usage: [First Name] [Last Name] [Keypr Email]

fName=$1
lName=$2
email=$3
password=$(cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1)

cat > .new_user.json <<- EOM
{
    "fName": "$fName",
    "lName": "$lName",
    "fullName": "",
    "note": "",
    "email": "$email",
    "emailPersonal": "",
    "username": "",
    "password": "$password",
    "role": "",
    "kyiv": "",
    "unixid": ""
}
EOM

#python secret_server.py
#python gmail.py
#source jumpcloud.sh
#python confluence.py

#rm .new_user.json
