Credentials:
    Get credentials file from Chris (ckoh@keypr.com)
    Store file in new_user/scripts

On-boarding (new_user.sh) - Setting up a new user will do the following
    1. Create a new randomly generated password, store the password in SecretServer
    2. Create a gmail account using first_initial+last_name@keypr.com
    3. Join groups which are assoicated by the users team
    4. Send slack, staff calendar and welcome emails
    5. Create users JumpCloud account
    6. Create users Jira/Confluence account
    7. Assign user to the internal-dev group

    Usage: ./new_user.sh [First Name] [Last Name] [Personal Email] [Role] [Contractor?] [Kyiv?] [Unix ID] [Jira Ticket Number]
        Possible roles: staff, ops, dev, ios, android, qa, hardware, fs, cs, sales, contractor
        Finding Unix ID: https://github.com/Keypr/cloudkeypr/blob/master/jc-ldap-check.sh

Off-boarding (rm_user.sh) - Removing a user will do the following
    1. Create a new randomly generated password, store the password in SecretServer
    2. Change gmail password
    3. Change gmail account: username@keypr.com -> username.old@keypr.com
    5. Add username@keypr.com as an alias to team manager group
    6. Remove account from all gmail groups
    7. Change JumpCloud password & email address
    8. Remove JumpCloud user tags
    9. Change Jira/Confluence password & email address
    10. Remove from Jira/Confluence groups 

    Usage: ./rm_user.sh ./rm_user.sh [First Name] [Last Name] [Role]
        Possible roles: staff, ops, dev, ios, android, qa, hardware, fs, cs, sales, contractor

Off-boarding non-conventional emails (rm_user_old.sh) - Use this when a user's email does not follow the first_initial+last_name@keypr.com naming convention.  Will act the same as rm_user.sh.

    Usage: ./rm_user_old.sh [First Name] [Last Name] [Email] [Role]
        Possible roles: staff, ops, dev, ios, android, qa, hardware, fs, cs, sales, contractor


TODO:
