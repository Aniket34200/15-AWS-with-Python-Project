import boto3
import os

ec2 = boto3.resource('ec2', region_name='ap-south-1')
ec2_client = boto3.client('ec2', region_name='ap-south-1')

KEY_NAME = 'my-ec2-instance-key'
SG_NAME = 'my-sg'


# ✅ Create Key Pair
def create_key():
    try:
        response = ec2_client.create_key_pair(KeyName=KEY_NAME)

        with open(f"{KEY_NAME}.pem", "w") as f:
            f.write(response['KeyMaterial'])

        os.chmod(f"{KEY_NAME}.pem", 0o400)

        print(f"Key created: {KEY_NAME}.pem")

    except Exception as e:
        print("Key already exists or error:", e)


# ✅ Create Security Group
def create_sg():
    try:
        response = ec2_client.create_security_group(
            GroupName=SG_NAME,
            Description='Auto SG'
        )

        sg_id = response['GroupId']

        # Allow SSH
        ec2_client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )

        print(f"Security Group created: {sg_id}")
        return sg_id

    except Exception as e:
        print("SG exists or error:", e)

        # Get existing SG
        response = ec2_client.describe_security_groups(GroupNames=[SG_NAME])
        return response['SecurityGroups'][0]['GroupId']


# ✅ Launch Instance (Your Format + Added Automation)
def launch_instance():
    create_key()
    sg_id = create_sg()

    instances = ec2.create_instances(
        ImageId='ami-0f5ee92e2d63afc18',  # Amazon Linux (Mumbai)
        MinCount=1,
        MaxCount=1,
        InstanceType='t3.micro',
        KeyName=KEY_NAME,
        SecurityGroupIds=[sg_id],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': 'Auto-Instance'}
                ]
            }
        ]
    )

    instance = instances[0]
    print(f"Instance launched: {instance.id}")

    # Wait until running
    instance.wait_until_running()
    instance.load()

    print(f"Public IP: {instance.public_ip_address}")


if __name__ == "__main__":
    launch_instance()