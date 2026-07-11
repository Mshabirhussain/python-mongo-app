from urllib.parse import quote_plus
from pymongo import MongoClient
import os

username = quote_plus(os.getenv("MONGO_DB_USERNAME"))
password = quote_plus(os.getenv("MONGO_DB_PASSWORD"))
host = os.getenv("MONGO_DB_HOSTNAME")

client = MongoClient(
    f"mongodb://{username}:{password}@{host}:27017/"
)