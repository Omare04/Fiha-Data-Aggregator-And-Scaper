from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def get_database():
    try:
        # Connect to MongoDB server
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command("ping")
        print("Successfully connected to MongoDB.")
        return client["fiha_stock_database"]
    except ConnectionFailure as e:
        print("Failed to connect to MongoDB:", e)
        exit(1)
