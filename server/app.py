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

@app.route("/", methods = ["GET"])
def home_page():
    return render_template("homepage.html")