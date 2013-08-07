# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import os

from pwm.config import config
import pwm.worker
import pwm.bar
import pwm.scheduler
import pwm.config

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


@pwm.config.create_arguments
def separator(char="|", color=None):
    """Return a separator."""
    return (color, " {} ".format(char))


@pwm.config.create_arguments
def time(fmt="%Y-%m-%d %H:%M:%S", color=None):
    """Return the current time.

    If color is None the default color will be used.
    """
    import time
    return (color, time.strftime(fmt))


@pwm.config.create_arguments
def battery(bat=1, color=None):
    """Return the current battery status.

    bat is the number of the battery to check.
    If color is None the default color will be used.
    """
    path = "/sys/class/power_supply/BAT{}".format(bat)

    if not os.path.exists(path):
        return ("#ff0000", "Battery BAT{} not found".format(bat))

    with open(path+"/capacity") as f:
        capacity = f.readline().strip()

    with open(path+"/status") as f:
        status = f.readline().strip()

    output = ["BAT{}".format(bat)]

    # Status can be Discharging, Charging or Full
    if status == "Discharging":
        output.append("DIS")
    elif status == "Charging":
        output.append("CHR")

    output.append("{}%".format(capacity))

    return (color, " ".join(output))
