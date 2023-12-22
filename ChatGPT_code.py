import boto3
import csv

# AWS credentials and region
aws_profile = 'skyvera'
aws_region = 'us-east-1'

# Initialize Boto3 EC2 client
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
ec2_client = session.client('ec2')

# Get EC2 instances
response = ec2_client.describe_instances()
instances = []

# Extract relevant information
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        instance_name = ''
        instance_type = instance['InstanceType']
        private_ip = instance.get('PrivateIpAddress', 'N/A')

        # Get the instance name from tags
        for tag in instance.get('Tags', []):
            if tag['Key'].lower() == 'name':
                instance_name = tag['Value']
                break

        instances.append({
            'InstanceID': instance_id,
            'InstanceName': instance_name,
            'IPAddress': private_ip,
            'InstanceType': instance_type
        })

# Write data to CSV file
csv_file_path = 'ec2_instance_details.csv'
csv_columns = ['InstanceID', 'InstanceName', 'IPAddress', 'InstanceType']

with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()
    for instance in instances:
        writer.writerow(instance)

print(f"EC2 instance details written to {csv_file_path}")
