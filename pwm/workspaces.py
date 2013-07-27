# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import logging

from pwm.config import config
import pwm.xcb
import pwm.bar
import pwm.windows
import pwm.layouts
import pwm.events

workspaces = []
current_workspace_index = 0
bar = None


class Workspace:
    def __init__(self):
        self.windows = []

        self.x = 0
        self.y = pwm.bar.height()

        self.width = pwm.xcb.screen.width_in_pixels
        self.height = pwm.xcb.screen.height_in_pixels - self.y

        self.layout = pwm.layouts.Default(self)

    def hide(self):
        for w in self.windows:
            pwm.windows.hide(w)

    def show(self):
        for w in self.windows:
            pwm.windows.show(w)

    def add_window(self, wid):
        with pwm.windows.no_enter_notify_event():
            self.windows.append(wid)
            self.layout.add(wid)
            pwm.windows.show(wid)

    def remove_window(self, wid):
        with pwm.windows.no_enter_notify_event():
            self.windows.remove(wid)
            self.layout.remove(wid)


def setup():
    """
    Set up all workspaces.
    """
    global workspaces
    workspaces = [Workspace() for i in range(0, config.workspaces)]

    global current_workspace_index
    current_workspace_index = 0
    current().show()

    global bar
    bar = pwm.bar.Bar()
    bar.show()


def destroy():
    """
    Destroy all workspaces.
    """

    global workspaces
    workspaces = []

    global bar
    if bar:
        bar.destroy()
        bar = None


def current():
    """
    Return the currently active workspace.
    """
    return workspaces[current_workspace_index]


def switch(index):
    """
    Switch to workspace at given index.
    """
    global current_workspace_index
    if current_workspace_index == index:
        return

    logging.debug("Switching to workspace {}".format(index))

    new_ws = workspaces[index]
    new_ws.show()

    current().hide()

    current_workspace_index = index

    bar.update()


def opened():
    """
    Return a generator which yields all open workspaces.

    yield (index, workspace)
    A workspace is considered open if it has any windows on it or if it's
    the current workspace.
    """

    for i in range(0, config.workspaces):
        if i == current_workspace_index or workspaces[i].windows:
            yield i, workspaces[i]
