from gfx_pack import GfxPack, SWITCH_A, SWITCH_B, SWITCH_C, SWITCH_D, SWITCH_E

gp = GfxPack()
display = gp.display

DISPLAY_WIDTH, DISPLAY_HEIGHT = display.get_bounds()

def clear_screen():
    display.set_pen(0)
    display.clear()
    display.set_pen(15)
    
def set_backlight(r, g, b, w):
    gp.set_backlight(r, g, b, w)