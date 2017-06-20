#!/usr/bin/env python
# automate jira account creation

import sys
import json
from jira import JIRA
from pprint import pprint

class jira:

    def __init__(self):

        # load admin credentials
        with open(".credentials.json") as credentials:
            self.creds = json.load(credentials)

        # load new user information
        with open(".new_user.json") as new_user:
            self.user = json.load(new_user)
        
        self.JIRA_SERVER = self.creds["jira"]["server"]
        self.JIRA_USERNAME =  self.creds["jira"]["username"]
        self.JIRA_PASSWORD = self.creds["jira"]["password"]
        self.jc = JIRA(server=self.JIRA_SERVER, basic_auth=(self.JIRA_USERNAME, self.JIRA_PASSWORD))

    # add new user to jira (keyprprojects.atlassian.net)
    def add_user(self):

        # contractors do not get confluence access, on an as-needed basis
        if self.user["contractor"].lower() == "f":
            # username, email, directory(?), password, full name, notification, activation
            self.jc.add_user(self.user["email"], self.user["email"], 1, self.user["password"], self.user["fullName"], False, True)
            print("Jira/Confluence: User created - %s" % self.user["email"])

    # set users groups
    def add_group(self):

        # contractors do not get confluence access, on an as-needed basis
        if self.user["contractor"].lower() == "f":
            # Default groups
            # username, group name
            self.jc.add_user_to_group(self.user["email"], "internal-dev")
            self.jc.add_user_to_group(self.user["email"], "confluence-users")
            print("Jira/Confluence: Groups added - internal-dev, jira-users, confluence-users")

    def remove_group(self):
    
        self.jc.remove_user_from_group(self.user["email"], "internal-dev")
        self.jc.remove_user_from_group(self.user["email"], "confluence-users")
        self.jc.remove_user_from_group(self.user["email"], "jira-users")
        print("Jira/Confluence: Removed user from groups [internal-dev, confluence-users, jira-users]")

def main(action):

    client = jira()

    if action.lower() == "create":
        client.add_user()
        client.add_group()

    else:
        client.remove_group()


if __name__ == "__main__":
    
    action = sys.argv[1]
    main(action)
