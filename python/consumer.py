from dotenv import load_dotenv

import os
import random
import redis
import socket
import sys
import time

# Load environment variables / secrets from .env file.
load_dotenv()

# Work out the consumer ID from the IP address (assumes IP v4).
maybe_ip = socket.gethostbyname(socket.gethostname())
ip_parts = maybe_ip.split(".")

if len(ip_parts) != 4:
    sys.exit("Failed to work out consumer name from IP address :(")

consumer_name = ip_parts[3]
print(f"Consumer name: {consumer_name}.")

print("Connecting to Redis.")
redis_client = redis.from_url(os.getenv("REDIS_URL"))

while True:
    print("TODO...")
    time.sleep(9000)