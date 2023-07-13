from gfx_pack import SWITCH_E

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
    response = redis_client.xinfo(
        "GROUPS",
        secrets.REDIS_STREAM_KEY
    )
    
    # Response includes all possible consumer groups so need to find the
    # one we are interested in (secrets.REDIS_CONSUMER_GROUP).  It looks like
    # this:
    # [[b'name', b'staff', b'consumers', 1, b'pending', 3, b'last-delivered-id', b'1688993636634-0', b'entries-read', 11, b'lag', 0]]
    
    if response is None:
        # TODO error case
        pass
    else:
        found_it = False
        for consumer_group in response:
            if consumer_group[1].decode("utf-8") == secrets.REDIS_CONSUMER_GROUP:
                # Found our consumer group.
                consumers_in_group = consumer_group[3]
                jobs_in_progress = consumer_group[5]
                consumer_lag = consumer_group[11]
                
                print(consumers_in_group)
                print(jobs_in_progress)
                print(consumer_lag)
                
                found_it = True
                
                gfx.clear_screen()
                # TODO set colour by lag...
                gfx.set_backlight(0, 0, 0, 80)
                gfx.display_centered("STATUS", 5, 2)
                display.text(f"CONSUMERS: {consumers_in_group}", 5, 22, gfx.DISPLAY_WIDTH, 1)
                display.text(f"IN PROGRESS: {jobs_in_progress}", 5, 32, gfx.DISPLAY_WIDTH, 1)
                display.text(f"LAG: {consumer_lag}", 5, 42, gfx.DISPLAY_WIDTH, 1)
                gfx.display_centered("E: EXIT", 55, 1)
                display.update()
        
        if not found_it:
            # TODO consumer group didn't exist!
            pass
        
def run():
    global redis_client
    
    display = gfx.display

    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    
    # TODO display connecting message...
    redis_client = redis.connect()
    # TODO check if we have a client...

    refresh_stream_status_display()
    last_updated = time.ticks_ms()
    
    while True:
        time.sleep(0.01)
        
        if gfx.gp.switch_pressed(SWITCH_E):
            # TODO dispay disconnecting message
            redis_client.close()
            return
            
        ticks_now = time.ticks_ms()
        if time.ticks_diff(ticks_now, last_updated) > secrets.REDIS_STREAM_UPDATE_FREQUENCY * 1000:
            refresh_stream_status_display()
            last_updated = time.ticks_ms()    
    