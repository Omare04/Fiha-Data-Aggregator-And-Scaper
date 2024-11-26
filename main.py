from Classes.Stock import Stock
from Classes.Market import Market
from datetime import time, datetime
from database.db import get_database
# from start_db import start_mongo
import time

def main():
    # Start MongoDB server
    # start_mongo()
    time.sleep(5)  # Wait to ensure MongoDB is fully initialized

    # Connect to the database
    db = get_database()
    collection = db["articles"]

    # collection.insert_one(sample_data)

    print("Inserted document:", list(collection.find()))

if __name__ == "__main__":
    main()
