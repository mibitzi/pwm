# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

from pwm.config import config
import pwm.xcb
import pwm.bar
import pwm.layouts
import pwm.events

workspaces = []
current_workspace_index = 0


class Workspace:
    def __init__(self):
        self.active = False
        self.windows = []

        self.x = 0
        self.y = config.bar.height

        self.width = pwm.xcb.screen.width_in_pixels
        self.height = pwm.xcb.screen.height_in_pixels - self.y

        self.bar = pwm.bar.Bar(self)

        self.layout = pwm.layouts.Default(self)

    def destroy(self):
        self.bar.destroy()

    def hide(self):
        self.active = False

        for w in self.windows:
            w.hide()

        self.bar.hide()

    def show(self):
        self.active = True

        for w in self.windows:
            w.show()

        self.bar.show()

    def add_window(self, window):
        self.windows.append(window)
        self.layout.add(window)
        window.show()

    def remove_window(self, window):
        self.windows.remove(window)
        self.layout.remove(window)


def setup():
    """Sets up initial workspace"""
    add(Workspace())
    current().show()


def destroy():
    """Destroys all workspaces"""

    global workspaces

    for ws in workspaces:
        ws.destroy()

    workspaces = []


def add(workspace):
    """Adds a new workspace"""
    workspaces.append(workspace)


def current():
    """Returns the currently active workspace"""
    return workspaces[current_workspace_index]
