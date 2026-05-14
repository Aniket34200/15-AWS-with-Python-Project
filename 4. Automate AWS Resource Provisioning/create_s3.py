import boto3

s3 = boto3.client('s3')

def create_bucket(bucket_name, region="ap-south-1"):
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
        print(f"Bucket {bucket_name} created.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    create_bucket("my-unique-demo-bucket-45678")