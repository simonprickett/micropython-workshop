from dotenv import load_dotenv
from rich import print
from rich.progress import Progress
from rich.console import Console

import os
import random
import redis
import sys
import time

# Load environment variables / secrets from .env file.
load_dotenv()

# Get the consumer name from the command line parameter.
if len(sys.argv) != 2:
    sys.exit("Usage: python consumer.py <consumername>")

consumer_name = sys.argv[1]
print(f"Consumer name: {consumer_name}.")
time.sleep(1.5)

print("Connecting to Redis.")
redis_client = redis.from_url(os.getenv("REDIS_URL"))

stream_config = dict()
stream_config[os.getenv("REDIS_STREAM_KEY")] = ">"

console = Console()
console.clear()

while True:
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

    console.clear()

    if response is None:
        print("No new jobs.")
    else:
        # Do the job.
        job_id = response[0][1][0][0]
        job_details = response[0][1][0][1]
        print(f"[white on dark_orange bold]Consumer: {consumer_name}")
        print("")
        print(f"Job ID: {job_id}")
        print(f"Room: {job_details['room']}")
        print(f"Job: {job_details['job']}")

        # Simulate doing the work...
        wait_time = random.randint(5, 10)

        with Progress() as progress:
            wait_task = progress.add_task("[yellow]Working...", total = 100, completed = 100)

            while progress.tasks[0].completed > 0:
                time.sleep(wait_time / 100)
                progress.update(wait_task, advance = -1)
        
        # Tell Redis the job is completed.
        redis_client.xack(
            os.getenv("REDIS_STREAM_KEY"), 
            os.getenv("REDIS_CONSUMER_GROUP"), 
            job_id
        )

        time.sleep(1)

    # Wait for a random amount of time before looking for the next job.
    console.clear()
    print(f"[white on dark_orange bold]Consumer: {consumer_name}")
    print("")
    
    wait_time = random.randint(5, 10)

    with Progress() as progress:
        wait_task = progress.add_task("[green]Resting...", total = 100, completed = 100)

        while progress.tasks[0].completed > 0:
            time.sleep(wait_time / 100)
            progress.update(wait_task, advance = -1)