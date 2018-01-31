#!/bin/bash
# offboarding older employee's whos emails dont follow the normal convention of first initial + last name

# Usage: ./rm_user_old.sh [First Name] [Last Name] [Email] [Role]

fName=$1
lName=$2
email=$3
role=$4 # staff, ops, dev, ios, android, qu, hardware, fs, cs, sales
uName=$(tr "[:upper:]" "[:lower:]" <<< "${fName:0:1}")$(tr "[:upper:]" "[:lower:]" <<< "$lName")
password=$(cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9!@#$%&*' | fold -w 10 | head -n 1)

cat > .new_user.json <<- EOM
{
    "fName": "$fName",
    "lName": "$lName",
    "fullName": "",
    "note": "Delete",
    "email": "$email@keypr.com",
    "emailPersonal": "$email.old@keypr.com",
    "username": "$email",
    "password": "1k$password!Z",
    "role": "$role",
    "kyiv": "",
    "unixid": ""
}
EOM

python secret_server.py delete
python gmail.py delete
source jumpcloud.sh
python confluence.py delete

rm .new_user.json
