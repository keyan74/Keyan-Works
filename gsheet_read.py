import gspread
from oauth2client.service_account import ServiceAccountCredentials
import boto3

dev = boto3.Session(profile_name="keyan")

client = dev.client('ec2', region_name='us-east-1')

ins_dict = {}


def ec2_detail():
    '''Get all ec2 instance details and give the instance_id and tag value of Schedule'''

    page_iterator = client.get_paginator('describe_instances').paginate()
    for page in page_iterator:

        Instances = page['Reservations']

        for ins in Instances:
            for i in ins['Instances']:
                ins_id = i['InstanceId']
                tag = i.get('Tags', [])

                for tg in tag:
                    if tg['Key'] == 'Schedule':  # if there is a tag matches the key Schedule
                        ins_tag = tg['Value']
                        ins_dict.update({ins_id: ins_tag})
                    elif ins_id not in ins_dict.keys():
                        ins_tag = 'n/a'  # add a tag value if there is not tag named as Schedule
                        ins_dict.update({ins_id: ins_tag})

    return (ins_dict)


'''ec2_data = ec2_detail()'''

def gsheet_api():
    '''Fetch info from google sheet and gets the instance_id and tag value'''

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    gsheet_data = gspread.authorize(creds)
    sheet = gsheet_data.open_by_key("1-IcT6bpA9Udmi46CVBjoKFdz50172r4X4RFSOswAkl8").sheet1  # Open the spreadhseet
    instance_id = sheet.col_values(3)  # from 3rd column
    schedule = sheet.col_values(4)  # from 4th column
    ins_schedule = list(zip(instance_id, schedule))

    return ins_schedule


'''gsheet_info = gsheet_api()'''

ec2_data = ec2_detail()

gsheet_info = gsheet_api()
for ins_no, ins_tag in gsheet_info:
        print(ins_no)
        print(ec2_data.keys())
        if ins_no in ec2_data.keys():
            ex_tag = ec2_data[ins_no]
            print(ins_tag.strip())
            print(ex_tag.strip())
            if ins_tag.strip() == ex_tag.strip():  # match tags
                a = 'hi'  # to by pass the condition
            else:
                tag_edit = client.create_tags(Resources=[
                    ins_no, ],
                    Tags=[
                        {
                            'Key': 'Schedule',
                            'Value': ins_tag,
                        },
                    ], )


