# Serverless Image Processing App

This project is a serverless image processing application using AWS S3, Lambda, and optionally API Gateway and DynamoDB. Users upload images to an S3 bucket, which triggers a Lambda function to process (resize, watermark) and store them in another S3 bucket.

## Architecture
- **Amazon S3**: Stores original and processed images
- **AWS Lambda**: Processes images (resize, watermark)
- **Amazon API Gateway (Optional)**: Exposes an API for uploads
- **Amazon DynamoDB (Optional)**: Stores image metadata

## Learning Outcomes
- Event-driven architectures with Lambda and S3 triggers
- Cost-efficient, auto-scaling serverless applications
- Security with IAM roles and S3 bucket policies

## Getting Started
See `infrastructure/` for deployment instructions.
