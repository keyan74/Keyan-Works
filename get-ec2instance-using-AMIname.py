import boto3
def get_instance_id_by_ami_name(ami_name):
    # Set your AWS credentials and region

    # Create an EC2 client
    dev = boto3.Session(profile_name="keyan")

    ec2 = dev.client('ec2', region_name='us-east-1')

    try:
        # Describe images with the specified name
        response = ec2.describe_images(Filters=[{'Name': 'name', 'Values': [ami_name]}])
       # print(response)
        # Check if any images are found
        if response['Images']:
            # Get the most recent image (assuming you want the latest)
            image = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)[0]
            print(image['BlockDeviceMappings'][0])
            # Get the instance ID associated with the image
            instance_id = image['BlockDeviceMappings'][0]['Ebs']['AttachTime']

            print(f"Instance ID for AMI '{ami_name}': {instance_id}")
        else:
            print(f"No images found with the name '{ami_name}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    ami_name = 'CentOS-7-2111-20220825_1.x86_64-d9a3032a-921c-4c6d-b150-bde168105e42'
    get_instance_id_by_ami_name(ami_name)
