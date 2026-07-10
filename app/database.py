import os
from pymongo import MongoClient


mongo_host = os.getenv(
    "MONGO_DB_HOSTNAME",
    "mongo"
)

mongo_user = os.getenv(
    "MONGO_DB_USERNAME",
    "devdb"
)

mongo_password = os.getenv(
    "MONGO_DB_PASSWORD",
    "dev@123"
)


client = MongoClient(
    f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:27017/admin"
)


database = client["users"]

collection = database["users"]