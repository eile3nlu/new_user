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

# add users to groups
def setgroups(service):
    
    # will have to define set groups by role
    if user["role"].lower() == "staff":
        # staff@keypr.com
        groups = ["03vac5uf0tebadn"]

    elif user["role"].lower() == "dev":
        # staff@keypr.com, dev@keypr.com, internal@keypr.com
        groups = ["03vac5uf0tebadn", "03as4poj18f1ku8", "03o7alnk144585r"]

    elif user["role"].lower() == "ops":
        # staff@keypr.com, bridge-ops@keypr.com, dev@keypr.com, kcs-alerts@keypr.com, ops@keypr.com, security@keypr.com, service-status@keypr.com, build@keypr.com
        groups = ["03vac5uf0tebadn", "00pkwqa10t6184d", "03as4poj18f1ku8", "01baon6m2p11k2p", "00tyjcwt0jo3gxm", "00ihv6361eix8zb", "035nkun23dv4k8i", "03x8tuzt0lobslp"]

    elif user["role"].lower() == "ios":
        # staff@keypr.com, dev@keypr.com, ios-dev@keypr.com
        groups = ["03vac5uf0tebadn", "03as4poj18f1ku8", "03oy7u292fyscdg"]
        
    elif user["role"].lower() == "android":
        # staff@keypr.com, dev@keypr.com, android-dev@keypr.com
        groups = ["03vac5uf0tebadn", "03as4poj18f1ku8", "02fk6b3p49a7k54"]

    elif user["role"].lower() == "qa":
        # staff@keypr.com, dev@keypr.com, qateam@keypr.com, testeng@keypr.com
        groups = ["03vac5uf0tebadn", "03as4poj18f1ku8", "00pkwqa130iy7m3", "030j0zll28x34h6"]

    elif user["role"].lower() == "hardware":
        # staff@keypr.com, dev@keypr.com, kilt@keypr.com
        groups = ["03vac5uf0tebadn", "03as4poj18f1ku8", "02bn6wsx190y7ep"]

    elif user["role"].lower() == "fs":
        # staff@keypr.com, fieldservices@keypr.com, support@keypr.com, supportafterhours@keypr.com, updates@keypr.com
        groups = ["03vac5uf0tebadn", "01y810tw3w17osf", "02s8eyo146al189", "04f1mdlm3pinoxb", "0111kx3o0iyeqei"]

    elif user["role"].lower() == "cs":
        # staff@keypr.com
        groups = ["03vac5uf0tebadn"]

    elif user["role"].lower() == "sales":
        # staff@keypr.com, sales@keypr.com
        groups = ["03vac5uf0tebadn", "04d34og824t1ihr"]
    

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

    message = MIMEText(template[TYPE]["message"])
    message["to"] = user["email"] 
    message["from"] = "ckoh@keypr.com"
    message["subject"] = template[TYPE]["title"]

    return {"raw": base64.urlsafe_b64encode(message.as_string())}


def sendemail(service, message):

    message = (service.users().messages().send(userId="me", body=message).execute())


def main():

    # create email account
    userservice = gmailauth("admin.directory.user")
    mkemail(userservice)
    
    # set groups
    groupservice = gmailauth("admin.directory.group")
    setgroups(groupservice)
    

    # send email notifications
    #mailservice = gmailauth("gmail.compose")
    #message = createmessage("calendar")
    #sendemail(mailservice, message)
    #message = createmessage("slack")
    #sendemail(mailservice, message)

if __name__ == "__main__":
    main()
