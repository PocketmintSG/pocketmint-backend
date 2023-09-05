import json
from bson import json_util

### QUICK FIX FOR IMPORT ERROR, NEED TO REFACTOR ##
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.environ.get("ENV")
MONGODB_URI = os.environ.get("MONGODB_URI_DEV" if ENV == "dev" else "MONGODB_URI_PROD")


def get_cluster_connection() -> MongoClient:
    client = MongoClient(MONGODB_URI)
    return client


def seed_insurance():
    cluster = get_cluster_connection()
    insurance_db = cluster["pocketmint"]["insurance_details"]
    with open("seed_data_insurance.json", "r") as f:
        data = json.load(f)
        for insurance_detail in data:
            res = insurance_db.insert_one(insurance_detail)


if __name__ == "__main__":
    seed_insurance()
