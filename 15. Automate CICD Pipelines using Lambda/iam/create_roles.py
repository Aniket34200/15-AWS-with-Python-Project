import boto3
import json

iam = boto3.client('iam')

def create_lambda_role():
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }

    role = iam.create_role(
        RoleName="LambdaCodePipelineTriggerRole",
        AssumeRolePolicyDocument=json.dumps(assume_role_policy)
    )

    iam.attach_role_policy(
        RoleName="LambdaCodePipelineTriggerRole",
        PolicyArn="arn:aws:iam::aws:policy/AWSCodePipeline_FullAccess"
    )

    iam.attach_role_policy(
        RoleName="LambdaCodePipelineTriggerRole",
        PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
    )

    print("Lambda Role Created")


def create_codepipeline_role():
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "codepipeline.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }

    role = iam.create_role(
        RoleName="CodePipelineServiceRole",
        AssumeRolePolicyDocument=json.dumps(assume_role_policy)
    )

    iam.attach_role_policy(
        RoleName="CodePipelineServiceRole",
        PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
    )

    print("CodePipeline Role Created")


if __name__ == "__main__":
    create_lambda_role()
    create_codepipeline_role()