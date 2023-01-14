import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from sys import argv

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]


month = argv[1] #a string, full month name, all lowercase
year = argv[2] #an integer

file = '/Users/Owner/Documents/Transaction_Tracker/'+ str(year) + '/rbc_' + month + '_' + str(year) + '.csv'

transactions = []

# categorizes each transaction and extracts the account type, date, name/description, category, and amount of each transaction. 
def rbc_fin(file): 
    with open(file, mode = 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        categories_dict = {
            'PLAYSTATIONNETWORK 877-971-7669 CA': 'Playstation Purchases',
            'Spotify P1F9839D9F Stockholm': 'Spotify Subscription',
            'INVESTMENT' : "TFSA Contribution",
            'Email Trfs' : 'E-Transfer',
            'PRESTO AUTL TORONTO ON' : 'Presto Card Autoload', 
            'PUBLIC MOBILE 855-4782542 BC': 'Phone Bill',
            'Transfer' : 'Credit Card Payment',
            'MISC PAYMENT' : 'Credit Card Payment',
            'PAYMENT - THANK YOU / PAIEMENT - MERCI' : 'Credit Card Payment'


        }

        sum = 0

        for row in csv_reader:

            if row[6] == 'CAD$' or row[6] == 'USD$':
                continue
            account = row[0]
            date = row[2]
            name = row[4]
            amount = float(row[6])
            sum += amount

            if row[4] in categories_dict:
                category = categories_dict[row[4]]
            else:
                category = 'Other'
            
            transaction = ((account, date, name, category, amount))
            print (transaction)
            transactions.append(transaction)
        return transactions


credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scopes) #access the PRIVATE json key you downloaded earlier 
sa = gspread.authorize(credentials) # authenticate the JSON key with gspread
sh = sa.open("Personal Finances - " + str(year)) #open sheet

wks = sh.worksheet(f"{month}")

rows = rbc_fin(file)

# prints each transaction in the google sheet
for row in rows:
    wks.insert_row([row[0], row[1], row[2], row[3], row[4] ], 8)
    time.sleep(2)

