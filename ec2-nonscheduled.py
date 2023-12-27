import boto3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gchat import sent_gchat_message
import pandas as pd

dev = boto3.Session(profile_name="keyan")

client = dev.client('ec2', region_name='us-east-1')

ins_dict = []
inst_not_found = []
gsheet_not_found = []
ec2_not_scheduled = []

def ec2_detail():
    '''Get all ec2 instance details and give the instance_id and tag value of Schedule'''

    page_iterator = client.get_paginator('describe_instances').paginate()
    for page in page_iterator:

        Instances = page['Reservations']

        for ins in Instances:
            for i in ins['Instances']:
                ins_id = i['InstanceId']
                ins_dict.append(ins_id)

    return (ins_dict)

def gsheet_api():
    '''Fetch info from google sheet and gets the instance_id and tag value'''

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    gsheet_data = gspread.authorize(creds)
    sheet = gsheet_data.open_by_key("1-IcT6bpA9Udmi46CVBjoKFdz50172r4X4RFSOswAkl8").sheet1  # Open the spreadhseet
    instance_id = sheet.col_values(3)  # from 3rd column
    ins_schedule = list(instance_id)

    # The below part to find any duplicate instance in google sheet
    df = pd.DataFrame({'instance id': ins_schedule})
    duplicate_values = df[df.duplicated('instance id', keep=False)]
    column_name = 'instance_id'
    if not duplicate_values.empty:
        print(f'Duplicate values in column "{column_name}":')
        print(duplicate_values)
    return (ins_schedule)

def get_not_scheduled_instance():
   ec2_data = ec2_detail()
   gsheet_info = gsheet_api()
   for ec2_inst in ec2_data:
      if ec2_inst in gsheet_info:
         v_skip = 0
      else:
        inst_not_found.append(ec2_inst)

   return(inst_not_found)

def remove_terminated_instance_gsheet():
   ec2_data = ec2_detail()
   gsheet_info = gsheet_api()
   for gct_inst in gsheet_info:
      if gct_inst in ec2_data:
         v_skip = 0
      else:
        gsheet_not_found.append(gct_inst )

   return(gsheet_not_found)

ec2_not_scheduled = get_not_scheduled_instance()
del_inst_details_from_gsheet = remove_terminated_instance_gsheet()

sent_gchat_message(ec2_not_scheduled)

print("Instance Not Scheduled")
for x in  ec2_not_scheduled:
    print(x)


print("Instance remove from Scheduler ")
for x in  del_inst_details_from_gsheet:
    print(x)
