from gfx_pack import SWITCH_A, SWITCH_E

import gfx
import random
import redis
import secrets
import time

def show_options(consumer_id):
    display = gfx.display
    gfx.clear_screen()
    gfx.set_backlight(0, 0, 0, 80)
    gfx.display_centered(f"CONSUMER {consumer_id}", 5, 2)
    x_pos = gfx.display_centered("A: GET NEXT JOB", 35, 1)
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
            gfx.clear_screen()
            gfx.display_centered("FETCHING JOB", 25, 2)
            display.update()
            
            response = redis_client.xreadgroup(
                "GROUP",
                secrets.REDIS_CONSUMER_GROUP,
                consumer_id,
                "COUNT",
                "1",
                "STREAMS",
                secrets.REDIS_STREAM_KEY,
                ">"
            )
            
            # response looks like:
            # [[b'jobs', [[b'1688668017967-0', [b'room', b'232', b'job', b'room_service']]]]]
            #
            # or when no jobs remain:
            # None
            
            gfx.clear_screen()
            
            if response is None:
                # Nothing to do right now.
                gfx.display_centered("NO NEW JOBS!", 25, 2)
                display.update()
                gfx.flash_backlight(5, 0, 64, 0, 0)
                gfx.set_backlight(0, 0, 0, 80)
                time.sleep(1)

            else:
                # Do the job.
                task = response[0][1][0][1]
                room = task[1].decode("utf-8")
                job = task[3].decode("utf-8")
                id = response[0][1][0][0].decode("utf-8")
                
                gfx.display_centered("DOING JOB", 5, 2)
                display.text(f"ID: {id}", 5, 25, gfx.DISPLAY_WIDTH, 1)
                display.text(f"ROOM: {room}", 5, 34, gfx.DISPLAY_WIDTH, 1)
                display.text(f"JOB: {job}", 5, 43, gfx.DISPLAY_WIDTH, 1)
                display.update()            

                bar_width = gfx.DISPLAY_WIDTH
                
                while bar_width > 0:
                    gfx.clear_rect(0, 61, gfx.DISPLAY_WIDTH, 61, 2)
                    display.line(0, 61, bar_width, 61, 2)
                    display.update()
                    bar_width = bar_width - (gfx.DISPLAY_WIDTH // 20)
                    time.sleep(0.2)
                
                # Tell Redis the job is completed.
                redis_client.xack(secrets.REDIS_STREAM_KEY, secrets.REDIS_CONSUMER_GROUP, id)
                
                gfx.clear_screen()
                gfx.display_centered("JOB DONE!", 25, 2)
                display.update()
                gfx.flash_backlight(5, 0, 64, 0, 0)
                gfx.set_backlight(0, 0, 0, 80)
                time.sleep(1)
            
            show_options(consumer_id)

        elif gfx.gp.switch_pressed(SWITCH_E):
            gfx.clear_screen()
            gfx.display_centered("DISCONNECTING FROM REDIS", 25, 1)
            display.update()
            redis_client.close()
            time.sleep(1)
            return
