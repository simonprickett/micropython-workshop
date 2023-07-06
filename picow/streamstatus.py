from gfx_pack import SWITCH_E
from picoredis import Redis

import gfx
import time

def run():
    display = gfx.display

    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    
    # TODO connecting to Redis message
    display.text("TODO: Redis Stream Status", 5, 20, gfx.DISPLAY_WIDTH, 2)
    display.update()
    
    # TODO connect to Redis
    # TODO get stream information...
    
    # TODO periodically update this...
    
    while True:
        time.sleep(0.01)
    
        if gfx.gp.switch_pressed(SWITCH_E):
            return