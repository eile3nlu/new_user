#!/usr/bin/env python
# automate gmail account creation

import httplib2
import sys
import json
import time
from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
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
    scope = ("https://www.googleapis.com/auth/%s" % (setType))

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
    if "admin" in setType:
        service = build("admin", "directory_v1", http=http)
    elif "gmail" in setType:
        service = build("gmail", "v1", http=http)

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

    print("Keypr Gmail: %s" % user["email"])

# add users to groups
def setgroups(service):
    
    # team mailing groups
    if user["role"].lower() == "staff":
        # staff@keypr.com
        print("Keypr Gmail Gropus: staff@keypr.com")
        groups = ["03vac5uf0tebadn"]

    elif user["role"].lower() == "dev":
        #  dev@keypr.com
        print("Keypr Gmail Groups: dev@keypr.com")
        groups = ["03as4poj18f1ku8"]

    elif user["role"].lower() == "ops":
        # bridge-ops@keypr.com, dev@keypr.com, kcs-alerts@keypr.com, ops@keypr.com, security@keypr.com, service-status@keypr.com, build@keypr.com
        print("Keypr Gmail Groups: bridge-ops@keypr.com, dev@keypr.com, kcs-alerts@keypr.com, ops@keypr.com, security@keypr.com, service-status@keypr.com, build@keypr.com")
        groups = ["00pkwqa10t6184d", "03as4poj18f1ku8", "01baon6m2p11k2p", "00tyjcwt0jo3gxm", "00ihv6361eix8zb", "035nkun23dv4k8i", "03x8tuzt0lobslp"]

    elif user["role"].lower() == "ios":
        # dev@keypr.com, ios-dev@keypr.com
        print("Keypr Gmail Groups: dev@keypr.com, ios-dev@keypr.com")
        groups = ["03as4poj18f1ku8", "03oy7u292fyscdg"]
        
    elif user["role"].lower() == "android":
        # dev@keypr.com, android-dev@keypr.com
        print("Keypr Gmail Groups: dev@keypr.com, android-dev@keypr.com")
        groups = ["03as4poj18f1ku8", "02fk6b3p49a7k54"]

    elif user["role"].lower() == "qa":
        # dev@keypr.com, qateam@keypr.com, testeng@keypr.com
        print("Keypr Gmail Groups: dev@keypr.com, qateam@keypr.com, testeng@keypr.com")
        groups = ["03as4poj18f1ku8", "00pkwqa130iy7m3", "030j0zll28x34h6"]

    elif user["role"].lower() == "hardware":
        # dev@keypr.com, kilt@keypr.com
        print("Keypr Gmail Groups: dev@keypr.com, kilt@keypr.com")
        groups = ["03as4poj18f1ku8", "02bn6wsx190y7ep"]

    elif user["role"].lower() == "fs":
        # fieldservices@keypr.com, support@keypr.com, supportafterhours@keypr.com, updates@keypr.com
        print("Keypr Gmail Groups: fieldservices@keypr.com, support@keypr.com, supportafterhours@keypr.com, updates@keypr.com")
        groups = ["01y810tw3w17osf", "02s8eyo146al189", "04f1mdlm3pinoxb", "0111kx3o0iyeqei"]

    elif user["role"].lower() == "cs":
        # 
        print("Keypr Gmail Groups: ")
        groups = []

    elif user["role"].lower() == "sales":
        # sales@keypr.com
        print("Keypr Gmail Groups: sales@keypr.com")
        groups = ["04d34og824t1ihr"]
    
    # "Group" mailing groups
    if user["contractor"].lower() == "t":
        # external@keypr.com    
        print("Keypr Gmail Groups: external@keypr.com")
        groups.append(["03ygebqi16xg5kj"])

    else:

        if user["kyiv"].lower() == "t":
            print("Speical Groups: kyiv-team@keypr.com, staff@keypr.com")
            groups.append("023ckvvd2s3scaj")
            groups.append("03vac5uf0tebadn")
        else:
            print("Speical Groups: la-team@keypr.com, staff@keypr.com")
            groups.append("01ci93xb1za9tyq")
            groups.append("03vac5uf0tebadn")

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

