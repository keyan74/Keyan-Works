import boto3
import csv

def get_tag(tags, key):
    if not tags: return ''
    for tag in tags:
        if tag['Key'] == key:
            return tag['Value'].replace(" ", "")
    return ''

session = boto3.Session(profile_name="skyvera", region_name="us-east-1")
ec2_resource = session.resource(service_name="ec2")

data = []

for instance in ec2_resource.instances.all():
    instance_name = get_tag(instance.tags, 'Name')
    data.append([
        instance.id,
        instance_name,
        instance.private_ip_address,
        instance.instance_type
    ])

with open('ec2_instances.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Instance ID", "Instance Name", "IP Address", "Instance Type"])
    writer.writerows(data)