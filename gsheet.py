import json
import pandas as pd
import pickle
import os.path
from oauth2client.service_account  import ServiceAccountCredentials
from googleapiclient.discovery import build

filename = 'credentials.json'
SCOPES =['https://www.googleapis.com/auth/spreadsheets','https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = '1C6oDP5kA_cc6bYBTEkI2BKtPxGgzMCHg8HepDIh2fzk'
DATA_TO_PULL = 'Instances'
#SPREADSHEET_ID = 'https://docs.google.com/spreadsheets/d/1C6oDP5kA_cc6bYBTEkI2BKtPxGgzMCHg8HepDIh2fzk/edit#gid=0'
def gsheet_api_check(SCOPES):
  creds = None
  print(os.path)
  if os.path.getsize(SPREADSHEET_ID) > 0:
     if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
     if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:

            #flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds  = ServiceAccountCredentials.from_json_keyfile_name(filename=filename, scopes=SCOPES)
            #creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
  else:
       print('data not found')
  return creds


creds = gsheet_api_check(SCOPES)
print('test')
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=DATA_TO_PULL).execute()
values = result.get('values', [])

if not values:
     print('No data found.')
else:
     rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                               range=DATA_TO_PULL).execute()
     data = rows.get('values')
     print("COMPLETE: Data copied")

#df = pd.DataFrame(data[1:], columns=data[0])
