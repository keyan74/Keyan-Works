import boto3
from datetime import datetime, timedelta

# AWS credentials and region
aws_profile = 'skyvera'
aws_region = 'us-east-1'

# Initialize Boto3 CloudWatch client
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
cloudwatch = session.client('cloudwatch')

# Specify EC2 instance ID and metric name
instance_id = 'i-00896b4dde86ef071'
metric_name = 'CPUUtilization'

# Specify the time range for the metric data
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=1)

# Get EC2 metric data
response = cloudwatch.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'm1',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/EC2',
                    'MetricName': metric_name,
                    'Dimensions': [{'Name': 'InstanceId', 'Value': instance_id}],
                },
                'Period': 300,  # The granularity, in seconds, of the returned data points (300 seconds = 5 minutes)
                'Stat': 'Average',
            },
            'ReturnData': True,
        },
    ],
    StartTime=start_time,
    EndTime=end_time,
)

# Print the metric data
print("Timestamp\t\t\tValue")
for idx, timestamp in enumerate(response['MetricDataResults'][0]['Timestamps']):
    value = response['MetricDataResults'][0]['Values'][idx]
    print(f"{timestamp}\t{value}")
