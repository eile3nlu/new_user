#!/usr/bin/env python
# automate jira account creation

import json
from jira import JIRA
from pprint import pprint

# auth
def auth(JIRA_SERVER, JIRA_USERNAME, JIRA_PASSWORD):

    jc = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_PASSWORD))

    return jc

# add new user to jira (keyprprojects.atlassian.net)
def add_user(jc, user):

    # username, email, directory(?), password, full name, notification, activation
    jc.add_user(user["email"], user["email"], 1, user["password"], user["fullName"], False, True)

# set users groups
def add_group(jc, user):

    # Default groups
    # username, group name
    jc.add_user_to_group(user["email"], "internal-dev")
    jc.add_user_to_group(user["email"], "confluence-users")

    if user["role"] == "staff":
        pass
    

def main():

    # load admin credentials
    with open(".credentials.json") as credentials:
        creds = json.load(credentials)

    # load new user information
    with open(".new_user.json") as new_user:
        user = json.load(new_user)
    
    jc = auth(creds["jira"]["server"], creds["jira"]["username"], creds["jira"]["password"])
    add_user(jc, user)
    add_group(jc, user)

if __name__ == "__main__":
    main()
