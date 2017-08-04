#!/usr/bin/env python
# Automatcially generate Secret Server password entry

import sys
import suds
import json
from pprint import pprint


class secret_server():

    def __init__(self):

        # load credentials
        with open(".credentials.json") as credentials:
            self.creds = json.load(credentials)

        # load new user details
        with open(".new_user.json") as new_user:
            self.user = json.load(new_user)

        self.client = suds.client.Client("https://www.secretserveronline.com/webservices/SSWebservice.asmx?wsdl")
        self.token = self.client.service.Authenticate(self.creds["secretserver"]["username"], self.creds["secretserver"]["password"], self.creds["secretserver"]["orgcode"], self.creds["secretserver"]["domain"])

    def search(self):

        # searches for IDs
        secretTypeSearch = client.service.GetSecretTemplates(token.Token)
        #folderSearch = client.service.SearchFolders(token.Token, "egress")

        pprint(secretTypeSearch)

    def mksecret(self, action):

        # on-boarding
        if action.lower() == "create":
            secretname  = ("%s, %s's reset/initial password" % (self.user["lName"], self.user["fName"])) 
            values = ["", self.user["email"], self.user["password"], self.user["note"], "", "", "", "" , ""]
            print("Secret Server: New password generated for %s, %s" % (self.user["lName"], self.user["fName"]))

        # off-boarding
        else:
            secretname  = ("%s, %s's reset/offboarding password" % (self.user["lName"], self.user["fName"])) 
            values = ["", self.user["email"], self.user["password"], "", "", "", "", "" , ""]
            print("Secret Server: New password generated for %s, %s" % (self.user["lName"], self.user["fName"]))

        # create secret
        secret = self.client.factory.create("AddSecret")
        secret.token = self.token.Token
        secret.secretTypeId = 2658234
        secret.secretName = secretname 

        if action.lower() == "create":
            secret.folderId = 112066 # on-boarding
        else:
            secret.folderId = 114965 # off-boarding

        secret.secretFieldIds = self.client.factory.create("ArrayOfInt")
        #Resource, Username, Password, Notes, keyfile1, keyfile2, keyfile3, keyfile4, keyfile 5
        secret.secretFieldIds.int = [12155710, 12155711, 12155712, 12155713, 12155714, 12155715, 12155716, 12155717, 12155718]
        secret.secretItemValues = self.client.factory.create("ArrayOfString")
        secret.secretItemValues.string = values 

        add = self.client.service.AddSecret(secret)

def main(action):

    secret = secret_server()
    secret.mksecret(action)

if __name__ == "__main__":

    action = sys.argv[1]
    main(action)
