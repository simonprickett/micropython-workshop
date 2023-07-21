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

stream_config = dict()
stream_config[os.getenv("REDIS_STREAM_KEY")] = ">"

while True:
    print("Fetching next job...")

    response = redis_client.xreadgroup(
        os.getenv("REDIS_CONSUMER_GROUP"), 
        consumer_name, 
        stream_config,
        1, 
        5000
    )

    # response looks like:
    # [['jobs', [('1689851801724-0', {'room': '281', 'job': 'extra_towels'})]]]
    # or None if there are no new jobs.

    if response is None:
        print("No new jobs.")
    else:
        # Do the job.
        job_id = response[0][1][0][0]
        job_details = response[0][1][0][1]

        print(f"Job ID: {job_id}")
        print(f"Room: {job_details['room']}")
        print(f"Job: {job_details['job']}")

        # TODO wait for a bit to simulate doing work.

        # Tell Redis the job is completed.
        redis_client.xack(
            os.getenv("REDIS_STREAM_KEY"), 
            os.getenv("REDIS_CONSUMER_GROUP"), 
            job_id
        )

    # TODO wait for a random amount of time before looking for 
    # the next job.
    time.sleep(9000)