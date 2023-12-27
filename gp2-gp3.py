import boto3


def change_all_volumes_to_gp3():
    # Set your AWS credentials and region
    dev = boto3.Session(profile_name="keyan")

    ec2 = dev.client('ec2', region_name='us-east-1')
    # Create an EC2 client
    try:
        # Describe all volumes in the account
        response = ec2.describe_volumes()

        # Iterate through volumes and change type to 'gp3'
        for volume in response['Volumes']:
            volume_id = volume['VolumeId']
            current_volume_type = volume['VolumeType']

            if current_volume_type == 'gp2':
                # Change volume type to 'gp3'
                   ec2.modify_volume(
                           VolumeId=volume_id,
                           VolumeType='gp3')
                  print(f"Changed volume {volume_id} type from 'gp2' to 'gp3'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    change_all_volumes_to_gp3()
