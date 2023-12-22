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

session=boto3.Session(profile_name="skyvera", region_name="us-east-1") #boto3 session, aws profile

ec2_resource=session.resource(service_name="ec2") # resource object method

print("Instance ID             Instance Name            Instance IP        Owner     Project     Product family       client")
for instance in ec2_resource.instances.all():
    instance_name = get_tag(instance.tags,'Name')
    instance_owner = get_tag(instance.tags,'Owner')
    instance_project = get_tag(instance.tags,'Project')
    instance_family = get_tag(instance.tags, 'productFamily')
    instance_client = get_tag(instance.tags, 'customerName')

    print(instance.id + ',' + instance_name + ',' + instance.private_ip_address + ',' + instance_owner + ',' +instance_project
          + ',' + instance_family + ',' + instance_client )
    '''print(
            "Id: {0}\tName: {1}\tPrivate ip: {2}\n".format(
         instance.id, instance_name, instance.private_ip_address
         )
     )'''

'''session = boto3.Session(profile_name='skyvera')
s3 = session.resource('s3')

for bucket in s3.buckets.all():
   print(bucket.name)'''