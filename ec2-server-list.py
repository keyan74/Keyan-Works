import boto3
dev = boto3.Session(profile_name="keyan", region_name="us-east-1")
def list_ec2_instances():
    ec2 = dev.resource('ec2')

    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running', 'stopped']}]
    )

    for instance in instances:
        print(instance.id, instance.instance_type, instance.state['Name'])

if __name__ == "__main__":
    list_ec2_instances()
