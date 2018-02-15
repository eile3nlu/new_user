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
    def mkemail(self, fName, lName, email, password):

        userinfo = {
                    "primaryEmail": email,
                    "name": {
                                "givenName": fName,
                                "familyName": lName 
                            },
                    "password": password 
                    }

        request = self.userservice.users().insert(body=userinfo)
        response = request.execute()

        print("Gmail: Account created - %s" % email)

    # add users to groups
    def setgroups(self, role, contractor, kyiv, email):
    
        # team mailing groups
        if role.lower() == "staff":
            # staff@keypr.com
            print("Gmail: Groups added - ")
            groups = []

        elif role.lower() == "dev":
            #  dev@keypr.com
            print("Gmail: Groups added - dev@keypr.com")
            groups = ["03as4poj18f1ku8"]

        elif role.lower() == "ops":
            # bridge-ops@keypr.com, dev@keypr.com, kcs-alerts@keypr.com, ops@keypr.com, security@keypr.com, service-status@keypr.com, build@keypr.com
            print("Gmail: Groups added - bridge-ops@keypr.com, dev@keypr.com, kcs-alerts@keypr.com, ops@keypr.com, security@keypr.com, service-status@keypr.com, build@keypr.com")
            groups = ["00pkwqa10t6184d", "03as4poj18f1ku8", "01baon6m2p11k2p", "00tyjcwt0jo3gxm", "00ihv6361eix8zb", "035nkun23dv4k8i", "03x8tuzt0lobslp"]

        elif role.lower() == "ios":
            # dev@keypr.com, ios-dev@keypr.com
            print("Gmail: Groups added - dev@keypr.com, ios-dev@keypr.com")
            groups = ["03as4poj18f1ku8", "03oy7u292fyscdg"]
        
        elif role.lower() == "android":
            # dev@keypr.com, android-dev@keypr.com
            print("Gmail: Groups added - dev@keypr.com, android-dev@keypr.com")
            groups = ["03as4poj18f1ku8", "02fk6b3p49a7k54"]

        elif role.lower() == "qa":
            # dev@keypr.com, qateam@keypr.com, testeng@keypr.com
            print("Gmail: Groups added - dev@keypr.com, qateam@keypr.com, testeng@keypr.com")
            groups = ["03as4poj18f1ku8", "00pkwqa130iy7m3", "030j0zll28x34h6"]

        elif role.lower() == "hardware":
            # dev@keypr.com, kilt@keypr.com
            print("Gmail: Groups added - dev@keypr.com, kilt@keypr.com")
            groups = ["03as4poj18f1ku8", "02bn6wsx190y7ep"]

        elif role.lower() == "fs":
            # fieldservices@keypr.com, support@keypr.com, supportafterhours@keypr.com, updates@keypr.com
            print("Gmail: Groups added - fieldservices@keypr.com, support@keypr.com, supportafterhours@keypr.com, updates@keypr.com")
            groups = ["01y810tw3w17osf", "02s8eyo146al189", "04f1mdlm3pinoxb", "0111kx3o0iyeqei"]

        elif role.lower() == "cs":
            print("Gmail: Groups added - ")
            groups = []

        elif role.lower() == "sales":
            # sales@keypr.com
            print("Gmail: Groups added - sales@keypr.com")
            groups = ["04d34og824t1ihr"]
    
        # "Group" mailing groups
        if contractor.lower() == "t":
            # external@keypr.com    
            print("Gmail: Groups added - external@keypr.com")
            groups.append("03ygebqi16xg5kj")

        else:

            if kyiv.lower() == "t":
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
                    "email": email,
                    "role": "MEMBER"
                    }

        for group in groups:
            request = self.groupservice.members().insert(body=userinfo, groupKey=group)
            response = request.execute()

    def sendemail(self, TYPE, fullName, email, password, emailPersonal, contractor):

        # Set message body
        # Set receipent based on message type
        if TYPE == "welcome":

            message = MIMEText((self.template[TYPE]["message"] % (fullName, email, password, email)), "html")
            message["to"] = emailPersonal 

            #override staff welcome with contractor welcome for contractors
            if contractor.lower() == "t":
                TYPE = 'welcome_contractor'

        elif TYPE in ['reviewforms', 'prereview21', 'prereview14', 'reviewday', 'postreview15', 'postreview30']:

            message = MIMEText(self.template[TYPE]["message"], "html")
            # Supervisor email address is passed through as password
            message["to"] = password 

        # If message is not routed to Personal or Supervisor email, then send to KEYPR email
        else:
            message = MIMEText(self.template[TYPE]["message"], "html")
            message["to"] = email 

        # set from, subject and encoding
        message["from"] = self.email_sender 
        message["subject"] = self.template[TYPE]["title"]
        message_text =  {"raw": base64.urlsafe_b64encode(message.as_string())}

        # only send welcome to contractors
        if contractor.lower() == "t":
            if TYPE == "welcome_contractor":
                send_message = (self.mailservice.users().messages().send(userId="me", body=message_text).execute())
                print("Gmail: Email sent - %s" % TYPE)
        else:
            send_message = (self.mailservice.users().messages().send(userId="me", body=message_text).execute())
            print("Gmail: Email sent - %s" % TYPE)

    ### OFF BOARDING ###

    def deletegroups(self, keyprEmail):

        request = self.groupservice.groups().list(userKey=keyprEmail)
        response = request.execute()

        groupids = []
        groups = []

        for groupid in response["groups"]:
            groupids.append(groupid["id"]) 
            groups.append(groupid["name"])

        for group in groupids:
            request = self.groupservice.members().delete(memberKey=keyprEmail, groupKey=group)
            response = request.execute()

        print("Gmail: %s removed from %s groups" % (keyprEmail, groups))

    def mvemail(self, keyprEmail, personalEmail, password):
        print(personalEmail)

        userinfo = {
                    "primaryEmail": personalEmail,
                    "password": password 
                    }

        request = self.userservice.users().update(userKey=keyprEmail, body=userinfo)
        response = request.execute()

        print("Gmail: Changed %s -> %s" % (keyprEmail, personalEmail))

    def rmemailalias(self, keyprEmail, personalEmail):

        request = self.aliasservice.users().aliases().delete(alias=keyprEmail, userKey=personalEmail)
        response = request.execute()

        print("Gmail: Alias %s removed from %s" % (keyprEmail, personalEmail))

    def mkalias(self, keyprEmail, role):

        userinfo = {
                    "alias": keyprEmail 
                    }

        if role == "staff":
            group = ""

        elif role == "ops":
            group = "ops-manager@keypr.com"

        elif role == "dev":
            group = "director-sw-eng@keypr.com"

        elif role == "ios":
            group = "director-sw-eng@keypr.com"

        elif role == "android":
            group = "director-sw-eng@keypr.com"

        elif role == "qa":
            group = "qa-manager@keypr.com"

        elif role == "hardware":
            group = "hw-manager@keypr.com"

        elif role == "fs":
            group = "fs-manager@keypr.com"

        elif role == "cs":
            group = "cs-manager@keypr.com"

        elif role == "sales":
            group = "ex-sales@keypr.com"

        request = self.groupservice.groups().aliases().insert(groupKey=group, body=userinfo)
        response = request.execute()

        print("Gmail: %s added as alias to %s group" % (keyprEmail, group))

    # search groups for a list of ID's
    def searchgroups(self):

        request = self.groupservice.groups().list(domain = "keypr.com")
        response = request.execute()

        pprint(response)

    def searchemail(self):
    
        request = self.groupservice.users().list(domain="keypr.com", showDeleted = True)
        response = request.execute()

        pprint(response)

