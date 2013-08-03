# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

from pwm.ffi.xcb import xcb
import pwm.xcbutil
import pwm.bar
import pwm.workspaces

connected = False
created_windows = []


def setup():
    # To increase test speed we only want to connect once
    global connected
    if not connected:
        xcb.connect()
        pwm.xcbutil.setup_root_window()
        connected = True

    pwm.workspaces.setup()
    pwm.bar.setup()


def tear_down():
    destroy_created_windows()
    pwm.bar.destroy()
    pwm.workspaces.destroy()


def create_window(manage=True):
    """Create a new window and manage it."""

    wid = pwm.windows.create(0, 0, 100, 100)

    if manage:
        pwm.windows.manage(wid)

    global created_windows
    created_windows.append((wid, manage))

    return wid


def destroy_created_windows():
    """Destroy all created windows.

    This function will be called during tear_down().
    """
    global created_windows
    for wid, managed in created_windows:
        if managed:
            pwm.windows.unmanage(wid)
        pwm.windows.destroy(wid)
    created_windows = []
