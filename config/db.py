from pymongo import MongoClient

MONGO_URI = "mongodb+srv://AgrisensDB:csio%4012345@cluster0.eyxyi.mongodb.net/"

client = MongoClient(MONGO_URI)

db = client["Spectral_data"]  
