# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import pwm.xcb
import pwm.bar
import pwm.layouts

workspaces = []
current_workspace_index = 0


class Workspace:
    def __init__(self):
        self.windows = set([])
        self.focused = None

        self.bar = pwm.bar.Bar()

        self.x = 0
        self.y = self.bar.height

        self.width = pwm.xcb.screen.width_in_pixels
        self.height = pwm.xcb.screen.height_in_pixels - self.bar.height

        self.layout = pwm.layouts.Default(self)

    def add_window(self, window):
        window.workspace = self
        self.windows.add(window)
        self.layout.add(window)
        window.show()

    def remove_window(self, window):
        self.windows.remove(window)
        self.layout.remove(window)

    def hide(self):
        for w in self.windows:
            w.hide()

    def show(self):
        for w in self.windows:
            w.show()

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


def setup():
    """Sets up initial workspace"""
    add(Workspace())


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

    for wspace in workspaces:
        win = wspace.find_window(wid)
        if win is not None:
            return (win, wspace)

    return None
