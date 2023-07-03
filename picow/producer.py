from gfx_pack import SWITCH_E

import gfx
import time

def run():
    display = gfx.display

    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    
    display.text("TODO: Redis Producer", 5, 20, gfx.DISPLAY_WIDTH, 2)
    display.update()
    
    while True:
        time.sleep(0.01)
    
        if gfx.gp.switch_pressed(SWITCH_E):
            return
