from dotenv import load_dotenv
from flask import Flask, render_template

import datetime
import os
import random
import redis

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%MZ"
INTENSITY_INDEX_VALUES = [ "very low", "low", "moderate", "high", "very high" ]
GENERATION_MIX_FUELS = [ "biomass", "coal", "wind", "solar", "imports", "gas", "nuclear", "hydro", "other"]

# Load environment variables / secrets from file.
load_dotenv()

# Connect to Redis.
redis_client = redis.from_url(os.getenv("REDIS_URL"))

app = Flask(__name__)

@app.route("/regional/postcode/<postcode>", methods = ["GET"])
def carbon_intensity_simulator(postcode):
    # Adjust the times to be the current half hour period.
    # TODO finish the fake data here...
    from_datetime = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0, second=0)
    to_datetime = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0, second=0)

    if from_datetime.minute < 30:
        from_datetime = from_datetime.replace(minute = 0)
        to_datetime = to_datetime.replace(minute = 30)
    else:
        from_datetime = from_datetime.replace(minute = 30)
        to_datetime = to_datetime.replace(minute = 0)
        to_datetime = to_datetime + datetime.timedelta(hours = 1)

    intensity_index = random.choice(INTENSITY_INDEX_VALUES)

    forecast = 0

    if intensity_index == "very low":
        forecast = random.randint(0, 49)
    elif intensity_index == "low":
        forecast = random.randint(50, 99)
    elif intensity_index == "moderate":
        forecast = random.randint(100, 199)
    elif intensity_index == "high":
        forecast = random.randint(200, 299)
    else:
        forecast = random.randint(300, 399)

    generation_mix = []
    percentage_remaining = 100
    random.shuffle(GENERATION_MIX_FUELS)

    for fuel in GENERATION_MIX_FUELS: 
        this_fuel_perc = random.randint(0, percentage_remaining)
        percentage_remaining = percentage_remaining - this_fuel_perc
        if percentage_remaining < 0:
            percentage_remaining = 0

        generation_mix.append({
            "fuel": fuel,
            "perc": this_fuel_perc
        })

    mix_data = [{
        "from": from_datetime.strftime(DATE_TIME_FORMAT),
        "to": to_datetime.strftime(DATE_TIME_FORMAT),
        "intensity": {
            "forecast": forecast,
            "index": intensity_index
        },
        "generationmix": generation_mix
    }]
    response = dict()
    response["data"] = [{
        "regionid": 12,
        "dnoregion": "SSE South",
        "shortname": "South England",
        "postcode": postcode,
        "data": mix_data
    }]

    return response

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