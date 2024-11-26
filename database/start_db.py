import subprocess
import os
import time

def start_mongo():
    data_path = "./data"  # Path to the MongoDB data directory
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    mongo_command = ["mongod", "--dbpath", data_path]
    process = subprocess.Popen(
        mongo_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("MongoDB is starting...")

    # Wait for MongoDB to initialize
    time.sleep(5)
    print("MongoDB database started successfully.")

if __name__ == "__main__":
    start_mongo()
