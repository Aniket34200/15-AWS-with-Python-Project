import json
import boto3
from PIL import Image
import io
import urllib.parse

# Initialize S3 client
s3 = boto3.client('s3')

# Configuration
BUCKET_NAME = "image-resizer-2026"
SOURCE_PREFIX = "original/"
DEST_PREFIX = "resize-image/"
JPEG_QUALITY = 70   # Adjust (0–100). Lower = smaller size

def lambda_handler(event, context):
    try:
        # Get file details from event
        key = urllib.parse.unquote_plus(
            event['Records'][0]['s3']['object']['key']
        )

        print(f"Processing file: {key}")

        # Process only files inside 'original/' folder
        if not key.startswith(SOURCE_PREFIX):
            print("Not in source folder. Skipping.")
            return {
                'statusCode': 200,
                'body': json.dumps('Skipped non-source file')
            }

        # Extract file name
        file_name = key.split("/")[-1]

        # Get image from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        image_content = response['Body'].read()

        # Open image
        image = Image.open(io.BytesIO(image_content))

        # Get original format
        original_format = image.format

        # Convert for compatibility (needed for JPEG compression)
        if original_format in ["JPEG", "JPG"]:
            image = image.convert("RGB")

        # Save optimized image to buffer
        buffer = io.BytesIO()

        if original_format in ["JPEG", "JPG"]:
            # Compress JPEG (lossy)
            image.save(
                buffer,
                format="JPEG",
                quality=JPEG_QUALITY,
                optimize=True
            )
            content_type = "image/jpeg"

        elif original_format == "PNG":
            # Optimize PNG (lossless, limited compression)
            image.save(
                buffer,
                format="PNG",
                optimize=True
            )
            content_type = "image/png"

        else:
            # Fallback for other formats
            image.save(buffer, format=original_format)
            content_type = f"image/{original_format.lower()}"

        buffer.seek(0)

        # Destination key
        dest_key = f"{DEST_PREFIX}{file_name}"

        # Upload optimized image
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=dest_key,
            Body=buffer,
            ContentType=content_type
        )

        print(f"Optimized image saved to {dest_key}")

        return {
            'statusCode': 200,
            'body': json.dumps(f'Image optimized and saved to {dest_key}')
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }