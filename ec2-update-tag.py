import boto3
dev = boto3.Session(profile_name="keyan", region_name="us-east-1")

client = dev.client('ec2', region_name='us-east-1')
response = client.create_tags(
    Resources=[
'i-0xcccxxxxcf',
'i-cdzzzzxdd33',

    ],
    Tags=[
        {
            'Key': 'Owner',
            'Value': 'XXXXxX@XX.com'

        },
    ]
)
