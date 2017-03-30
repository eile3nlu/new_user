#!/usr/bin/env python

import httplib2
import sys
import json
from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from pprint import pprint

def gmailauth():
    
    # load secret
    with open(".client_secret.json") as secret:
        client = json.load(secret)
    client_id = client["installed"]["client_id"]
    client_secret = client["installed"]["client_secret"]
    scope = "https://www.googleapis.com/auth/admin.directory.user"

    # create flow object 
    flow = OAuth2WebServerFlow(client_id, client_secret, scope)

    # create / refresh credentials
    storage = Storage(".credentials.dat")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())

    # create / authorize http object to handle HTTP requests
    http = httplib2.Http()
    http = credentials.authorize(http)

    # create object to make API calls
    service = build("admin", "directory_v1", http=http)

    return service

def mkemail(service):

    # load new user info
    with open(".new_user.json") as new_user:
        user = json.load(new_user)

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

def main():

    service = gmailauth()
    mkemail(service)

if __name__ == "__main__":
    main()
