import boto3
session = boto3.Session(profile_name="skyvera", region_name="us-east-1")
ec2_resource = session.resource(service_name="ec2")

unattached_volumes = ec2_resource.volumes.filter(
    Filters=[{'Name': 'status', 'Values': ['available']}]
)

for volume in unattached_volumes:
  print(f"Unattached volume ID: {volume.id}")
