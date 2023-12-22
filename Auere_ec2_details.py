import boto3
import sys
import time

def get_tag(tags,key):
    if not tags: return ''
    for tag in tags:
        if tag['Key'] == key:
            v_str = tag['Value']
            return v_str.replace(" ", "")

    return ''

session=boto3.Session(profile_name="keyan", region_name="us-east-1") #boto3 session, aws profile

ec2_resource=session.resource(service_name="ec2") # resource object method

print("Instance ID             Instance Name            Instance IP      Instance type       Instance Lifecycle     Schedule      Owner     Project     Product family       client")
for instance in ec2_resource.instances.all():
    instance_name = get_tag(instance.tags,'Name')
    instance_owner = get_tag(instance.tags,'Owner')
    instance_schedule = get_tag(instance.tags,'Schedule')
    instance_project = get_tag(instance.tags,'Project')
    instance_family = get_tag(instance.tags, 'productFamily')
    instance_client = get_tag(instance.tags, 'customerName')

    print(instance.id + ',' + instance_name + ',' + instance.private_ip_address + ',' + instance.instance_type + ','
          + str(instance.instance_lifecycle or '') + ',' +  instance_schedule + ','+ instance_owner + ',' +instance_project
          + ',' + instance_family + ',' + instance_client )
