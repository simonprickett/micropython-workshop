# MicroPython Workshop: Desktop Python Alternatives

![Stream status running in the console](../images/console_demo.gif)

## Overview

This folder contains equivalent Python scripts that perform all of the functionality of the MicroPython scripts for the Raspberry Pi Pico W / GFX Pack.  Use these if you don't have access to the hardware to run the MicroPython, or mix and match and run these alongside the MicroPython if you want to add more moving parts to the Redis Stream processing system.

Each function performed by the MicroPython code has an equivalent here, each in its own Python script.  The Redis components use the [redis-py](https://github.com/redis/redis-py) client to connect to Redis.

* `producer.py`: The Redis Stream producer component.
* `consumer.py`: The Redis Stream consumer group consumer component.
* `streamstatus.py`: The Redis Stream status overview component.
* `carbonintensity.py`: The carbon intensity display component.

These have all been tested using Python 3.10 on macOS Ventura.

## Prerequisites

Before running these components you should first have started your Redis instance and configured your stream consumer group.  See the [main README](../README.md) for details.

## Setup and Configuration

Create a Python virtual environment and activate it:

```
python3 -m venv venv
. ./venv/bin/activate
```

Use `pip` to install the dependencies:

```
pip install -r requirements.txt
```

These components have a few configurable parameters.  Set these up by creating a `.env` file from the `env.example` provided:

```
cp env.example .env
```

Now edit `.env` to point to the host where your Redis instance is running.  If you're running Redis on your local machine port 6379 you can skip this section.

If you're running Redis on, for example, `192.168.4.22` port `6379`, set the line beginning `REDIS_URL` to:

```
REDIS_URL=redis://192.168.4.22:6379/?decode_responses=True
```

If your Redis server requires a password, use a Redis URL as follows, replacing `password` with your password:

```
REDIS_URL=redis://default:password@myserver.mydomain.com:6379/?decode_responses=True
```

Finally if your Redis server requires both a user and a password, use a Redis URL like this, replacing `username` and `password` with your username and password respectively:

```
REDIS_URL=redis://username:password@localhost:6379/?decode_responses=True
```

Remember to save any changes you make to the `.env` file before going any further.

## The Producer

This component periodically generates a random new job and adds it to the Redis stream.  Start it like this:

```
python producer.py
```

When you're done using this component, stop it with Ctrl-C.

## The Consumer

This component periodically completes a job assigned to it from the Redis Stream, then takes a short break.  It needs to have a unique consumer name... so use something like your own name.  Start it like this, replacing `emmagonzalez` with your own name (no spaces):

```
python consumer.py emmagonzalez
```

When you're done using this component, stop it with Ctrl-C.

## The Stream Status Component

This component shows the current state of the Redis stream - the number of consumers, number of jobs in progress and the lag.

It updates periodically. Start it like this:

```
python streamstatus.py
```

When you're done using this component, stop it with Ctrl-C.

## The Carbon Intensity Component

This component doesn't use Redis.  It demonstrates how to fetch data from a public JSON API endpoint using the Carbon Intensity API.

Start the component like this:

```
python carbonintensity.py
```

When you're done using this component, stop it with Ctrl-C.

If you are running this code in an environment where you can't access the internet, you can use the [server](../server) component to provide fake data.  To do this, start the server component (see its [README](../server/README.md) for details).  Then edit your `.env` file and replace the line:

```
CARBON_INTENSITY_URL=https://api.carbonintensity.org.uk/regional/postcode/OX1
```

With:

```
CARBON_INTENSITY_URL=http://SERVER IP ADDRESS:5000/regional/postcode/OX1
```

Note that you can also change the postcode to match your area - swap `OX1` for the first part of your postcode e.g. `DE78`.  Save your changes and re-start the component.