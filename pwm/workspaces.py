# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import logging

from pwm.config import config
from pwm.ffi.xcb import xcb
import pwm.bar
import pwm.windows
import pwm.layout
import pwm.events

workspaces = []
current_workspace_index = 0


class Workspace:
    def __init__(self):
        self.windows = []

        self.x = 0
        self.y = pwm.bar.calculate_height()

        self.width = xcb.screen.width_in_pixels
        self.height = xcb.screen.height_in_pixels - self.y

        self.tiling = pwm.layout.Tiling(self)
        self.floating = pwm.layout.Floating(self)
        self.fullscreen = pwm.layout.Fullscreen(self)

        self.layouts = (self.tiling, self.floating, self.fullscreen)

    def hide(self):
        for w in self.windows:
            # The next UnmapNotifyEvent for this window has to be ignored
            pwm.windows.managed[w].ignore_unmaps += 1
            xcb.core.unmap_window(w)

    def show(self):
        for w in self.windows:
            xcb.core.map_window(w)

    def add_window(self, wid):
        with pwm.windows.no_enter_notify_event():
            if pwm.windows.managed[wid].fullscreen:
                self.fullscreen.add_window(wid)
            elif pwm.windows.managed[wid].floating:
                self.floating.add_window(wid)
            else:
                # Place new window below the one with the highest priority
                column = 0
                row = -1
                for priority in reversed(self.windows):
                    if not pwm.windows.managed[priority].floating:
                        column, row = self.tiling.path(priority)
                        row += 1
                        break

                self.tiling.add_window(wid, column, row)

            self.windows.append(wid)
            if current() == self:
                xcb.core.map_window(wid)

    def _proxy_layout(self, attr, wid, *args, **kwargs):
        for layout in self.layouts:
                if wid in layout.windows and hasattr(layout, attr):
                    return getattr(layout, attr)(wid, *args, **kwargs)

    def remove_window(self, wid):
        with pwm.windows.no_enter_notify_event():
            self._proxy_layout("remove_window", wid)
            self.windows.remove(wid)

    def move_window(self, wid, direction):
        with pwm.windows.no_enter_notify_event():
            self._proxy_layout("move", wid, direction)

    def resize_window(self, wid, delta):
        with pwm.windows.no_enter_notify_event():
            self._proxy_layout("resize", wid, delta)

    def focus_relative(self, wid, pos):
        """Focus the neighbour of a window."""
        rel = self._proxy_layout("relative", wid, pos)
        if rel:
            pwm.windows.focus(rel)

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

        # Simply move the window to the end of the list.
        # This way all windows will be sorted by how recently they were
        # focused.
        self.windows.remove(wid)
        self.windows.append(wid)

    def toggle_floating(self, wid):
        with pwm.windows.no_enter_notify_event():
            if pwm.windows.managed[wid].floating:
                self.floating.remove_window(wid)
                self.tiling.add_window(wid)
            else:
                self.tiling.remove_window(wid)
                self.floating.add_window(wid)

            pwm.windows.managed[wid].floating = (
                not pwm.windows.managed[wid].floating)

    def toggle_focus_layer(self):
        target = not pwm.windows.managed[pwm.windows.focused].floating

        for win in reversed(self.windows):
            if pwm.windows.managed[win].floating == target:
                pwm.windows.focus(win)
                return

    def toggle_fullscreen(self, wid):
        info = pwm.windows.managed[wid]
        if info.fullscreen:
            self.remove_fullscreen(wid)
        else:
            self.add_fullscreen(wid)

    def add_fullscreen(self, wid):
        self._proxy_layout("remove_window", wid)
        self.fullscreen.add_window(wid)

    def remove_fullscreen(self, wid):
        info = pwm.windows.managed[wid]
        self.fullscreen.remove_window(wid)
        if info.floating:
            self.floating.add_window(wid)
        else:
            self.tiling.add_window(wid)


def setup():
    """
    Set up all workspaces.
    """
    global workspaces
    workspaces = [Workspace() for i in range(config.workspaces)]

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
    pwm.windows.focus(current().top_focus_priority())
    pwm.events.workspace_switched(index)


def opened():
    """
    Return a generator which yields all open workspaces.

    yield (index, workspace)
    A workspace is considered open if it has any windows on it or if it's
    the current workspace.
    """

    for i in range(config.workspaces):
        if i == current_workspace_index or workspaces[i].windows:
            yield i, workspaces[i]


def send_window_to(wid, workspace):
    """Send the window to another workspace."""

    old_ws = pwm.windows.managed[wid].workspace
    old_ws.remove_window(wid)

    # Prevent this window from sending a UnmapNotifyEvent, then unmap it
    pwm.windows.managed[wid].ignore_unmaps += 1
    xcb.core.unmap_window(wid)

    new_ws = workspaces[workspace]
    new_ws.add_window(wid)
    pwm.windows.managed[wid].workspace = new_ws

    if current() == old_ws:
        pwm.windows.focus(old_ws.top_focus_priority())
