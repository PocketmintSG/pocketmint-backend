# Getting Started

## First-Time Setup

`pocketmint-backend` uses python3.10.

1. Install [python3.10](https://www.python.org/downloads/release/python-3100/)
2. Run `virtualenv -p 3.10 venv`
3. Activate the virtual environment by running `source venv/bin/activate`
4. Install required python libraries by running `pip install -r requirements.txt`
5. See Running on how to run the server

## Running

To run the app:

1. Activate your virtual environment by running `source venv/bin/activate`
2. Execute `uvicorn api.main:app --reload`

# AWS Configurations

- [Modify S3 bucket permissions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteAccessPermissionsReqd.html)
- [boto3 to upload images to S3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
