# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import pwm.xcb
import pwm.workspaces

connected = False
created_windows = []


def setup():
    # To increase test speed we only want to connect once
    global connected
    if not connected:
        pwm.xcb.connect()
        pwm.xcb.setup_root_window()
        connected = True

    pwm.workspaces.setup()


def tear_down():
    global created_windows
    for wid in created_windows:
        pwm.windows.unmanage(wid)
        pwm.windows.destroy(wid)
    created_windows = []

    pwm.workspaces.destroy()


def create_window():
    """Create a new window and manage it."""

    wid = pwm.windows.create(0, 0, 100, 100)
    pwm.windows.manage(wid)

    global created_windows
    created_windows.append(wid)

    return wid
