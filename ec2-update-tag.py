import boto3
dev = boto3.Session(profile_name="skyvera", region_name="us-east-1")

client = dev.client('ec2', region_name='us-east-1')
response = client.create_tags(
    Resources=[
'i-0ce4ad83e4407f7cf',
'i-00f73ab9e21ca731a',

    ],
    Tags=[
        {
            'Key': 'Owner',
            'Value': 'nirmalkumar@devfactory.local'

        },
    ]
)