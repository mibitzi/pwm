# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import logging

from pwm.config import config
from pwm.ffi.xcb import xcb
#import pwm.bar
import pwm.windows
import pwm.layout
import pwm.events

workspaces = []
current_workspace_index = 0


class Workspace:
    def __init__(self):
        self.windows = []

        self.x = 0
        self.y = 0#pwm.bar.calculate_height()

        self.width = xcb.screen.width_in_pixels
        self.height = xcb.screen.height_in_pixels - self.y

        self.layout = pwm.layout.Layout(self)

    def hide(self):
        for w in self.windows:
            pwm.windows.hide(w)

    def show(self):
        for w in self.windows:
            pwm.windows.show(w)

    def add_window(self, wid):
        with pwm.windows.no_enter_notify_event():
            # Place new window below the one with the highest priority
            column = 0
            row = -1
            priority = self.top_focus_priority()
            if priority:
                column, row = self.layout.path(priority)
                row += 1

            self.windows.append(wid)
            self.layout.add_window(wid, column, row)

            if current() == self:
                pwm.windows.show(wid)

    def remove_window(self, wid):
        with pwm.windows.no_enter_notify_event():
            self.windows.remove(wid)
            self.layout.remove_window(wid)

    def top_focus_priority(self):
        """Return the window which is on top of the focus priority list.

        If there are no windows, return None.
        """
        if self.windows:
            return self.windows[-1]
        return None

    def handle_focus(self, wid):
        """Handle focus and rearrange the focus priority list accordingly."""

        if wid not in self.windows:
            return

        # Simply remove the window from the list and append it at the end.
        # This way all windows will be sorted by how recently they were
        # focused.
        self.windows.remove(wid)
        self.windows.append(wid)


def setup():
    """
    Set up all workspaces.
    """
    global workspaces
    workspaces = [Workspace() for i in range(0, config.workspaces)]

    global current_workspace_index
    current_workspace_index = 0
    current().show()


def destroy():
    """
    Destroy all workspaces.
    """

    global workspaces
    workspaces = []


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

    with pwm.windows.no_enter_notify_event():
        new_ws = workspaces[index]
        new_ws.show()
        current().hide()

    current_workspace_index = index
    pwm.windows.handle_focus(current().top_focus_priority())
    pwm.events.workspace_switched(index)


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
