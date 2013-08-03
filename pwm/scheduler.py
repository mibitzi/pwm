# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import time
import heapq
import threading
from collections import namedtuple
import logging


Event = namedtuple("Event", ["time", "interval", "func"])

queue = []
thread = None
stop_event = None
lock = None


def setup():
    global queue
    queue = []

    global stop_event
    stop_event = threading.Event()

    global lock
    lock = threading.Lock()

    global thread
    thread = threading.Thread(target=_loop)


def destroy():
    if thread.is_alive():
        stop_event.set()
        thread.join(2)

        if thread.is_alive():
            logging.error("Scheduler did not stop, will be killed forcefully.")

    global queue
    queue = []


def add(func, interval):
    """Add a new function to the queue.

    interval is the amount of seconds to wait before calling this function
    again.
    """
    with lock:
        heapq.heappush(queue, Event(time.monotonic()+interval, interval, func))


def remove(func):
    """Remove a function which was previously added."""
    with lock:
        global queue
        queue = [f for f in queue if f[2] != func]


def start():
    """Active the scheduler thread and start processing the event functions."""
    logging.info("Starting scheduler...")
    thread.start()


def _loop():
    while not stop_event.is_set():
        process_next()


def process_next():
    """Process the next event in the queue.

    If the time for the next event is in the future, block until that time.
    """
    event = None
    with lock:
        if not queue:
            stop_event.wait(0.5)
            return

        event = heapq.heappop(queue)

    now = time.monotonic()
    if event.time > now and stop_event.wait(event.time-now):
        return

    event.func()
    add(event.func, event.interval)
