import boto3

codebuild = boto3.client('codebuild')

def create_project():
    response = codebuild.create_project(
        name='my-codebuild-project',
        source={
            'type': 'S3',
            'location': 'my-source-bucket-aniket-2026/source.zip'
        },
        artifacts={
            'type': 'S3',
            'location': 'my-artifact-bucket-aniket-2026'
        },
        environment={
            'type': 'LINUX_CONTAINER',
            'image': 'aws/codebuild/standard:6.0',
            'computeType': 'BUILD_GENERAL1_SMALL'
        },
        serviceRole='arn:aws:iam::604475637990:role/CodeBuildServiceRole'
    )

    print("CodeBuild Project Created")

if __name__ == "__main__":
    create_project()