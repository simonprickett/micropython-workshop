from gfx_pack import SWITCH_A, SWITCH_E

import gfx
import random
import redis
import secrets
import time

def show_options():
    display = gfx.display
    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    gfx.display_centered("PRODUCER", 5, 2)
    x_pos = gfx.display_centered("A: CREATE JOB", 35, 1)
    display.text("E: Exit", x_pos, 44, gfx.DISPLAY_WIDTH, 1)
    display.update()
    
def run():
    JOB_TYPES = [
        "cleaning",
        "room_service",
        "taxi",
        "extra_towels",
        "extra_pillows"
    ]
    
    
    display = gfx.display
    
    gfx.clear_screen()
    gfx.display_centered("CONNECTING TO REDIS", 25, 1)
    display.update()
    
    redis_client = redis.connect()
    # TODO check if we have a client... and show an error if not.
    
    gfx.clear_screen()
    gfx.display_centered("CONNECTED TO REDIS", 25, 1)
    display.update()
    time.sleep(1)
    
    show_options()
    
    while True:
        time.sleep(0.01)
    
        if gfx.gp.switch_pressed(SWITCH_A):
            room = random.randint(100, 500)
            job = random.choice(JOB_TYPES)
            
            gfx.clear_screen()
            gfx.display_centered("NEW JOB", 5, 2)
            display.text(f"ROOM: {room}", 5, 25, gfx.DISPLAY_WIDTH, 1)
            display.text(f"JOB: {job}", 5, 34, gfx.DISPLAY_WIDTH, 1)
            display.update()
                        
            job_id = redis_client.xadd(
                secrets.REDIS_STREAM_KEY,
                "*",
                "room",
                room,
                "job",
                job
            )
            
            display.text(f"ID: {job_id.decode('utf-8')}", 5, 43, gfx.DISPLAY_WIDTH, 1)
            display.update()
            
            gfx.flash_backlight(5, 0, 64, 0, 0)
            gfx.set_backlight(0, 0, 0, 80)
            
            # Wait a little bit before allowing the creation of the next job.
            bar_width = gfx.DISPLAY_WIDTH
                
            while bar_width > 0:
                gfx.clear_rect(0, 61, gfx.DISPLAY_WIDTH, 61, 2)
                display.line(0, 61, bar_width, 61, 2)
                display.update()
                bar_width = bar_width - (gfx.DISPLAY_WIDTH // 20)
                time.sleep(0.2)
                
            show_options()
        elif gfx.gp.switch_pressed(SWITCH_E):
            gfx.clear_screen()
            gfx.display_centered("DISCONNECTING FROM REDIS", 25, 1)
            display.update()
            redis_client.close()
            time.sleep(1)
            return
