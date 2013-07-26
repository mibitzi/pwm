# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function  # , unicode_literals

import struct
import xcb.xproto as xproto

from pwm.config import config
import pwm.xcb
import pwm.color
import pwm.workspaces
import pwm.events

# wid: (window, workspace)
windows = {}

focused = None


class Window:
    def __init__(self, wid):
        self.wid = wid
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.visible = False

        self.change_attributes(
            eventmask=(xproto.EventMask.EnterWindow |
                       xproto.EventMask.FocusChange |
                       xproto.EventMask.PropertyChange))

    def show(self):
        self.visible = True
        pwm.xcb.core.MapWindow(self.wid)

    def hide(self):
        self.visible = False
        pwm.xcb.core.UnmapWindow(self.wid)

    def change_attributes(self, **kwargs):
        mask, values = pwm.xcb.attribute_mask(**kwargs)
        pwm.xcb.core.ChangeWindowAttributes(self.wid, mask, values)

    def get_name(self):
        name = pwm.xcb.get_property_value(
            pwm.xcb.get_property(self.wid, xproto.Atom.WM_NAME).reply())

        return name or ""

    def configure(self, **kwargs):
        """Configure the window and set the given variables.

        Arguments can be: x, y, width, height
        All changes to these variables should be done by calling this method.
        """

        self.x = int(kwargs.get("x", self.x))
        self.y = int(kwargs.get("y", self.y))
        self.width = int(kwargs.get("width", self.width))
        self.height = int(kwargs.get("height", self.height))

        workspace = pwm.workspaces.current()

        mask, values = pwm.xcb.configure_mask(
            x=workspace.x + self.x,
            y=workspace.y + self.y,
            width=self.width - 2*config.window.border,
            height=self.height - 2*config.window.border,
            borderwidth=config.window.border)
        pwm.xcb.core.ConfigureWindow(self.wid, mask, values)

    def handle_focus(self, focused):
        """Set border color and input focus according to focus."""

        border = None
        if focused:
            border = pwm.color.get_pixel(config.window.focused)
        else:
            border = pwm.color.get_pixel(config.window.unfocused)

        self.change_attributes(borderpixel=border)

        if focused:
            pwm.xcb.core.SetInputFocus(xproto.InputFocus.PointerRoot,
                                       self.wid,
                                       xproto.Time.CurrentTime)


def handle_map_request(wid):
    win = Window(wid)
    ws = pwm.workspaces.current()

    ws.add_window(win)
    windows[wid] = (win, ws)


def handle_unmap_notification(win):
    _, ws = find(win.wid)
    ws.remove_window(win)
    del windows[win.wid]


def handle_focus(wid):
    """Focus the window with the given wid.

    events.focus_changed will be fired with the new focused window as
    parameter. If no window was focused or the window was not found
    the event will be fired with None as parameter.
    """

    global focused

    (win, ws) = windows.get(wid, (None, None))
    if focused == win:
        return

    if focused:
        focused.handle_focus(False)

    focused = win
    if focused:
        focused.handle_focus(True)

    pwm.events.focus_changed(win)


def find(wid):
    """Find the window with the given wid.

    Return a (window, workspace) tuple if found, otherwise (None, None).
    """

    return windows.get(wid, (None, None))


def get_wm_protocols(wid):
    """Return the protocols supported by this window."""

    return pwm.xcb.get_property_value(
        pwm.xcb.get_property(wid, "WM_PROTOCOLS").reply())


def kill(wid, kill_client=False):
    """Kill the window with wid.

    wid:         Id of the window to be killed
    kill_client: If set to True, the client will be force-fully killed with
                 xcb_kill_client.
                 Otherwise the window will be closed with xcb_destroy_window
    """

    # Check if the window supports WM_DELETE_WINDOW, otherwise kill it
    # the hard way.
    if "WM_DELETE_WINDOW" in get_wm_protocols(wid):
        vals = [
            33,  # ClientMessageEvent
            32,  # Format
            0,
            wid,
            pwm.xcb.get_atom("WM_PROTOCOLS"),
            pwm.xcb.get_atom("WM_DELETE_WINDOW"),
            xproto.Time.CurrentTime,
            0,
            0,
            0,
        ]

        event = struct.pack('BBHII5I', *vals)

        pwm.xcb.core.SendEvent(False, wid, xproto.EventMask.NoEvent, event)

    else:
        pwm.xcb.core.KillClient(wid)
