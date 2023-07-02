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
display.text("Starting up...", 5, 25, gfx.DISPLAY_WIDTH, 2)
display.update()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

n = 0
while not wlan.isconnected() and wlan.status() >= 0:
    gfx.clear_screen()
    display.text(f"Connecting {SPINNER_CHARS[n]}", 6, 25, gfx.DISPLAY_WIDTH, 2)
    display.update()
    
    n = n + 1 if n < len(SPINNER_CHARS) - 1 else 0
    
    time.sleep(0.2)
    
gfx.clear_screen()
# TODO deal with sad path stuff... https://docs.micropython.org/en/latest/library/network.WLAN.html
# sort out these extra params - wordwrap & scale
display.text("Connected!", 15, 20, gfx.DISPLAY_WIDTH, 2)
ip_address = wlan.ifconfig()[0]
display.text(ip_address, 12, 35, gfx.DISPLAY_WIDTH, 2)
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
        carbonintensity.display_intensity_info()
    elif gfx.gp.switch_pressed(SWITCH_E):
        print("E pressed")
        
    time.sleep(0.01)
    