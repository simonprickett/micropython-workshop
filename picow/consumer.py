from gfx_pack import SWITCH_A, SWITCH_E

import gfx
import redis
import time

def show_options(consumer_id):
    display = gfx.display
    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    gfx.display_centered(f"CONSUMER {consumer_id}", 5, 2)
    x_pos = gfx.display_centered("A: Get Next Job", 35, 1)
    display.text("E: Exit", x_pos, 44, gfx.DISPLAY_WIDTH, 1)
    display.update()
    
def run(consumer_id):    
    show_options(consumer_id)    
    time.sleep(1)
    
    display = gfx.display
    
    # TODO display connecting message...
    redis_client = redis.connect()
    # TODO check if we have a client...    
    
    while True:
        time.sleep(0.01)

        if gfx.gp.switch_pressed(SWITCH_A):
            # TODO
            print("A pressed")
        if gfx.gp.switch_pressed(SWITCH_E):
            return
