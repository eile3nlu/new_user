#!/bin/bash

# Usage: [First Name] [Last Name] [Role]

fName=$1
lName=$2
role=$3 # staff, ops, dev, ios, android, qu, hardware, fs, cs, sales
uName=$(tr "[:upper:]" "[:lower:]" <<< "${fName:0:1}")$(tr "[:upper:]" "[:lower:]" <<< "$lName")
password=$(cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9!@#$%&*' | fold -w 10 | head -n 1)

cat > .new_user.json <<- EOM
{
    "fName": "$fName",
    "lName": "$lName",
    "fullName": "",
    "note": "Delete",
    "email": "$uName@keypr.com",
    "emailPersonal": "$uName.old@keypr.com",
    "username": "$uName",
    "password": "1k$password!Z",
    "role": "$role",
    "kyiv": "",
    "unixid": ""
}
EOM

python secret_server.py
python gmail.py
source jumpcloud.sh
python confluence.py

#rm .new_user.json
