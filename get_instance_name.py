import boto3

# AWS credentials and region
aws_profile = 'skyvera'
aws_region = 'us-east-1'

# Initialize Boto3 EC2 client
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
ec2_client = session.client('ec2')

# List of instance IDs for which you want to retrieve instance names
instance_ids_to_query = ['i-0bba723c853422427',
'i-02d49ece76cf265ba',
'i-038b30ed1d77a156f',
'i-004fd3cb95953cae7',
'i-021b5e47dcb2fac5b',
'i-006ff9f7fcc9acf62',
'i-09bb2983b1a7c0a67',
'i-07e4d66e4ddbfa8fa',
'i-096eea64b67a522c3',
'i-036acb7b995b7f386',
'i-0b0bc52800dbe5aae',
'i-0ddd086876b35eb09',
'i-0eade07c17be0c160',
'i-08adcfcaa481900e5',
'i-081e574e0228177ad',
'i-05d3e77815171420d',
'i-00896b4dde86ef071',
'i-0f468504d8e017cc7',
'i-091b0c398605e9f07',
'i-094e0d361e522576f',
'i-0a0dc3218e8e99370',
'i-0d43add73b3f70746',
'i-0fb8280840d7b1093',
'i-0f75e1ae03df3f19d',
'i-0d6a123b8c650e7d5',
'i-067d9c5e281338c0d',
]  # Replace with your instance IDs

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
