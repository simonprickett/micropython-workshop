from gfx_pack import GfxPack, SWITCH_A, SWITCH_B, SWITCH_C, SWITCH_D, SWITCH_E
import time

gp = GfxPack()
display = gp.display

DISPLAY_WIDTH, DISPLAY_HEIGHT = display.get_bounds()

def clear_screen():
    display.set_pen(0)
    display.clear()
    display.set_pen(15)
    
def clear_rect(start_x, start_y, end_x, end_y, height):
    display.set_pen(0)
    display.line(start_x, start_y, end_x, end_y, height)
    display.set_pen(15)
    display.update()
    
def set_backlight(r, g, b, w):
    gp.set_backlight(r, g, b, w)
    
def display_centered(text_to_display, y_pos, scale):
    width = display.measure_text(text_to_display, scale)
    x_pos = (DISPLAY_WIDTH - width) // 2
    display.text(text_to_display, x_pos, y_pos, DISPLAY_WIDTH, scale)
    return x_pos

def flash_backlight(how_many, r, g, b, w):
    for _ in range(how_many):
        gp.set_backlight(r, g, b, w)
        time.sleep(0.2)
        gp.set_backlight(0, 0, 0, 0)
        time.sleep(0.2)