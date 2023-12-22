import boto3

def copy_ami_to_another_region(source_ami_id, source_region, destination_region):
    # Set your AWS credentials for the source region
    source_access_key_id = 'YOUR_SOURCE_ACCESS_KEY'
    source_secret_access_key = 'YOUR_SOURCE_SECRET_KEY'

    # Create EC2 clients for source and destination regions
    source_ec2 = boto3.client('ec2', aws_access_key_id=source_access_key_id, aws_secret_access_key=source_secret_access_key, region_name=source_region)
    destination_ec2 = boto3.client('ec2', region_name=destination_region)

    try:
        # Copy the AMI to the destination region
        response = source_ec2.copy_image(
            SourceImageId=source_ami_id,
            SourceRegion=source_region,
            Name='AMI Copy to S3'
        )

        # Get the new AMI ID created by the copy operation
        new_ami_id = response['ImageId']

        # Wait for the new AMI to be available in the destination region
        waiter = destination_ec2.get_waiter('image_available')
        waiter.wait(ImageIds=[new_ami_id])

        return new_ami_id

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def export_ami_to_s3(ami_id, destination_region, s3_bucket_name, s3_object_key):
    # Set your AWS credentials for the destination region
    destination_access_key_id = 'YOUR_DESTINATION_ACCESS_KEY'
    destination_secret_access_key = 'YOUR_DESTINATION_SECRET_KEY'

    # Create EC2 and S3 clients for the destination region
    destination_ec2 = boto3.client('ec2', aws_access_key_id=destination_access_key_id, aws_secret_access_key=destination_secret_access_key, region_name=destination_region)
    s3 = boto3.client('s3', aws_access_key_id=destination_access_key_id, aws_secret_access_key=destination_secret_access_key, region_name=destination_region)

    try:
        # Create a presigned URL for the S3 bucket
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': s3_bucket_name, 'Key': s3_object_key},
            ExpiresIn=3600  # URL expires in 1 hour (adjust as needed)
        )

        # Export the AMI to S3
        response = destination_ec2.export_image(
            ImageId=ami_id,
            DiskImageFormat='VMDK',  # Change this format based on your requirements
            S3ExportLocation={
                'S3Bucket': s3_bucket_name,
                'S3Prefix': s3_object_key
            }
        )

        # Wait for the export task to complete
        export_task_id = response['ExportTaskId']
        waiter = destination_ec2.get_waiter('export_task_completed')
        waiter.wait(ExportTaskIds=[export_task_id])

        print(f"AMI {ami_id} exported to S3 at: {presigned_url}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    source_ami_id = 'YOUR_SOURCE_AMI_ID'
    source_region = 'YOUR_SOURCE_REGION'
    destination_region = 'YOUR_DESTINATION_REGION'
    s3_bucket_name = 'YOUR_S3_BUCKET_NAME'
    s3_object_key = 'YOUR_S3_OBJECT_KEY'

    new_ami_id = copy_ami_to_another_region(source_ami_id, source_region, destination_region)

    if new_ami_id:
        export_ami_to_s3(new_ami_id, destination_region, s3_bucket_name, s3_object_key)
