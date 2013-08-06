# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from queue import Queue
import threading
import logging

tasks = Queue()
_thread = None


class ExitWorker(Exception):
    pass


def start():
    global _thread
    _thread = threading.Thread(target=_loop)
    _thread.daemon = True
    _thread.start()


def destroy():
    tasks.put(ExitWorker)
    _thread.join()


def _loop():
    while True:
        try:
            work = tasks.get()
            if work is ExitWorker:
                raise ExitWorker()
            work()
            tasks.task_done()
        except ExitWorker:
            break
        except:
            logging.exception("Worker task error")
