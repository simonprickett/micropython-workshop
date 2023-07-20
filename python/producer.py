from dotenv import load_dotenv
from rich import print, print_json
from rich.progress import Progress
from rich.console import Console

import os
import random
import redis
import time

# Load environment variables / secrets from .env file.
load_dotenv()

JOB_TYPES = [
    "cleaning",
    "room_service",
    "taxi",
    "extra_towels",
    "extra_pillows"
]

print("Connecting to Redis.")
redis_client = redis.from_url(os.getenv("REDIS_URL"))

console = Console()
console.clear()

while True:
    job = {
        "room": random.randint(100, 500),
        "job": random.choice(JOB_TYPES)
    }

    job_id = redis_client.xadd(os.getenv("REDIS_STREAM_KEY"), job)

    print(f"Created job [bold reverse]{job_id}[/bold reverse]:")
    print_json(data = job)

    wait_time = random.randint(5, 10)

    with Progress() as progress:
        wait_task = progress.add_task("[yellow]Waiting...", total = 100, completed = 100)

        while progress.tasks[0].completed > 0:
            time.sleep(wait_time / 100)
            progress.update(wait_task, advance = -1)
        
    time.sleep(0.5)
    console.clear()
