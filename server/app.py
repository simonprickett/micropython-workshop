from dotenv import load_dotenv
from flask import Flask, render_template

import os
import redis

# Load environment variables / secrets from file.
load_dotenv()

# Connect to Redis.
redis_client = redis.from_url(os.getenv("REDIS_URL"))

app = Flask(__name__)

@app.route("/regional/postcode/<postcode>", methods = ["GET"])
def carbon_intensity_simulator(postcode):
    pass

@app.route("/status", methods = ["GET"])
def stream_status():
    response = redis_client.xinfo_groups(os.getenv("REDIS_STREAM_KEY"))
    
    # response looks like this (and may contain many groups) so we have to 
    # find the group we want:
    # [{'name': 'staff', 'consumers': 3, 'pending': 23, 'last-delivered-id': '1689852169094-0', 'entries-read': 49, 'lag': 264}]

    group_info = dict()

    for consumer_group in response:
        if consumer_group["name"] == os.getenv("REDIS_CONSUMER_GROUP"):
            # Found our consumer group, grab the values we want.
            group_info["lag"] = consumer_group["lag"]
            group_info["consumers"] = consumer_group["consumers"]
            group_info["pending"] = consumer_group["pending"]
            break

    return group_info

@app.route("/", methods = ["GET"])
def home_page():
    return render_template("homepage.html")