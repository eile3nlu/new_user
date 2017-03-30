#!/usr/bin/env python
# automate gmail account creation

import httplib2
import sys
import json
from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from pprint import pprint

# load new user info
with open(".new_user.json") as new_user:
    user = json.load(new_user)

# authenticate api resource
def gmailauth(setType):
    
    # load secret
    with open(".client_secret.json") as secret:
        client = json.load(secret)
    client_id = client["installed"]["client_id"]
    client_secret = client["installed"]["client_secret"]
    scope = ("https://www.googleapis.com/auth/admin.directory.%s" % (setType))

    # create flow object 
    flow = OAuth2WebServerFlow(client_id, client_secret, scope)

    # create / refresh credentials
    storage = Storage(".%s_credentials.dat" % (setType))
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())

    # create / authorize http object to handle HTTP requests
    http = httplib2.Http()
    http = credentials.authorize(http)

    # create object to make API calls
    service = build("admin", "directory_v1", http=http)

    return service

# create new user email based on given information
def mkemail(service):


    userinfo = {
                "primaryEmail": user["email"],
                "name": {
                            "givenName": user["fName"],
                            "familyName": user["lName"] 
                        },
                "password": user["password"] 
                }

    request = service.users().insert(body=userinfo)
    response = request.execute()

# add users to groups
def setgroups(service, role):
    
    # will have to define set groups by role
    if role == user["role"]:
        groups = ["03vac5uf0tebadn"]

    userinfo = {
                "kind": "admin#directory#member",
                "type": "USER",
                "email": user["email"],
                "role": "MEMBER"
                }

    for group in groups:
        request = service.members().insert(body=userinfo, groupKey=group)
        response = request.execute()

# search groups for a list of ID's
def searchgroups(service):

    request = service.groups().list(domain = "keypr.com")
    response = request.execute()

    pprint(response)

def searchemail(service):
    
    request = service.users().list(domain="keypr.com", showDeleted = True)
    response = request.execute()

    pprint(response)

def main():

    userservice = gmailauth("user")
    mkemail(userservice)
    groupservice = gmailauth("group")
    # options: staff.  Will add more later 
    setgroups(groupservice, "staff")

if __name__ == "__main__":
    main()
