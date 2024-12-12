from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("MONGO_URI environment variable is not set!")

client = MongoClient(mongo_uri)
db = client["Spectral_data"]
