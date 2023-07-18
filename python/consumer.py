from dotenv import load_dotenv

import os
import random
import redis
import time

# Load environment variables / secrets from .env file.
load_dotenv()

print("Connecting to Redis.")
redis_client = redis.from_url(os.getenv("REDIS_URL"))

while True:
    print("TODO...")