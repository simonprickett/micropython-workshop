from dotenv import load_dotenv
from rich import print
from rich.progress import Progress
from rich.console import Console

import os
import requests
import time

# Load environment variables / secrets from .env file.
load_dotenv()

# TODO put this in a timed loop.
console = Console()
console.clear()

response_doc = requests.get(f"https://api.carbonintensity.org.uk/regional/postcode/{os.getenv('CARBON_INTENSITY_POSTCODE')}").json()

# Get the region name.
region_name = response_doc["data"][0]["shortname"]

# Get the intensity index (very low, low, moderate, high, very high)
intensity_index = response_doc["data"][0]["data"][0]["intensity"]["index"]

# Pick out values from the generation mix data...
# We want solar, wind, gas, nuclear then other is 100% minus the total of those.

solar_pct = 0
wind_pct = 0
nuclear_pct = 0
gas_pct = 0

for g in response_doc["data"][0]["data"][0]["generationmix"]:
    if g["fuel"] == "solar":
        solar_pct = g["perc"]
    if g["fuel"] == "wind":
        wind_pct = g["perc"]
    if g["fuel"] == "gas":
        gas_pct = g["perc"]
    if g["fuel"] == "nuclear":
        nuclear_pct = g["perc"]

others_pct = 100 - solar_pct - wind_pct - nuclear_pct - gas_pct

sorted_generators = sorted([
    (solar_pct, "Solar"),
    (wind_pct, "Wind"),
    (nuclear_pct, "Nuclear"),
    (gas_pct, "Gas"),
    (others_pct, "Others")
], reverse = True)

# Translate intensity_index into color formatting.
if intensity_index == "very low":
    intensity_color = "black on green"
elif intensity_index == "low":
    intensity_color = "black on yellow"
elif intensity_index == "moderate":
    intensity_color = "white on dark_orange"
elif intensity_index == "high" or intensity_index == "very high":
    intensity_color = "white on red"

print(f"[{intensity_color} bold]{region_name}")
print("")

with Progress() as progress:
    for g in sorted_generators:
        # TODO Suppress the time display if possible?
        progress.add_task(g[1], total = 100, completed = g[0])

    wait_task = progress.add_task("[yellow]Next Update...", total = 100)
