#!/usr/bin/env python
# automate onboard / offboarding based off google doc

import gspread
import secret_server as ss
import gmail
import random
import string
from subprocess import call
from oauth2client.service_account import ServiceAccountCredentials
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
def get_new_users():

    # open spreadsheet
    sheet = client.open("Employee Spreadsheet").sheet1
 
    # get all lines
    listOfUsers = sheet.get_all_records()

    return listOfUsers

class new_user:

    def __init__(self, user):

        #Set values
        self.firstName = user['First Name']
        self.lastName = user['Last Name']
        self.fullName = ("%s %s" % (self.firstName, self.lastName))
        self.personalEmail = user['Email']
        self.userName = ("%s%s" % (self.firstName[0].lower(), self.lastName.lower()))
        self.keyprEmail = ("%s@keypr.com" % (self.userName))
        self.phone = user['Phone']
        self.startDate = user['Start Date']
        self.accessDate = user['KEYPR System Access Date']
        self.department = user['Department']
        self.role = user['Role']
        self.contractor = user['Contractor [T/F]']
        self.kyiv = user['Kyiv [T/F]']
        self.unixId = user['Unix ID']

        pwdSize = 14
        chars = string.letters + string.digits + string.punctuation
        self.password = ''.join((random.choice(chars)) for x in range(pwdSize))


    def secret_server(self, action):

        ss.main(action, self.firstName, self.lastName, self.personalEmail, self.password)

    def gmail(self, action):

        gmail.main(action, self.firstName, self.lastName, self.fullName, self.keyprEmail, self.personalEmail, self.password, self.role, self.contractor, self.kyiv)

    def jumpcloud(self, action):
        
        print("%s %s %s %s %s %s %s %s %s %s" % (type(self.firstName), type(self.lastName), type(self.keyprEmail), type(self.personalEmail), type(self.userName), type(self.password), type(self.unixId), type(self.role), type(self.contractor), type(self.kyiv)))
        #call(['bash', 'jumpcloud.sh', self.firstName, self.lastName, self.keyprEmail, self.personalEmail, self.userName, self.password, '2015', self.role, self.contractor, self.unixId, action])
        call(['bash', 'jumpcloud.sh', self.firstName, self.lastName, self.keyprEmail, self.personalEmail, self.userName, 'keypr!20301', str(self.unixId), self.role, self.contractor.lower(), action])

def main():

    users = get_new_users()

    for user in users:

        onboarding = new_user(user)

        #onboarding.secret_server('create')
        #onboarding.gmail('create')
        onboarding.jumpcloud('create')


if __name__ == "__main__":
    main()
