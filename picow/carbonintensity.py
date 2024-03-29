from gfx_pack import SWITCH_E

import gfx
import json
import secrets
import time
import urequests
            
def refresh_intensity_display():
    BAR_MIN_X = 50
    BAR_MAX_X = 120
    BAR_HEIGHT = 4
    
    display = gfx.display

    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    gfx.display_centered("UPDATING...", 25, 2)
    display.update()
    
    response_doc = urequests.get(secrets.CARBON_INTENSITY_URL).json()
    
    # Get the region name
    region_name = response_doc["data"][0]["shortname"]
    
    # Get the intensity index (very low, low, moderate, high, very high)
    intensity_index = response_doc["data"][0]["data"][0]["intensity"]["index"]

    # Pick out values from the generation mix data...
    # We want solar, wind, gas, nuclear, then other is 100% minus the total of those.
    
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
    
    sorted_generators = sorted([
        (solar_width, "SOLAR"),
        (wind_width, "WIND"),
        (nuclear_width, "NUCLEAR"),
        (gas_width, "GAS"),
        (others_width, "OTHERS")
    ], reverse = True)
            
    gfx.clear_screen()

    # Set backlight according to intensity...
    if intensity_index == "very low":
        gfx.set_backlight(0, 64, 0, 0)
    elif intensity_index == "low":
        gfx.set_backlight(128, 64, 0, 0)
    elif intensity_index == "moderate":
        gfx.set_backlight(128, 16, 0, 0)
    elif intensity_index == "high" or intensity_index == "very high":
        gfx.set_backlight(128, 0, 0, 0)

    # Centre the region name on screen.
    gfx.display_centered(region_name, 2, 1)

    v_pos = 10
    for g in sorted_generators:
        display.text(g[1], 5, v_pos, gfx.DISPLAY_WIDTH, 1)
        display.line(BAR_MIN_X, v_pos + 3, BAR_MIN_X + g[0], v_pos + 3, BAR_HEIGHT)
        v_pos += 10
        
    display.text("E: Exit", 95, 50, gfx.DISPLAY_WIDTH, 1)   
    display.update()
          
def run():
    refresh_intensity_display()
    display = gfx.display
    last_updated = time.ticks_ms()
    ticks_before = last_updated
    bar_width = gfx.DISPLAY_WIDTH
    BAR_UPDATE_FREQUENCY = 1000
    
    while True:
        time.sleep(0.01)
        
        if gfx.gp.switch_pressed(SWITCH_E):
            return
            
        ticks_now = time.ticks_ms()
        
        if time.ticks_diff(ticks_now, ticks_before) > BAR_UPDATE_FREQUENCY:
            bar_width = bar_width - (gfx.DISPLAY_WIDTH // secrets.CARBON_INTENSITY_UPDATE_FREQUENCY)
            ticks_before = time.ticks_ms()
            
        if time.ticks_diff(ticks_now, last_updated) > secrets.CARBON_INTENSITY_UPDATE_FREQUENCY * 1000:
            refresh_intensity_display()
            last_updated = time.ticks_ms()
            bar_width = gfx.DISPLAY_WIDTH
            
        gfx.clear_rect(0, 61, gfx.DISPLAY_WIDTH, 61, 2)
        display.line(0, 61, bar_width, 61, 2)
        display.update()