def main(action, firstName, lastName, fullName, keyprEmail, personalEmail, password, role, contractor, kyiv):

    account = new_account()

    # on-boarding
    if action.lower() == "create":

        # create email account
        account.mkemail(firstName, lastName, keyprEmail, password)
        time.sleep(3)

        # set groups
        account.setgroups(role, contractor, kyiv, keyprEmail)
        time.sleep(3)

        # send email notifications
        account.sendemail("welcome", fullName, keyprEmail, password, personalEmail, contractor)
        time.sleep(5)

        account.sendemail("calendar", fullName, keyprEmail, password, personalEmail, contractor)
        time.sleep(5)

        account.sendemail("slack", fullName, keyprEmail, password, personalEmail, contractor)
        time.sleep(5)

    # off-boarding
    elif action.lower() == 'delete':

        # remove user from all groups
        account.deletegroups(keyprEmail)
        time.sleep(3)

        # change email to .old
        # personalEmail = firstInitial + lastName + ".old@keypr.com"
        # ex. ckoh.old@keypr.com
        account.mvemail(keyprEmail, personalEmail, password)
        time.sleep(3)

        # remove old keypr.com email from email alias
        account.rmemailalias(keyprEmail, personalEmail)
        time.sleep(3)

        # create alias on manager group
        account.mkalias(keyprEmail, role)

    elif action.lower() in ['reviewforms', 'prereview21', 'prereview14', 'reviewday', 'postreview15', 'postreview30']:
        account.sendemail(action, fullName, keyprEmail, password, personalEmail, contractor)

if __name__ == "__main__":

    action = sys.argv[1]  
    main(action)
