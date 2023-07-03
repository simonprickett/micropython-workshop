from gfx_pack import SWITCH_A, SWITCH_B, SWITCH_C, SWITCH_D, SWITCH_E
import carbonintensity
import gfx
import network
import secrets
import time

SPINNER_CHARS = [ "\\", "|", "/", "-" ]

display = gfx.display

display.set_font("bitmap_8")
    
gfx.clear_screen()
gfx.set_backlight(128, 16, 0, 0)
gfx.display_centered("Starting up!", 25, 2)
display.update()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

n = 0
while not wlan.isconnected() and wlan.status() >= 0:
    gfx.clear_screen()
    display.text(f"Connecting {SPINNER_CHARS[n]}", 2, 25, gfx.DISPLAY_WIDTH, 2)
    display.update()
    
    n = n + 1 if n < len(SPINNER_CHARS) - 1 else 0
    
    time.sleep(0.2)
    
gfx.clear_screen()
# TODO deal with sad path stuff... https://docs.micropython.org/en/latest/library/network.WLAN.html
# sort out these extra params - wordwrap & scale
gfx.display_centered("Connected!", 1, 2)
ip_address = wlan.ifconfig()[0]
gfx.display_centered(ip_address, 16, 2)
x_pos = gfx.display_centered("A - Redis Producer", 31, 1)
display.text("B - Redis Consumer", x_pos, 40, gfx.DISPLAY_WIDTH, 1)
display.text("C - Stream Status", x_pos, 49, gfx.DISPLAY_WIDTH, 1)
display.text("D - Energy Mix", x_pos, 58, gfx.DISPLAY_WIDTH, 1)
display.update()

for _ in range(5):
    gfx.set_backlight(0, 64, 0, 0)
    time.sleep(0.2)
    gfx.set_backlight(0, 0, 0, 0)
    time.sleep(0.2)

gfx.set_backlight(0, 0, 0, 80)

while True:
    if gfx.gp.switch_pressed(SWITCH_A):
        print("A pressed")
    elif gfx.gp.switch_pressed(SWITCH_B):
        print("B pressed")
    elif gfx.gp.switch_pressed(SWITCH_C):
        print("C pressed")
    elif gfx.gp.switch_pressed(SWITCH_D):
        print("D pressed")
        carbonintensity.run()
    elif gfx.gp.switch_pressed(SWITCH_E):
        print("E pressed")
        
    time.sleep(0.01)
    