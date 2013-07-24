# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

from pwm.config import config
import pwm.xcb
import pwm.bar
import pwm.layouts

workspaces = []
current_workspace_index = 0


class Workspace:
    def __init__(self):
        self.active = False
        self.windows = []
        self.focused = None

        self.x = 0
        self.y = config["bar"]["height"]

        self.width = pwm.xcb.screen.width_in_pixels
        self.height = pwm.xcb.screen.height_in_pixels - self.y

        self.bar = pwm.bar.Bar(self)

        self.layout = pwm.layouts.Default(self)

    def add_window(self, window):
        window.workspace = self
        self.windows.append(window)
        self.layout.add(window)

        window.show()
        self.bar.update()

    def remove_window(self, window):
        self.windows.remove(window)
        self.layout.remove(window)

        if window == self.focused:
            self.focused = None

            if self.windows:
                self.focus(self.windows[-1])

        self.bar.update()

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

    def find_window(self, wid):
        """Searches this workspace for a window with the given wid"""

        for win in self.windows:
            if win.wid == wid:
                return win
        return None

    def focus(self, window):
        """Focuses the given window
        window=None will unfocus the current window
        """

        if window is not None and window not in self.windows:
            return

        if self.focused is not None:
            self.focused.handle_focus(False)
            self.focused = None

        if window is not None:
            self.focused = window
            self.focused.handle_focus(True)

        self.bar.update()

    def handle_property_notify(self, window):
        if window not in self.windows:
            return

        self.bar.update()


def setup():
    """Sets up initial workspace"""
    add(Workspace())
    current().show()


def destroy():
    """Destroys all workspaces"""
    global workspaces
    workspaces = []


def add(workspace):
    """Adds a new workspace"""
    workspaces.append(workspace)


def current():
    """Returns the currently active workspace"""
    return workspaces[current_workspace_index]


def find_window(wid):
    """Searches all workspaces for a window with the given wid.
    Returns (window, workspace) if found otherwise None
    """

    for ws in workspaces:
        win = ws.find_window(wid)
        if win is not None:
            return (win, ws)

    return None
