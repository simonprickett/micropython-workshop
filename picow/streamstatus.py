from gfx_pack import SWITCH_E
from picoredis import RedisError

import gfx
import redis
import secrets
import time

redis_client = None

def refresh_stream_status_display():
    global redis_client

    display = gfx.display

    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    
    gfx.display_centered("UPDATING...", 25, 2)
    display.update()

    # Get consumer group status information...
    # XINFO GROUPS key
    try:
        response = redis_client.xinfo(
            "GROUPS",
            secrets.REDIS_STREAM_KEY
        )
    
        # Response includes all possible consumer groups so need to find the
        # one we are interested in (secrets.REDIS_CONSUMER_GROUP).  It looks like
        # this:
        # [[b'name', b'staff', b'consumers', 1, b'pending', 3, b'last-delivered-id', b'1688993636634-0', b'entries-read', 11, b'lag', 0]]
    
        found_it = False
        for consumer_group in response:
            if consumer_group[1].decode("utf-8") == secrets.REDIS_CONSUMER_GROUP:
                # Found our consumer group.
                consumers_in_group = consumer_group[3]
                jobs_in_progress = consumer_group[5]
                consumer_lag = consumer_group[11]
                
                found_it = True
                
                gfx.clear_screen()
                
                # Set backlight colour according to stream lag...
                if consumer_lag < 3:
                    gfx.set_backlight(0, 64, 0, 0)
                elif consumer_lag < 6:
                    gfx.set_backlight(128, 64, 0, 0)
                elif consumer_lag < 9:
                    gfx.set_backlight(128, 16, 0, 0)
                else:
                    gfx.set_backlight(128, 0, 0, 0)

                gfx.display_centered("STATUS", 5, 2)
                display.text(f"CONSUMERS: {consumers_in_group}", 5, 22, gfx.DISPLAY_WIDTH, 1)
                display.text(f"IN PROGRESS: {jobs_in_progress}", 5, 32, gfx.DISPLAY_WIDTH, 1)
                display.text(f"LAG: {consumer_lag}", 5, 42, gfx.DISPLAY_WIDTH, 1)
                gfx.display_centered("E: EXIT", 51, 1)
                display.update()
        
        if not found_it:
            gfx.clear_screen()
            gfx.display_centered(f"NO GROUP \"{secrets.REDIS_CONSUMER_GROUP}\"", 25, 1)
            gfx.display_centered("E: EXIT", 51, 1)
            display.update()
            gfx.flash_backlight(5, 128, 0, 0, 0)
            gfx.set_backlight(0, 0, 0, 80)
            
    except RedisError:
        gfx.clear_screen()
        gfx.display_centered(f"NO STREAM \"{secrets.REDIS_STREAM_KEY}\"?", 25, 1)
        gfx.display_centered("E: EXIT", 51, 1)
        display.update()
        gfx.flash_backlight(5, 128, 0, 0, 0)
        gfx.set_backlight(0, 0, 0, 80)
        
def run():
    global redis_client
    
    display = gfx.display

    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    
    gfx.clear_screen()
    gfx.display_centered("CONNECTING TO REDIS", 25, 1)
    display.update()

    redis_client = redis.connect()
    
    gfx.clear_screen()

    if (redis_client is None):
        gfx.display_centered("REDIS CONNECTION ERROR", 25, 1)
        display.update()
        gfx.flash_backlight(5, 128, 0, 0, 0)
        return
    
    gfx.display_centered("CONNECTED TO REDIS", 25, 1)
    display.update()
    gfx.flash_backlight(5, 0, 64, 0, 0)
    gfx.set_backlight(0, 0, 0, 80)

    refresh_stream_status_display()
    last_updated = time.ticks_ms()
    ticks_before = last_updated
    bar_width = gfx.DISPLAY_WIDTH
    BAR_UPDATE_FREQUENCY = 200
    
    while True:
        time.sleep(0.01)
        
        if gfx.gp.switch_pressed(SWITCH_E):
            gfx.set_backlight(0, 0, 0, 80)
            gfx.clear_screen()
            gfx.display_centered("DISCONNECTING FROM REDIS", 25, 1)
            display.update()
            redis_client.close()
            time.sleep(1)
            return
            
        ticks_now = time.ticks_ms()
        
        if time.ticks_diff(ticks_now, ticks_before) > BAR_UPDATE_FREQUENCY:
            bar_width = bar_width - (gfx.DISPLAY_WIDTH // (secrets.REDIS_STREAM_UPDATE_FREQUENCY * 5))
            ticks_before = time.ticks_ms()
            
        if time.ticks_diff(ticks_now, last_updated) > secrets.REDIS_STREAM_UPDATE_FREQUENCY * 1000:
            refresh_stream_status_display()
            last_updated = time.ticks_ms()
            bar_width = gfx.DISPLAY_WIDTH
            
        gfx.clear_rect(0, 61, gfx.DISPLAY_WIDTH, 61, 2)
        display.line(0, 61, bar_width, 61, 2)
        display.update()
    