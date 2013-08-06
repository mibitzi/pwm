# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT


from queue import Queue
import threading


tasks = Queue()
shutdown = threading.Event()


def process_tasks():
    while not shutdown.is_set():
        work = tasks.get()
        work()
        tasks.task_done()
