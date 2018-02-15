#!/usr/bin/env python
# automate onboard / offboarding based off google doc

import gspread
import secret_server as ss
import confluence
import gmail
import random
import string
from datetime import datetime
from dateutil.relativedelta import relativedelta
from subprocess import call
from oauth2client.service_account import ServiceAccountCredentials
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
def get_users(spreadsheet, userType):

    # open spreadsheets
    if userType == 'onboarding':
        onboarding = spreadsheet.get_worksheet(0)

    elif userType == 'review':
        onboarding = spreadsheet.get_worksheet(1)

    elif userType == 'departments':
        onboarding = spreadsheet.get_worksheet(3)

    # count number of lines
    numLines = onboarding.row_count

    # get all data from on-boaridng list 
    listOfUsers = onboarding.get_all_records()

    return listOfUsers

class review_user:

    def __init__(self, user, departments, spreadsheet):

        print(user)
        print('---------- Review Process ----------')
        

        # set employee values
        self.firstName = user['First Name']
        self.lastName = user['Last Name']
        self.fullName = ("%s %s" % (self.firstName, self.lastName))
        self.personalEmail = user['Personal Email']
        self.keyprEmail = user['Keypr Email']
        self.phone = user['Phone']
        self.status = user['Status']
        self.hireDate = user['Start Date']
        self.department = user['Department']
        self.role = user['Role']
        self.contractor = user['Contractor']
        self.kyiv = user['Kyiv']

        # set supervisor values
        for department in departments:
            if self.department == department['Department']:
                self.supervisorName = department['Department Head']
                self.supervisorEmail = department['Contact Email']

        # configure current year review date based on year hired 
        self.today = datetime.now()
        self.startDate = datetime.strptime(self.hireDate, "%m/%d/%Y")
        yearDelta = self.today.year - self.startDate.year
        reviewDate = self.startDate + relativedelta(years =+ yearDelta)

        # get date difference between today and review day
        self.dateDiff = (reviewDate - self.today).days

    # send review emails based on dates
    def send_review(self, action):

        print(self.dateDiff)

        # -30: forms go out
        # -21: Reminder to manager to complete manager review form
        # -14: Reminder to managers to send completed employee and manager review forms to HR inbox
        # 0: 2 Emails, Reminder to manger to schedule 1 on 1.  

        # Skip sending review process emails if employee's hire date was this year
        if self.today.year != self.startDate.year:

            # 30 - Day Review Form Distribution 
            if self.dateDiff == 29:

                gmail.main('reviewforms', '', '', self.fullName, self.keyprEmail, self.personalEmail, self.supervisorEmail, self.role, self.contractor, self.kyiv)
    
            # 21 - Day Pre-Review Notice
            elif self.dateDiff == 20:

                gmail.main('prereview21', '', '', self.fullName, self.keyprEmail, self.personalEmail, self.supervisorEmail, self.role, self.contractor, self.kyiv)

            # 14 - Day Pre-Review Notice
            elif self.dateDiff == 13:

                gmail.main('prereview14', '', '', self.fullName, self.keyprEmail, self.personalEmail, self.supervisorEmail, self.role, self.contractor, self.kyiv)

            # Review Day Notice
            elif self.dateDiff == -1: 

                gmail.main('reviewday', '', '', self.fullName, self.keyprEmail, self.personalEmail, self.supervisorEmail, self.role, self.contractor, self.kyiv)

            # 15 Day Post-Review
            elif self.dateDiff == -16:

                gmail.main('postreview15', '', '', self.fullName, self.keyprEmail, self.personalEmail, self.supervisorEmail, self.role, self.contractor, self.kyiv)
        
            # 30 Day Post-Review
            elif self.dateDiff == -31:

                gmail.main('postreview30', '', '', self.fullName, self.keyprEmail, self.personalEmail, self.supervisorEmail, self.role, self.contractor, self.kyiv)

        else:
        
            print("%s onboarded this year (%s) skipping review emails" % (self.fullName, self.startDate))

