from dotenv import load_dotenv
from rich import print, print_json
from rich.progress import Progress
from rich.console import Console

import os
import random
import redis
import sys
import time

# Load environment variables / secrets from .env file.
load_dotenv()

print("Connecting to Redis.")
redis_client = redis.from_url(os.getenv("REDIS_URL"))

console = Console()
console.clear()

while True:
    response = redis_client.xinfo_groups(os.getenv("REDIS_STREAM_KEY"))

    if response is None:
        sys.exit(f"Failed to get consumer group info for stream at {os.getenv('REDIS_STREAM_KEY')}")

    # response looks like this (and may contain many groups) so we have to 
    # find the group we want:
    # [{'name': 'staff', 'consumers': 3, 'pending': 23, 'last-delivered-id': '1689852169094-0', 'entries-read': 49, 'lag': 264}]

    found_it = False

    for consumer_group in response:
        if consumer_group["name"] == os.getenv("REDIS_CONSUMER_GROUP"):
            # Found our consumer group!
            current_lag = consumer_group["lag"]

            if current_lag < 3:
                lag_color = "black on green"
            elif current_lag < 6:
                lag_color = "black on yellow"
            elif current_lag < 9:
                lag_color = "white on dark orange"
            else:
                lag_color = "white on red"
            
            print(f"[{lag_color} bold]{os.getenv('REDIS_CONSUMER_GROUP')} Consumer Group Status")
            print("")
            print(f"Consumers: {consumer_group['consumers']}")
            print(f"In Progress: {consumer_group['pending']}")
            print(f"Lag: {current_lag}")
            print("")
            print("Full response:")
            print_json(data = consumer_group)
            print("")
            found_it = True

    if not found_it:
        sys.exit(f"Failed to find consumer group {os.getenv('REDIS_CONSUMER_GROUP')} for stream at {os.getenv('REDIS_STREAM_KEY')}")

    # TODO progress bar counting down to update...
    time.sleep(5)
    console.clear()