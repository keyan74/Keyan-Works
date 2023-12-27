import boto3

# Set your AWS credentials and region

# Create an EC2 client
dev = boto3.Session(profile_name="keyan")
ec2_client = dev.client('ec2', region_name='us-east-1')

# Get all EBS volumes
response = ec2_client.describe_volumes()

# Iterate through each volume and print details
for volume in response['Volumes']:
    volume_id = volume['VolumeId']
    volume_name = next((tag['Value'] for tag in volume.get('Tags', []) if tag['Key'] == 'Name'), 'N/A')
    volume_type = volume['VolumeType']
    volume_size = volume['Size']

    # Get attached instance details
    attached_instance_id = next((attachment['InstanceId'] for attachment in volume['Attachments']), None)
    attached_instance_name = 'N/A'

    if attached_instance_id:
        instance_response = ec2_client.describe_instances(InstanceIds=[attached_instance_id])
        instance_name = next((tag['Value'] for tag in instance_response['Reservations'][0]['Instances'][0].get('Tags', []) if tag['Key'] == 'Name'), 'N/A')
        attached_instance_name = instance_name

    print(volume_id + ',' + volume_name + ',' + volume_type + ',' + str(volume_size) + 'GB'+ ' ,' + attached_instance_name)

    # Print or use the details as needed

