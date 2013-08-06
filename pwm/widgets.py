# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from pwm.config import config
import pwm.worker
import pwm.bar
import pwm.scheduler

output = []
scheduler = None


def start():
    global scheduler
    scheduler = pwm.scheduler.Scheduler(_update, config.bar.interval)
    scheduler.start()


def destroy():
    global scheduler
    scheduler.stop()
    scheduler = None


def _update():
    _call_widgets(config.bar.widgets)
    pwm.worker.tasks.put(pwm.bar.primary.update)


def _call_widgets(widgets):
    global output
    output = []

    for func in widgets:
        output.append(func())


def time(fmt="%Y-%m-%d %H:%M:%S", color=None):
    import time
    return (color, time.strftime(fmt))
