# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import threading
import logging


class Scheduler:
    def __init__(self, func, interval):
        self.func = func
        self.interval = interval

        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._loop)
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def _loop(self):
        while not self.stop_event.is_set():
            try:
                self.func()
            except:
                logging.exception("Scheduler error")
            self.stop_event.wait(self.interval)
