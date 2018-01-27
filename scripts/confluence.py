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

        self.JIRA_SERVER = self.creds["jira"]["server"]
        self.JIRA_USERNAME =  self.creds["jira"]["username"]
        self.JIRA_PASSWORD = self.creds["jira"]["password"]
        self.jc = JIRA(server=self.JIRA_SERVER, basic_auth=(self.JIRA_USERNAME, self.JIRA_PASSWORD))

    # add new user to jira (keyprprojects.atlassian.net)
    def add_user(self, fullName, password, contractor, email):

        # contractors do not get confluence access, on an as-needed basis
        if contractor.lower() == "f":
            # username, email, directory(?), password, full name, notification, activation
            self.jc.add_user(email, email, 1, password, fullName, False, True)
            print("Jira/Confluence: User created - %s" % email)

    # set users groups
    def add_group(self, email, contractor):

        # contractors do not get confluence access, on an as-needed basis
        if contractor.lower() == "f":
            # Default groups
            # username, group name
            self.jc.add_user_to_group(email, "internal-dev")
            self.jc.add_user_to_group(email, "confluence-users")
            print("Jira/Confluence: Groups added - internal-dev, jira-users, confluence-users")

    def remove_group(self, email):
    
        self.jc.remove_user_from_group(email, "internal-dev")
        self.jc.remove_user_from_group(email, "confluence-users")
        self.jc.remove_user_from_group(email, "jira-users")
        print("Jira/Confluence: Removed user from groups [internal-dev, confluence-users, jira-users]")

def main(action, fullName, password, contractor, email):

    client = jira()

    if action.lower() == "create":
        client.add_user(fullName, password, contractor, email)
        client.add_group(email, contractor)

    else:
        client.remove_group(email)


if __name__ == "__main__":
    
    action = sys.argv[1]
    main(action)