class new_user:

    def __init__(self, user, spreadsheet):

        print(user)

        #Set values
        self.firstName = user['First Name']
        self.lastName = user['Last Name']
        self.fullName = ("%s %s" % (self.firstName, self.lastName))
        self.personalEmail = user['Personal Email']
        self.userName = ("%s%s" % (self.firstName[0].lower(), self.lastName.lower()))
        self.keyprEmail = ("%s@keypr.com" % (self.userName))
        self.phone = user['Phone']
        self.startDate = user['Start Date']
        self.accessDate = user['KEYPR System Access Date']
        self.department = user['Department']
        self.role = user['Role']
        try:
            self.contractor = user['Contractor [T/F]']
            self.kyiv = user['Kyiv [T/F]']
            self.unixId = user['Unix ID']
        except:
            print("Offboarding no contractor / id / kyiv")
            self.contractor = '' 
            self.kyiv = '' 
            self.unixId = '' 

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

        #ss.main(action, self.firstName, self.lastName, self.personalEmail, self.password)
        self.auditSheet.update_cell(2, 6, 'X')

        if action == 'create':
            print('---------- Onboarding ----------')
        else:
            print('---------- Offboarding ----------')
        
        print('Secret Created')

    # Create KEYPR gmail account, add to groups based on department, send notification emails
    def gmail(self, action):

        if action == 'create':
            #gmail.main(action, self.firstName, self.lastName, self.fullName, self.keyprEmail, self.personalEmail, self.password, self.role, self.contractor, self.kyiv)
            self.auditSheet.update_cell(2, 7, 'X')
            self.auditSheet.update_cell(2, 10, 'X')
            self.auditSheet.update_cell(2, 11, 'X')
            self.auditSheet.update_cell(2, 12, 'X')
            print('Gmail Account Created')
            print('Gmail Groups Set')
            print('Welcomie Email sent')
        else:
            self.personalEmail = ("%s.old@keypr.com" % (self.userName))
            #gmail.main(action, self.firstName, self.lastName, self.fullName, self.keyprEmail, self.personalEmail, self.password, self.role, self.contractor, self.kyiv)
        
    # Create jumpcloud user
    def jumpcloud(self, action):
        
        #call(['bash', 'jumpcloud.sh', self.firstName, self.lastName, self.keyprEmail, self.personalEmail, self.userName, self.password, str(self.unixId), self.role, self.contractor.lower(), action])
        self.auditSheet.update_cell(2, 8, 'X')

        print('Jumpcloud user created')

    # Create confluence user
    def confluence(self, action): 

        #confluence.main(action, self.fullName, self.password, self.contractor, self.keyprEmail)
        self.auditSheet.update_cell(2, 9, 'X')

        print('Jira user created')

    # Add new hire to the active employee list
    def employee_list_add(self):

        self.employeeSheet.insert_row([self.fullName, self.personalEmail, self.keyprEmail, self.phone, 'Active', self.startDate, self.department, self.role, self.contractor, self.kyiv], 2)
        print('Added to active employee list')

    # remove new hire from the onboarding list
    def remove_from_onboarding(self):
   
            
        self.onboardingSheet.delete_row(2)
        self.onboardingSheet.insert_row([], 2)
        print('Removed from onboarding')


def main():

    # Open onboarding spreadsheet
    onboardingSpreadsheet = client.open("Employee Spreadsheet")

    # get onboarding page of onboarding spreadsheet
    users = get_users(onboardingSpreadsheet, 'onboarding')

    # Onboarding
    # based on the list of users on the On-boarding tab

    ## Ask for input "Do you want to process a new user? (Y/N)
    new_user=input('Do you want to process a new user? (Y/N) ')
    
    ## If Y || y: do actions from line 247 - 259. Else pass
    if new_user.lower()=='y':
       for user in users:

        onboarding = new_user(user, onboardingSpreadsheet)

        # Create accounts and set access
        onboarding.secret_server('create')
        onboarding.gmail('create')
        onboarding.jumpcloud('create')
        onboarding.confluence('create')

        # add user to employee list and remove from onboarding sheet
        onboarding.employee_list_add()
        #onboarding.remove_from_onboarding() 
    else:
        pass    

    # Review Emails / Off-boarding
    # get Active Employee list and department spreadsheets
    users = get_users(onboardingSpreadsheet, 'review')
    departments = get_users(onboardingSpreadsheet, 'departments')

    # Analyze all active employees, send annual review emails based on how close to review day they are
    for user in users:

        # Review Emails
        review = review_user(user, departments, onboardingSpreadsheet)
        review.send_review('review')
        
        # Off-boarding
        if user["Status"] == "Inactive":
            offboarding = new_user(user, onboardingSpreadsheet)
            #offboarding.secret_server('delete')
            #offboarding.gmail('delete')
            onboarding.jumpcloud('delete')
        
    

if __name__ == "__main__":
    main()
