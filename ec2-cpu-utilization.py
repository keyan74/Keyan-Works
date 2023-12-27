import boto3

dev = boto3.Session(profile_name="keyan")

ec2_client = dev.client('ec2', region_name='us-east-1')
cloudwatch_client = dev.client('cloudwatch', region_name='us-east-1')
    # Set the threshold for CPU utilization (change as needed)
cpu_threshold_percent = 2.0

    # Describe EC2 instances
response = ec2_client.describe_instances()
instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in
                reservation['Instances']]

underutilized_instances = []

# Iterate through reservations and instance
# Iterate through instance IDs and get CPU utilization metric
for instance_id in instance_ids:
    # Get average CPU utilization for the last hour
    print(instance_id)
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime='2023-12-10T00:00:00Z',  # Replace with your desired start time
        EndTime='2023-12-11T00:00:00Z',  # Replace with your desired end time
        Period=3600,  # 1 hour intervals
        Statistics=['Average']
    )


   # Check if there are data points
if response['Datapoints']:
      average_cpu_utilization = response['Datapoints'][0]['Average']

      # Check if average CPU utilization is below the threshold
      if average_cpu_utilization < cpu_threshold_percent:
                underutilized_instances.append({
                    'InstanceId': instance_id,
                    'AverageCPUUtilization': average_cpu_utilization
                })

if underutilized_instances:
    print(f"Underutilized instances found: {underutilized_instances}")
else:
    print("No underutilized instances found.")
