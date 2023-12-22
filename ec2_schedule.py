import boto3

from oauth2client.service_account import ServiceAccountCredentials

dev = boto3.Session(profile_name="skyvera", region_name="us-east-1")

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


ec2_detail()
print(ins_dict)

