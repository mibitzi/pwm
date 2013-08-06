# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from queue import Queue
import threading
import logging

tasks = Queue()
shutdown = threading.Event()


def process_tasks():
    while not shutdown.is_set():
        try:
            work = tasks.get()
            work()
            tasks.task_done()
        except (KeyboardInterrupt, SystemExit):
            shutdown.set()
            break
        except:
            logging.exception("Worker task error")
