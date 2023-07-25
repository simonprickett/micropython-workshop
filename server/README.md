# MicroPython Workshop: Server Component

![Server running in a browser](../images/server_demo.gif)


## Overview

This folder contains the Python code for the server component.  It is written with the [Flask framework](https://flask.palletsprojects.com/), talks to Redis using the [redis-py](https://github.com/redis/redis-py) client and provides a web front end that performs the following functions:

* Displays the current state of the stream consumer group (number of consumers, number of jobs currently in progress, processing lag).
* Refreshes automatically every few seconds.
* Provides fake randomized JSON data for the Carbon Intensity demo when the internet is not available at the workshop location.

This has been tested using Python 3.10 on macOS Ventura.

## Prerequisites

Before starting the server you should first have started your Redis instance and configured your stream consumer group.  See the [main README](../README.md) for details.

## Setup and Configuration

Create a Python virtual environment and activate it:

```
python3 -m venv venv
. ./venv/bin/activte
```

Use `pip` to install the dependencies:

```
pip install -r requirements.txt
```

This component has a few configurable parameters.  Set these up by creating a `.env` file from the `env.example` provided:

```
cp env.example .env
```

Now edit `.env` to point to the host where your Redis instance is running.  For example if you're running on `192.168.4.22` port `6379`, set the line beginning `REDIS_URL` to:

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

## Starting the Server

Start the server like this:

```
flask run --host=0.0.0.0
```

The server should start up, attach to port 5000 and display output similar to the following:

```
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.4.24:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 127-179-123
```

## Using the Server

With the server running, point your browser at `http://127.0.0.1:5000/`.  You should see the current state of the Redis stream displayed, and a progress bar that counts down until the next update.

Click on the "Carbon Intensity Data" button to see randomized sample data for the carbon intensity view on the Pi Pico W component.  This is used when the workshop is taking place somewhere that the Pi Pico W devices can't connect to the internet (e.g. because a [captive portal wifi system](https://en.wikipedia.org/wiki/Captive_portal) is in place).

## Stopping the Server

Stop the server by pressing Ctrl-C in the terminal that you started it from.