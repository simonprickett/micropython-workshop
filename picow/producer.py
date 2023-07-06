from gfx_pack import SWITCH_A, SWITCH_E
from picoredis import Redis

import gfx
import random
import time

def run():
    STREAM_KEY = "jobs"

    JOB_TYPES = [
        "cleaning",
        "room_service",
        "taxi",
        "extra_towels",
        "extra_pillows"
    ]
    
    display = gfx.display

    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    
    gfx.display_centered("PRODUCER", 5, 2)
    x_pos = gfx.display_centered("A: Create Job", 35, 1)
    display.text("E: Exit", x_pos, 44, gfx.DISPLAY_WIDTH, 1)
    display.update()
    
    time.sleep(1)
    
    while True:
        time.sleep(0.01)
    
        if gfx.gp.switch_pressed(SWITCH_A):
            job = {
                "room": random.randint(100, 500),
                "job": random.choice(JOB_TYPES)
            }
            
            print(job)
            
            # TODO update the screen etc...
            time.sleep(1)
        elif gfx.gp.switch_pressed(SWITCH_E):
            return