def createmessage(TYPE):

    # load email templates 
    with open("email_templates.json") as templates:
        template = json.load(templates)

    if TYPE == "welcome":
        message = MIMEText((template[TYPE]["message"] % (user["fullName"], user["email"], user["password"], user["email"])), "html")
        message["to"] = user["emailPersonal"] 

    else:
        message = MIMEText(template[TYPE]["message"], "html")
        message["to"] = user["email"] 

    message["from"] = "ckoh@keypr.com"
    message["subject"] = template[TYPE]["title"]

    return {"raw": base64.urlsafe_b64encode(message.as_string())}

def sendemail(service, message):

    message = (service.users().messages().send(userId="me", body=message).execute())

def deletegroups(service):

    request = service.groups().list(userKey=user["email"])
    response = request.execute()

    groupids = []
    groups = []
    for groupid in response["groups"]:
       groupids.append(groupid["id"]) 
       groups.append(groupid["name"])

    for group in groupids:
        request = service.members().delete(memberKey=user["email"], groupKey=group)
        response = request.execute()

    print("Off-boarding (Gmail): Keypr gmail %s removed from %s groups" % (user["email"], groups))

def mvemail(service):

    userinfo = {
                "primaryEmail": user["emailPersonal"],
                "password": user["password"] 
                }

    request = service.users().update(userKey=user["email"], body=userinfo)
    response = request.execute()

    print("Off-boarding (Gmail): Keypr gmail changed %s -> %s" % (user["email"], user["emailPersonal"]))

def rmemailalias(service):

    request = service.users().aliases().delete(alias=user["email"], userKey=user["emailPersonal"])
    response = request.execute()

    print("Off-boarding (Gmail): Keypr gmail alias %s removed from %s" % (user["email"], user["emailPersonal"]))

def mkalias(service):

    userinfo = {
                "alias": user["email"]
                }

    if user["role"] == "staff":
        group = ""

    elif user["role"] == "ops":
        group = "ops-manager@keypr.com"

    elif user["role"] == "dev":
        group = "director-sw-eng@keypr.com"

    elif user["role"] == "ios":
        group = "director-sw-eng@keypr.com"

    elif user["role"] == "android":
        group = "director-sw-eng@keypr.com"

    elif user["role"] == "qa":
        group = "qa-manager@keypr.com"

    elif user["role"] == "hardware":
        group = "hw-manager@keypr.com"

    elif user["role"] == "fs":
        group = "fs-manager@keypr.com"

    elif user["role"] == "cs":
        group = "cs-manager@keypr.com"

    elif user["role"] == "sales":
        group = "ex-sales@keypr.com"

    request = service.groups().aliases().insert(groupKey=group, body=userinfo)
    response = request.execute()

    print("Off-boarding (Gmail): Keypr gmail %s added as alias to %s group" % (user["email"], group))

def main():

    # on-boarding
    if user["note"] != "Delete":
        # create email account
        userservice = gmailauth("admin.directory.user")
        mkemail(userservice)
        time.sleep(3)
    
        # set groups
        groupservice = gmailauth("admin.directory.group")
        setgroups(groupservice)
        time.sleep(3)

        # send email notifications
        mailservice = gmailauth("gmail.compose")

        message = createmessage("welcome")
        sendemail(mailservice, message)
        print("Welcome email: Sent to %s" % user["emailPersonal"])

        message = createmessage("calendar")
        sendemail(mailservice, message)
        print("Staff calendar email: Sent %s" % user["email"])
        time.sleep(3)

        # Only send slack invite to non-contractors (contractors on an as-needed basis)
        if user["contractor"].lower() == "f":
            message = createmessage("slack")
            sendemail(mailservice, message)
            print("Slack email: Sent to %s" % user["email"])
            time.sleep(3)


    # off-boarding
    else:

        # remove user from all groups
        groupservice = gmailauth("admin.directory.group")
        deletegroups(groupservice)
        time.sleep(3)

        # change email to .old
        # assuming that the users email is in the first initial last name format
        userservice = gmailauth("admin.directory.user")
        mvemail(userservice)
        time.sleep(3)

        # remove old keypr.com email from email alias
        userservice = gmailauth("admin.directory.user.alias")
        rmemailalias(userservice)
        time.sleep(3)

        # create alias on manager group
        userservice = gmailauth("admin.directory.group")
        mkalias(userservice)

if __name__ == "__main__":
    main()
