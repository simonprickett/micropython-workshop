# Redis MicroPython Workshop with Raspberry Pi Pico W and Pimoroni GFX Pack

![Redis and Pico W Image](images/redis_picow_workshop.jpg)

This is the repository for my Redis Streams / Raspberry Pi Pico W / MicroPython workshop!

In this workshop you'll learn about Redis Streams, MicroPython, how to call an API from a Raspberry Pi Pico W and how to display text and graphics and capture user input from the GFX Pack screen.

If you don't have the hardware, you can run equivalent desktop Python scripts and still learn about Redis Streams and some cool tricks for displaying information in the terminal using the ["rich"](https://pypi.org/project/rich/) module for Python.

Interested in having me deliver this workshop for your group?  [Get in touch](https://simonprickett.dev/contact/).

## Hardware Bill of Materials

![Workshop Hardware](images/workshop_kit.png)

Each student or pair of students at the workshop should have access to a kit containing:

* [Raspberry Pi Pico W with headers pre-soldered](https://shop.pimoroni.com/products/raspberry-pi-pico-w?variant=40454061752403) (required) - £7.20.
* [Pimoroni GFX Pack](https://shop.pimoroni.com/products/pico-gfx-pack?variant=40414469062739) - a display with buttons and multi-coloured backlight (required) - £16.50.
* [USB A to micro USB data/charge cable](https://shop.pimoroni.com/products/usb-a-to-microb-cable-red?variant=32065140746) (required - use one you have already perhaps?) - £3.00.
* [Pimoroni large loot box](https://shop.pimoroni.com/products/pirate-brand-plastic-loot-box?variant=40286342922) (optional but looks cool and keeps everything organized) - £3.30.

At the time of writing one kit including all of the above costs £30.00 plus postage at Pimoroni.

The GFX pack is a great start point for a workshop like this, and can also be expanded with a Stemma/QT cable and a range of sensors or other inputs (see the "Connecting Breakouts" section [here](https://shop.pimoroni.com/products/pico-gfx-pack?variant=40414469062739)).

## Workshop Overview

TODO

## Software Prerequisites

TODO

## Starting Redis

TODO

```
XGROUP CREATE jobs staff 0 MKSTREAM
```

## Next Steps

You should now read the README files in the various folders in this repository:

* [`micropython`](micropython/README.md) - The MicroPython software that runs on the Raspberry Pi Pico W.
* [`python`](python/README.md) - Desktop Python alternatives that perform the same tasks as the MicroPython code.
* [`server`](server/README.md) - A server that displays Redis Stream overview information in a web front end, and which can also act as a fake data generator for the carbon intensity functionality in environments where connecting the Raspberry Pi Pico W to the internet is not practical (example: wifi with a [captive portal](https://en.wikipedia.org/wiki/Captive_portal)).
