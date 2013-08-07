# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import os
import shutil
import subprocess
import re

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


def _format(fmt, *args, **kwargs):
    """Format and clean the string."""
    clean = fmt.format(*args, **kwargs)
    clean = re.sub("\s{2,}", " ", clean)
    return clean


def _humanize_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "{:.2f} {}".format(num, x)
        num /= 1024.0
    return "{:.2f} {}".format(num, 'TB')


@pwm.config.create_arguments
def separator(char="•", color=None):
    """Return a separator."""
    if not color:
        color = config.bar.separator
    return (color, " {} ".format(char))


@pwm.config.create_arguments
def time(fmt="%Y-%m-%d %H:%M:%S", color=None):
    """Return the current time.

    If color is None the default color will be used.
    """
    import time
    return (color, time.strftime(fmt))


@pwm.config.create_arguments
def battery(bat="BAT0", color=None, fmt="⚡ {status} {capacity}%"):
    """Return the current battery status.

    bat is the number of the battery to check.
    If color is None the default color will be used.
    """
    path = "/sys/class/power_supply/{}".format(bat)

    if not os.path.exists(path):
        return ("#ff0000", "Battery {} not found".format(bat))

    with open(path+"/capacity") as f:
        capacity = f.readline().strip()

    with open(path+"/status") as f:
        status = f.readline().strip()

    # Status can be Discharging, Charging or Full
    if status == "Discharging":
        status = "DIS"
    elif status == "Charging":
        status = "CHR"
    elif status == "Full":
        status = "FUL"
    else:
        status = ""

    return (color, _format(fmt, status=status, capacity=capacity))


@pwm.config.create_arguments
def volume(control="Master", card=0, color=None, fmt="♪ {volume}"):
    """Return the current volume."""
    out = subprocess.check_output(["amixer", "-c", str(card), "get", control],
                                  universal_newlines=True)

    match = re.search("\[(\d{0,3}%)\]", out)
    if match:
        return (color, _format(fmt, volume=match.group(1)))
    else:
        return ("#ff0000", "amixer error")


@pwm.config.create_arguments
def disk(path, color=None, fmt="{path} {free}"):
    """Return information about available disk space.

    Available formatting arguments are {free} {used} and {total}.
    """
    usage = shutil.disk_usage(path)
    return (color, _format(fmt,
                           path=path,
                           free=_humanize_bytes(usage.free),
                           total=_humanize_bytes(usage.total),
                           used=_humanize_bytes(usage.used)))


@pwm.config.create_arguments
def load(color=None):
    """Return system load."""
    return (color, " ".join("{:.2f}".format(f) for f in os.getloadavg()))
