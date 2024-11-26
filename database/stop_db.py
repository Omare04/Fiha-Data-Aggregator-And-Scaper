import os
import signal
import subprocess

def stop_mongo():
    try:
        # Find the mongod process
        result = subprocess.run(
            ["pgrep", "mongod"], capture_output=True, text=True, check=True
        )
        process_ids = result.stdout.strip().split("\n")

        if process_ids:
            print("Stopping MongoDB...")
            for pid in process_ids:
                os.kill(int(pid), signal.SIGTERM)
                print(f"MongoDB process {pid} stopped.")
        else:
            print("No MongoDB process found.")

    except subprocess.CalledProcessError:
        print("MongoDB is not running.")

if __name__ == "__main__":
    stop_mongo()
