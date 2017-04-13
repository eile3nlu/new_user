#!/usr/bin/env python
# Automatcially generate Secret Server password entry

import sys
import suds
import json

client = suds.client.Client("https://www.secretserveronline.com/webservices/SSWebservice.asmx?wsdl")

def ssauth():

    # load credentials
    with open(".credentials.json") as credentials:
        creds = json.load(credentials)

    # create token
    token = client.service.Authenticate(creds["secretserver"]["username"], creds["secretserver"]["password"], creds["secretserver"]["orgcode"], creds["secretserver"]["domain"])

    # searches for IDs
    #secretTypeSearch = client.service.GetSecretTemplates(token.Token)
    #folderSearch = client.service.SearchFolders(token.Token, "on")

    return token

def mksecret(token):

    # load new user details
    with open(".new_user.json") as new_user:
        user = json.load(new_user)

    # on-boarding
    if user["username"] != "":
        secretname  = ("%s, %s's reset/initial password" % (user["lName"], user["fName"])) 
        values = ["", user["email"], user["password"], user["note"], "", "", "", "" , ""]

    # off-boarding
    else:
        secretname  = ("%s, %s's reset/offboarding password" % (user["lName"], user["fName"])) 
        values = ["", user["email"], user["password"], "", "", "", "", "" , ""]

    # create secret
    secret = client.factory.create("AddSecret")
    secret.token = token.Token
    secret.secretTypeId = 2658234
    secret.secretName = secretname 
    secret.folderId = 112066
    secret.secretFieldIds = client.factory.create("ArrayOfInt")
    #Resource, Username, Password, Notes, keyfile1, keyfile2, keyfile3, keyfile4, keyfile 5
    secret.secretFieldIds.int = [12155710, 12155711, 12155712, 12155713, 12155714, 12155715, 12155716, 12155717, 12155718]
    secret.secretItemValues = client.factory.create("ArrayOfString")
    secret.secretItemValues.string = values 

    add = client.service.AddSecret(secret)

def main():

    token = ssauth()
    mksecret(token)

if __name__ == "__main__":
    main()
