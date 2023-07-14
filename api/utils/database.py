from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.environ.get("ENV")
MONGODB_URI = os.environ.get("MONGODB_URI_DEV" if ENV == "dev" else "MONGODB_URI_PROD")


def get_cluster_connection() -> MongoClient:
    client = MongoClient(MONGODB_URI)
    return client
