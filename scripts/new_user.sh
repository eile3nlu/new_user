#!/bin/bash

# Usage: [First Name] [Last Name] [Personal Email] [Role] [Contractor?] [Kyiv?] [Unix ID] [Jira Ticket Number]

fName=$1
lName=$2
uName=$(tr "[:upper:]" "[:lower:]" <<< "${fName:0:1}")$(tr "[:upper:]" "[:lower:]" <<< "$lName")
emailPersonal=$(tr "[:upper:]" "[:lower:]" <<< "$3")
role=$4 # staff, ops, dev, ios, android, qa, hardware, fs, cs, sales, contractor
contractor=$5
kyiv=$6
unixid=$7
ticketNum=$8
password=$(cat /dev/urandom | LC_CTYPE=C tr -dc 'a-zA-Z0-9!@#$%&*' | fold -w 12 | head -n 1)


cat > .new_user.json <<- EOM
{
    "fName": "$fName",
    "lName": "$lName",
    "fullName": "$fName $lName",
    "note": "https://keyprprojects.atlassian.net/browse/HD-$ticketNum",
    "email": "$uName@keypr.com",
    "emailPersonal": "$emailPersonal",
    "username": "$uName",
    "password": "$password",
    "role": "$role",
    "contractor": "$contractor",
    "kyiv": "$kyiv",
    "unixid": "$unixid"
}
EOM

python secret_server.py create
python gmail.py create
source jumpcloud.sh
python confluence.py create

echo 'Please copy and paste the above message into the ticket details (https://keyprprojects.atlassian.net/browse/HD-'$ticketNum')'

rm temp.txt
rm .new_user.json
