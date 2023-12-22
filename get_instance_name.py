import boto3

# AWS credentials and region
aws_profile = 'keyan'
aws_region = 'us-east-1'

# Initialize Boto3 EC2 client
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
ec2_client = session.client('ec2')

# List of instance IDs for which you want to retrieve instance names
instance_ids_to_query = ['i-098sdesd002033030',
                        ] 
# Replace with your instance IDs

# Get instance details
response = ec2_client.describe_instances(InstanceIds=instance_ids_to_query)

# Extract and print instance names
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        instance_name = ''

        # Get the instance name from tags
        for tag in instance.get('Tags', []):
            if tag['Key'].lower() == 'name':
                instance_name = tag['Value']
                break

        print(f"Instance ID: {instance_id}, Instance Name: {instance_name or 'N/A'}")
