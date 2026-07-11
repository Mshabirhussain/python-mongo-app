from urllib.parse import quote_plus
from pymongo import MongoClient
import os


username = quote_plus(
    os.getenv("MONGO_DB_USERNAME", "")
)

password = quote_plus(
    os.getenv("MONGO_DB_PASSWORD", "")
)

host = os.getenv(
    "MONGO_DB_HOSTNAME",
    "localhost"
)


mongo_uri = (
    f"mongodb://{username}:{password}@{host}:27017/"
)


client = MongoClient(mongo_uri)


# Database name
db = client["employee_db"]


# Collection name
collection = db["employees"]