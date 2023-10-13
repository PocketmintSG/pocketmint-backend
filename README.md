# Introduction

Pocketmint is split into two parts: A frontend repository and a backend repository. This is the frontend repository.

## Frameworks and Language

The backend repository is written in Python using the FastAPI framework. It uses MongoDB as its database, using the Pymongo driver. This repository handles requests using the typical API-driven approach, in contrast to newer approaches like using GraphQL.

## Hosting and Authentication

`pocketmint-backend` is hosted using an AWS EC2 instance. Unlike `pocketmint-frontend`, it does not have automatic CI/CD setup. The CI/CD that's set up can be safely ignored, as it was legacy code from previous attempts at hosting.

As such, with each new deployment to `main`, the EC2 needs to be SSH'd into and pulled to reflect the latest changes. Refer to "Connecting to EC2 Instance" for more information on how to do so.

Notably, authentication is handled under the `Pocketmint Frontend` project in the firebase console.

# Setting Up

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

# Configurations

## Connecting to EC2 Instance

This server is hosted on EC2, using the Pocketmint AWS account. To SSH to the EC2 instance:

1. Obtain a copy of `pocketmint-backend-key.pem` secret.
2. Execute `ssh -i "pocketmint-backend-key.pem" ubuntu@ec2-18-141-203-207.ap-southeast-1.compute.amazonaws.com`
3. To update the server, kill the `uvicorn` process by `grep`-ing the previous `uvicorn` process by doing `ps aux | grep "uvicorn api.main:app"`. Once you obtain the PID of the process, kill it by executing `kill <PID>`. Execute `git pull origin main` to fetch new changes. To restart the server, execute `nohup python3 -m uvicorn api.main:app &`.

## Connecting to the MongoDB Instance

1. Note that you have to add your IP address to the MongoDB cluster to allow connections to it.
2. Connect to the MongoDB instance using the following URI: `mongodb+srv://pocketmint-dev:<MongoDB password>@dev.gx0pb5p.mongodb.net/`

## AWS Configurations

- [Modify S3 bucket permissions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteAccessPermissionsReqd.html)
- [boto3 to upload images to S3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

# Repository Walkthrough

I will be covering important files and codebase organization in this section. I won't be covering every file, just important ones to note.

## Under `/`

Most files here are self-explanatory. `firebase_config.json` and `firebase_secrets.json` are config files used for authentication.

## Under `/api`

- `/configs`: Contains configs that are global to the repository. Currently, some refactoring needs to take place to avoid hard-coding strings in the repository, such as error messages.
- `/models`: Contains request and response models used by Pydantic and FastAPI, to determine the shape of API requests and responses.
- `/routers`: Contains the relevant routers and its handlers used to service API calls. `router.py` can be thought of as the root router that's used to service all routers.
- `/seeds`: Used to seed the MongoDB database. Also contains a utility file, `seed_data_insurance.py`, used to seed insurance data.
- `/types`: Contains common Pydantic types used across the different routers. This is where I placed useful type hints, such as the Enum values for insurance types.
- `/utils`: Contains utility functions.
