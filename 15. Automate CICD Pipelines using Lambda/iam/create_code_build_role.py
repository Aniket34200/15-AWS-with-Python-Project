import boto3
import json
import time

iam = boto3.client('iam')

def create_codebuild_role():
    role_name = "CodeBuildServiceRole"

    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "codebuild.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }

    try:
        iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy)
        )
        print("✅ CodeBuild Role Created")

        time.sleep(10)

        # Attach required policies
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn="arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess"
        )

        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess"
        )

        print("✅ Policies attached to CodeBuild role")

    except iam.exceptions.EntityAlreadyExistsException:
        print("⚠️ CodeBuild role already exists")


if __name__ == "__main__":
    create_codebuild_role()