import json
import boto3

codepipeline = boto3.client('codepipeline')

PIPELINE_NAME = "MyLambdaTriggeredPipeline"

def lambda_handler(event, context):
    try:
        response = codepipeline.start_pipeline_execution(
            name=PIPELINE_NAME
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Pipeline triggered successfully',
                'executionId': response['pipelineExecutionId']
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }