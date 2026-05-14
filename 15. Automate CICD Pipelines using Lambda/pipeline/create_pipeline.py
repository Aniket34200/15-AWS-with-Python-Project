import boto3

codepipeline = boto3.client('codepipeline')

def create_pipeline():
    response = codepipeline.create_pipeline(
        pipeline={
            "name": "MyLambdaTriggeredPipeline",
            "roleArn": "arn:aws:iam::604475637990:role/CodePipelineServiceRole",
            "artifactStore": {
                "type": "S3",
                "location": "my-artifact-bucket-aniket-2026"
            },
            "stages": [
                {
                    "name": "Source",
                    "actions": [{
                        "name": "Source",
                        "actionTypeId": {
                            "category": "Source",
                            "owner": "AWS",
                            "provider": "S3",
                            "version": "1"
                        },
                        "outputArtifacts": [{"name": "source_output"}],
                        "configuration": {
                            "S3Bucket": "my-source-bucket-aniket-2026",
                            "S3ObjectKey": "source.zip"
                        },
                        "runOrder": 1
                    }]
                },
                {
                    "name": "Build",
                    "actions": [{
                        "name": "Build",
                        "actionTypeId": {
                            "category": "Build",
                            "owner": "AWS",
                            "provider": "CodeBuild",
                            "version": "1"
                        },
                        "inputArtifacts": [{"name": "source_output"}],
                        "outputArtifacts": [{"name": "build_output"}],
                        "configuration": {
                            "ProjectName": "my-codebuild-project"
                        },
                        "runOrder": 1
                    }]
                }
            ]
        }
    )

    print("Pipeline Created")

if __name__ == "__main__":
    create_pipeline()