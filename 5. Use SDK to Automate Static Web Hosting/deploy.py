import boto3
import os
import mimetypes

# CONFIG
BUCKET_NAME = "aniket-static-site-12345"  # must be globally unique
WEBSITE_DIR = r"E:\15 AWS with Python Projects\5. Use SDK to Automate Static Web Hosting\my-website"

s3 = boto3.client("s3")

# 1. Create Bucket
def create_bucket():
    try:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'
            }
        )
        print("Bucket created")
    except Exception as e:
        print("Bucket may already exist:", e)

# 2. Disable Block Public Access
def disable_block_public_access():
    s3.put_public_access_block(
        Bucket=BUCKET_NAME,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False
        }
    )
    print("Public access enabled")

# 3. Add Bucket Policy (Make Public)
def make_bucket_public():
    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"]
        }]
    }

    import json
    s3.put_bucket_policy(
        Bucket=BUCKET_NAME,
        Policy=json.dumps(policy)
    )
    print("Bucket policy applied")

# 4. Enable Static Website Hosting
def enable_website():
    s3.put_bucket_website(
        Bucket=BUCKET_NAME,
        WebsiteConfiguration={
            "IndexDocument": {"Suffix": "index.html"}
        }
    )
    print("Static website hosting enabled")

# 5. Upload Files
def upload_files():
    print("Uploading files from:", WEBSITE_DIR)

    for root, dirs, files in os.walk(WEBSITE_DIR):
        print("Current folder:", root)
        print("Files found:", files)

        for file in files:
            file_path = os.path.join(root, file)
            key = os.path.relpath(file_path, WEBSITE_DIR)

            content_type, _ = mimetypes.guess_type(file_path)

            s3.upload_file(
                file_path,
                BUCKET_NAME,
                key,
                ExtraArgs={
                    "ContentType": content_type or "application/octet-stream"
                }
            )
            print(f"Uploaded: {key}")

# 6. Main Execution
def main():
    create_bucket()
    disable_block_public_access()
    make_bucket_public()
    enable_website()
    upload_files()
    
    print("\nWebsite URL:")
    print(f"http://{BUCKET_NAME}.s3-website.ap-south-1.amazonaws.com")


if __name__ == "__main__":
    main()