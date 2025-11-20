# CCMP 200: Serverless Image Processing Pipeline

## Overview
A serverless application that automatically resizes images uploaded to an S3 bucket using AWS Lambda, Step Functions, and API Gateway.

## Architecture
### Request Flow Diagram

```
Client (Web/Mobile/CLI)
        |
        v
+-------------------+
|   API Gateway     |
|  (POST /process)  |
+-------------------+
        |
        v
+-------------------+
|  Step Functions   |
| ImageProcessingWorkflow |
+-------------------+
        |
   +---------+---------+
   |                   |
   v                   v
Lambda (Image Resize)  Lambda (Metadata/Validation)
   |                   |
   +---------+---------+
             |
             v
        S3 Bucket (Processed Images)
```

* API Gateway triggers the workflow via a POST request.
* Step Functions orchestrates the image resizing process.
* Lambda resizes the image using Pillow and stores the result.
* S3 stores both original and resized images.


## Prerequisites
- AWS account with access to:       
   - S3
   - Lambda
   - Step Functions
   - API Gateway
* Python 3.12 with Pillow installed
* IAM roles with appropriate permissions
* Region: ca-central-1


## Deployment Steps
1. Create S3 buckets: `image-input-dev-269372836149`, `image-output-dev-269372836149`
2. Deploy Lambda function with image library
3. Set up Step Functions state machine
4. Connect API Gateway to Step Functions
5. Test by uploading an image

## API Endpoint
`https://63u3x8ga69.execute-api.ca-central-1.amazonaws.com/process`

## License
MIT

## How to Test
1. Upload an image (example.jpg) into the input S3 bucket: `image-input-dev-269372836149`
2. Run the command below in your terminal:
* PowerShell
```ps1
Invoke-RestMethod -Uri "https://63u3x8ga69.execute-api.ca-central-1.amazonaws.com/process" `
  -Method POST `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"bucket":"image-input-dev-269372836149","key":"example.jpg"}'
```

* curl (Linux/macOS)
```bash
curl -X POST https://63u3x8ga69.execute-api.ca-central-1.amazonaws.com/process \
  -H "Content-Type: application/json" \
  -d '{"bucket":"image-input-dev-269372836149","key":"example.jpg"}'
```

You can check Step Functions execution history to verify success and inspect logs in CloudWatch.

3. Check your S3 output bucket `image-output-dev-269372836149` to see the resized image created.


