import boto3
from PIL import Image
import os
import io

# Initialize the S3 client once (outside the handler for efficiency)
s3_client = boto3.client('s3')

# Environment variables for configuration
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']  # Destination bucket for resized images
THUMB_WIDTH = int(os.environ.get('THUMB_W', '300'))  # Default width if not provided
THUMB_HEIGHT = int(os.environ.get('THUMB_H', '300'))  # Default height if not provided

def lambda_handler(event, context):
    """
    Lambda entry point for image resizing.
    Expects event payload with 'bucket' and 'key' fields.
    Example:
    {
      "bucket": "image-input-dev-269372836149",
      "key": "example.jpg"
    }
    """
    try:
        # Extract source bucket and object key from the event
        src_bucket = event['bucket']
        src_key = event['key']

        # Download the image object from S3
        response = s3_client.get_object(Bucket=src_bucket, Key=src_key)
        image_bytes = response['Body'].read()

        # Open the image using Pillow
        img = Image.open(io.BytesIO(image_bytes))

        # Resize the image to thumbnail dimensions (preserves aspect ratio)
        img.thumbnail((THUMB_WIDTH, THUMB_HEIGHT))

        # Save the resized image into an in-memory buffer
        buffer = io.BytesIO()
        # Default to JPEG if format is missing
        image_format = img.format if img.format else 'JPEG'
        img.save(buffer, format=image_format)
        buffer.seek(0)

        # Construct output file name (e.g., thumbnails/example_thumb.jpg)
        filename = os.path.basename(src_key)  # Extract file name only
        name, ext = os.path.splitext(filename)
        # Ensure extension is valid, fallback to .jpg
        output_key = f"thumbnails/{name}_thumb{ext if ext else '.jpg'}"

        # Upload the resized image to the output bucket
        s3_client.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=buffer.getvalue(),
            ContentType=f"image/{image_format.lower()}"
        )

        # Return success response with the new file path
        return {
            "status": "success",
            "file": output_key
        }

    except Exception as error:
        # Return error details for debugging
        return {
            "status": "error",
            "message": str(error)
        }
