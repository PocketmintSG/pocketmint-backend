# Getting Started

## First-Time Local Setup

`pocketmint-backend` uses python3.10.

1. Install [python3.10](https://www.python.org/downloads/release/python-3100/)
2. Run `virtualenv -p 3.10 venv`
3. Activate the virtual environment by running `source venv/bin/activate`
4. Install required python libraries by running `pip install -r requirements.txt`
5. See Running on how to run the server

## Running Locally

To run the app:

1. Activate your virtual environment by running `source venv/bin/activate`
2. Execute `uvicorn api.main:app --reload`

NOTE: After each commit/merge to the `main` branch, you need to connect to the EC2 instance to pull and reflect the changes.

## Connecting to EC2 Instance

This server is hosted on EC2, using the Pocketmint AWS account. To SSH to the EC2 instance:

1. Obtain a copy of `pocketmint-backend-key.pem` secret.
2. Execute `ssh -i "pocketmint-backend-key.pem" ubuntu@ec2-18-141-203-207.ap-southeast-1.compute.amazonaws.com`
3. To update the server, kill the `uvicorn` process by `grep`-ing the previous `uvicorn` process by doing `ps aux | grep "uvicorn api.main:app"`. Once you obtain the PID of the process, kill it by executing `kill <PID>`. Execute `git pull origin main` to fetch new changes. To restart the server, execute `nohup python3 -m uvicorn api.main:app &`.

## Connecting to the MongoDB Instance

1. Note that you have to add your IP address to the MongoDB cluster to allow connections to it.
2. Connect to the MongoDB instance using the following URI: `mongodb+srv://pocketmint-dev:<MongoDB password>@dev.gx0pb5p.mongodb.net/`

# AWS Configurations

- [Modify S3 bucket permissions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteAccessPermissionsReqd.html)
- [boto3 to upload images to S3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
