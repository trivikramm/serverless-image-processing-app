# Deployment Instructions

## Prerequisites
- AWS CLI configured
- AWS SAM CLI installed
- Python 3.11

## Steps
1. Install dependencies for Lambda:
   ```
   cd lambda
   pip install -r ../infrastructure/requirements.txt -t .
   ```
2. Deploy with AWS SAM:
   ```
   cd ../infrastructure
   sam build
   sam deploy --guided
   ```
3. Upload an image to the original images S3 bucket to trigger processing.

## Notes
- Processed images will appear in the processed images bucket.
- Update `template.yaml` to add API Gateway or DynamoDB if needed.
