import gfx
import json
import secrets
import time
import urequests

def display_intensity_info():
    BAR_MIN_X = 50
    BAR_MAX_X = 120
    BAR_HEIGHT = 4
    
    display = gfx.display
    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    display.text("Loading Data...", 5, 20, gfx.DISPLAY_WIDTH, 2)
    display.update()
    
    response_doc = urequests.get(f"https://api.carbonintensity.org.uk/regional/postcode/{secrets.CARBON_INTENSITY_POSTCODE}").json()
    
    # Get the region name
    region_name = response_doc["data"][0]["shortname"]
    
    # Get the intensity index (very low, low, moderate, high)
    intensity_index = response_doc["data"][0]["data"][0]["intensity"]["index"]
    print(intensity_index)

    # Pick out values from the generation mix data...
    # we want solar, wind, gas, nuclear, then other is 100% minus the total of those.
    
    solar_pct = 0
    wind_pct = 0
    nuclear_pct = 0
    gas_pct = 0
    
    for g in response_doc["data"][0]["data"][0]["generationmix"]:
        if g["fuel"] == "solar":
            solar_pct = g["perc"]
        elif g["fuel"] == "wind":
            wind_pct = g["perc"]
        elif g["fuel"] == "gas":
            gas_pct = g["perc"]
        elif g["fuel"] == "nuclear":
            nuclear_pct = g["perc"]
            
    others_pct = 100 - solar_pct - wind_pct - nuclear_pct - gas_pct
    
    one_percent_length = (BAR_MAX_X - BAR_MIN_X) / 100
    solar_width = round(one_percent_length * solar_pct)
    wind_width = round(one_percent_length * wind_pct)
    nuclear_width = round(one_percent_length * nuclear_pct)
    gas_width = round(one_percent_length * gas_pct)
    others_width = round(one_percent_length * others_pct)
    
    print(f"solar {solar_pct}")
    print(f"wind {wind_pct}")
    print(f"gas {gas_pct}")
    print(f"nuclear {nuclear_pct}")
    print(f"others {others_pct}")
        
    gfx.clear_screen()

    # Set backlight according to intensity...
    if intensity_index == "very low":
        gfx.set_backlight(0, 64, 0, 0)
    elif intensity_index == "low":
        gfx.set_backlight(128, 64, 0, 0)
    elif intensity_index == "moderate":
        gfx.set_backlight(128, 16, 0, 0)
    elif intensity_index == "high":
        gfx.set_backlight(128, 0, 0, 0)

    # TODO centre the region name and draw a line unnder it...
    # TODO consider adding update time
    # TODO consider showing these in descending percentage order
    display.text(region_name, 5, 3, gfx.DISPLAY_WIDTH, 1)
    display.text("SOLAR", 5, 15, gfx.DISPLAY_WIDTH, 1)
    display.text("WIND", 5, 25, gfx.DISPLAY_WIDTH, 1)
    display.text("GAS", 5, 35, gfx.DISPLAY_WIDTH, 1)
    display.text("NUCLEAR", 5, 45, gfx.DISPLAY_WIDTH, 1)
    display.text("OTHERS", 5, 55, gfx.DISPLAY_WIDTH, 1)
    display.line(BAR_MIN_X, 18, BAR_MIN_X + solar_width, 18, BAR_HEIGHT)
    display.line(BAR_MIN_X, 28, BAR_MIN_X + wind_width, 28, BAR_HEIGHT)
    display.line(BAR_MIN_X, 38, BAR_MIN_X + gas_width, 38, BAR_HEIGHT)
    display.line(BAR_MIN_X, 48, BAR_MIN_X + nuclear_width, 48, BAR_HEIGHT)
    display.line(BAR_MIN_X, 58, BAR_MIN_X + others_width, 58, BAR_HEIGHT)
    display.update()
    
    
    while True:
        time.sleep(0.5)
        
        
        
