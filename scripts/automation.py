#!/usr/bin/env python
# automate onboard / offboarding based off google doc

import gspread
import secret_server as ss
import confluence
import gmail
import random
import string
from subprocess import call
from oauth2client.service_account import ServiceAccountCredentials
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
def get_new_users(spreadsheet):

    # open spreadsheets
    onboarding = spreadsheet.get_worksheet(0)

    # count number of lines
    numLines = onboarding.row_count

    # get all data from on-boaridng list 
    listOfUsers = onboarding.get_all_records()

    return listOfUsers

class new_user:

    def __init__(self, user, spreadsheet):

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

        #audit logs
        self.auditSheet = spreadsheet.get_worksheet(4)
        self.auditData = self.auditSheet.get_all_records
        self.auditRows = self.auditSheet.row_count
        self.auditSheet.insert_row([self.fullName, self.startDate, self.accessDate, self.department, self.role], 2)

        # employee list
        self.employeeSheet = spreadsheet.get_worksheet(1)

        # onboarding
        self.onboardingSheet = spreadsheet.get_worksheet(0)

    def secret_server(self, action):

        ss.main(action, self.firstName, self.lastName, self.personalEmail, self.password)
        self.auditSheet.update_cell(2, 6, 'X')

        if action == 'create':
            print('---------- Onboarding ----------')
        else:
            print('---------- Offboarding ----------')

    def gmail(self, action):

        gmail.main(action, self.firstName, self.lastName, self.fullName, self.keyprEmail, self.personalEmail, self.password, self.role, self.contractor, self.kyiv)
        self.auditSheet.update_cell(2, 7, 'X')
        self.auditSheet.update_cell(2, 10, 'X')
        self.auditSheet.update_cell(2, 11, 'X')
        self.auditSheet.update_cell(2, 12, 'X')
        

    def jumpcloud(self, action):
        
        call(['bash', 'jumpcloud.sh', self.firstName, self.lastName, self.keyprEmail, self.personalEmail, self.userName, self.password, str(self.unixId), self.role, self.contractor.lower(), action])
        self.auditSheet.update_cell(2, 8, 'X')

    def confluence(self, action): 

        confluence.main(action, self.fullName, self.password, self.contractor, self.keyprEmail)
        self.auditSheet.update_cell(2, 9, 'X')

    def employee_list_add(self):

        self.employeeSheet.insert_row([self.fullName, self.personalEmail, self.keyprEmail, self.phone, 'Active', self.startDate, self.department, self.role], 2)

    def remove_from_onboarding(self):
   
            
        print('test') 
        self.onboardingSheet.delete_row(2)
        self.onboardingSheet.insert_row([], 2)
        print('removed')

def main():

    spreadsheet = client.open("Employee Spreadsheet")

    users = get_new_users(spreadsheet)

    for user in users:

        onboarding = new_user(user, spreadsheet)

        # onboard new user
        onboarding.secret_server('create')
        onboarding.gmail('create')
        onboarding.jumpcloud('create')
        onboarding.confluence('create')

        # add user to employee list and remove from onboarding sheet
        onboarding.employee_list_add()
        onboarding.remove_from_onboarding()

if __name__ == "__main__":
    main()
