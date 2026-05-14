import boto3

s3 = boto3.client('s3')
region = "ap-south-1"

def create_bucket(bucket_name):
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region
        }
    )
    print(f"{bucket_name} created")

if __name__ == "__main__":
    create_bucket("my-source-bucket-aniket-2026")
    create_bucket("my-artifact-bucket-aniket-2026")