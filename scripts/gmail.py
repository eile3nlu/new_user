#!/usr/bin/env python
# automate gmail account creation
# if script stops working tokens might have expired.  
# remove action arg and run script to re-authorize
# todo: create a script in 

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

class new_account:
    
    def __init__(self):

        # load secret
        with open(".client_secret.json") as secret:
            self.client = json.load(secret)

        # load new user info
        with open(".new_user.json") as new_user:
            self.user = json.load(new_user)

        # load email templates 
        with open("../templates/email_templates.json") as templates:
            self.template = json.load(templates)

        self.client_id = self.client["installed"]["client_id"]
        self.client_secret = self.client["installed"]["client_secret"]

        self.userservice = self.gmailauth("admin.directory.user")
        self.groupservice = self.gmailauth("admin.directory.group")
        self.mailservice = self.gmailauth("gmail.compose")

        self.aliasservice = self.gmailauth("admin.directory.user.alias")

        self.email_sender = "chris@keypr.com"

    ### ON-BOARDING ###

    # authenticate api resource
    def gmailauth(self, setType):
    
        scope = ("https://www.googleapis.com/auth/%s" % (setType))

        # create flow object 
        flow = OAuth2WebServerFlow(self.client_id, self.client_secret, scope)

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
    def mkemail(self):

        userinfo = {
                    "primaryEmail": self.user["email"],
                    "name": {
                                "givenName": self.user["fName"],
                                "familyName": self.user["lName"] 
                            },
                    "password": self.user["password"] 
                    }

        request = self.userservice.users().insert(body=userinfo)
        response = request.execute()

        print("Gmail: Account created - %s" % self.user["email"])

    # add users to groups
    def setgroups(self):
    
        # team mailing groups
        if self.user["role"].lower() == "staff":
            # staff@keypr.com
            print("Gmail: Groups added - ")
            groups = []

        elif self.user["role"].lower() == "dev":
            #  dev@keypr.com
            print("Gmail: Groups added - dev@keypr.com")
            groups = ["03as4poj18f1ku8"]

        elif self.user["role"].lower() == "ops":
            # bridge-ops@keypr.com, dev@keypr.com, kcs-alerts@keypr.com, ops@keypr.com, security@keypr.com, service-status@keypr.com, build@keypr.com
            print("Gmail: Groups added - bridge-ops@keypr.com, dev@keypr.com, kcs-alerts@keypr.com, ops@keypr.com, security@keypr.com, service-status@keypr.com, build@keypr.com")
            groups = ["00pkwqa10t6184d", "03as4poj18f1ku8", "01baon6m2p11k2p", "00tyjcwt0jo3gxm", "00ihv6361eix8zb", "035nkun23dv4k8i", "03x8tuzt0lobslp"]

        elif self.user["role"].lower() == "ios":
            # dev@keypr.com, ios-dev@keypr.com
            print("Gmail: Groups added - dev@keypr.com, ios-dev@keypr.com")
            groups = ["03as4poj18f1ku8", "03oy7u292fyscdg"]
        
        elif self.user["role"].lower() == "android":
            # dev@keypr.com, android-dev@keypr.com
            print("Gmail: Groups added - dev@keypr.com, android-dev@keypr.com")
            groups = ["03as4poj18f1ku8", "02fk6b3p49a7k54"]

        elif self.user["role"].lower() == "qa":
            # dev@keypr.com, qateam@keypr.com, testeng@keypr.com
            print("Gmail: Groups added - dev@keypr.com, qateam@keypr.com, testeng@keypr.com")
            groups = ["03as4poj18f1ku8", "00pkwqa130iy7m3", "030j0zll28x34h6"]

        elif self.user["role"].lower() == "hardware":
            # dev@keypr.com, kilt@keypr.com
            print("Gmail: Groups added - dev@keypr.com, kilt@keypr.com")
            groups = ["03as4poj18f1ku8", "02bn6wsx190y7ep"]

        elif self.user["role"].lower() == "fs":
            # fieldservices@keypr.com, support@keypr.com, supportafterhours@keypr.com, updates@keypr.com
            print("Gmail: Groups added - fieldservices@keypr.com, support@keypr.com, supportafterhours@keypr.com, updates@keypr.com")
            groups = ["01y810tw3w17osf", "02s8eyo146al189", "04f1mdlm3pinoxb", "0111kx3o0iyeqei"]

        elif self.user["role"].lower() == "cs":
            print("Gmail: Groups added - ")
            groups = []

        elif self.user["role"].lower() == "sales":
            # sales@keypr.com
            print("Gmail: Groups added - sales@keypr.com")
            groups = ["04d34og824t1ihr"]
    
        # "Group" mailing groups
        if self.user["contractor"].lower() == "t":
            # external@keypr.com    
            print("Gmail: Groups added - external@keypr.com")
            groups.append("03ygebqi16xg5kj")

        else:

            if self.user["kyiv"].lower() == "t":
                print("Gmail: Speical Groups - kyiv-team@keypr.com, staff@keypr.com")
                groups.append("023ckvvd2s3scaj")
                groups.append("03vac5uf0tebadn")
            else:
                print("Gmail: Speical Groups - la-team@keypr.com, staff@keypr.com")
                groups.append("01ci93xb1za9tyq")
                groups.append("03vac5uf0tebadn")

        userinfo = {
                    "kind": "admin#directory#member",
                    "type": "USER",
                    "email": self.user["email"],
                    "role": "MEMBER"
                    }

        for group in groups:
            request = self.groupservice.members().insert(body=userinfo, groupKey=group)
            response = request.execute()

    def sendemail(self, TYPE):

        # Change receipeient (message["to"]) based on email type.
        if TYPE == "welcome":

            #override staff welcome with contractor welcome for contractors
            if self.user["contractor"].lower() == "t":
                TYPE = 'welcome_contractor'

            message = MIMEText((self.template[TYPE]["message"] % (self.user["fullName"], self.user["email"], self.user["password"], self.user["email"])), "html")
            message["to"] = self.user["emailPersonal"] 

        else:
            message = MIMEText(self.template[TYPE]["message"], "html")
            message["to"] = self.user["email"] 

        # set from, subject and encoding
        message["from"] = self.email_sender 
        message["subject"] = self.template[TYPE]["title"]
        message_text =  {"raw": base64.urlsafe_b64encode(message.as_string())}

        # only send welcome to contractors
        if self.user["contractor"].lower() == "t":
            if TYPE == "welcome_contractor":
                send_message = (self.mailservice.users().messages().send(userId="me", body=message_text).execute())
                print("Gmail: Email sent - %s" % TYPE)
        else:
            send_message = (self.mailservice.users().messages().send(userId="me", body=message_text).execute())
            print("Gmail: Email sent - %s" % TYPE)

    ### OFF BOARDING ###

    def deletegroups(self):

        request = self.groupservice.groups().list(userKey=self.user["email"])
        response = request.execute()

        groupids = []
        groups = []

        for groupid in response["groups"]:
            groupids.append(groupid["id"]) 
            groups.append(groupid["name"])

        for group in groupids:
            request = self.groupservice.members().delete(memberKey=self.user["email"], groupKey=group)
            response = request.execute()

        print("Gmail: %s removed from %s groups" % (self.user["email"], groups))

    def mvemail(self):

        userinfo = {
                    "primaryEmail": self.user["emailPersonal"],
                    "password": self.user["password"]
                    }

        request = self.userservice.users().update(userKey=self.user["email"], body=userinfo)
        response = request.execute()

        print("Gmail: Changed %s -> %s" % (self.user["email"], self.user["emailPersonal"]))

    def rmemailalias(self):

        request = self.aliasservice.users().aliases().delete(alias=self.user["email"], userKey=self.user["emailPersonal"])
        response = request.execute()

        print("Gmail: Alias %s removed from %s" % (self.user["email"], self.user["emailPersonal"]))

    def mkalias(self):

        userinfo = {
                    "alias": self.user["email"]
                    }

        if self.user["role"] == "staff":
            group = ""

        elif self.user["role"] == "ops":
            group = "ops-manager@keypr.com"

        elif self.user["role"] == "dev":
            group = "director-sw-eng@keypr.com"

        elif self.user["role"] == "ios":
            group = "director-sw-eng@keypr.com"

        elif self.user["role"] == "android":
            group = "director-sw-eng@keypr.com"

        elif self.user["role"] == "qa":
            group = "qa-manager@keypr.com"

        elif self.user["role"] == "hardware":
            group = "hw-manager@keypr.com"

        elif self.user["role"] == "fs":
            group = "fs-manager@keypr.com"

        elif self.user["role"] == "cs":
            group = "cs-manager@keypr.com"

        elif self.user["role"] == "sales":
            group = "ex-sales@keypr.com"

        request = self.groupservice.groups().aliases().insert(groupKey=group, body=userinfo)
        response = request.execute()

        print("Gmail: %s added as alias to %s group" % (self.user["email"], group))

    # search groups for a list of ID's
    def searchgroups(self):

        request = self.groupservice.groups().list(domain = "keypr.com")
        response = request.execute()

        pprint(response)

    def searchemail(self):
    
        request = self.groupservice.users().list(domain="keypr.com", showDeleted = True)
        response = request.execute()

        pprint(response)

def main(action):

    account = new_account()

    # on-boarding
    if action.lower() == "create":

        # create email account
        account.mkemail()
        time.sleep(3)

        # set groups
        account.setgroups()
        time.sleep(3)

        # send email notifications
        account.sendemail("welcome")
        time.sleep(5)

        account.sendemail("calendar")
        time.sleep(5)

        account.sendemail("slack")
        time.sleep(5)

    # off-boarding
    else:

        # remove user from all groups
        account.deletegroups()
        time.sleep(3)

        # change email to .old
        account.mvemail()
        time.sleep(3)

        # remove old keypr.com email from email alias
        account.rmemailalias()
        time.sleep(3)

        # create alias on manager group
        account.mkalias()

if __name__ == "__main__":

    action = sys.argv[1]  
    main(action)
