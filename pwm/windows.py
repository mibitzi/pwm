# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function  # , unicode_literals

from contextlib import contextmanager
import struct
import xcb.xproto as xproto

from pwm.config import config
import pwm.xcb
import pwm.color
import pwm.workspaces
import pwm.events

managed = {}
focused = None
focus_history = []

MANAGED_EVENT_MASK = (xproto.EventMask.EnterWindow |
                      xproto.EventMask.FocusChange |
                      xproto.EventMask.PropertyChange)


def create(x, y, width, height):
    """Create a new window and return its id."""

    wid = pwm.xcb.conn.generate_id()

    mask, values = pwm.xcb.attribute_mask(
        backpixel=pwm.xcb.screen.black_pixel,
        eventmask=xproto.EventMask.Exposure)

    pwm.xcb.core.CreateWindow(
        pwm.xcb.screen.root_depth,
        wid,
        pwm.xcb.screen.root,
        x, y,
        width,
        height,
        0,  # border
        xproto.WindowClass.InputOutput,
        pwm.xcb.screen.root_visual,
        mask, values)

    return wid


def destroy(wid):
    """Destroy the window."""
    pwm.xcb.core.DestroyWindow(wid)


def manage(wid):
    if wid in managed:
        return

    change_attributes(wid, eventmask=MANAGED_EVENT_MASK)

    managed[wid] = pwm.workspaces.current()
    pwm.workspaces.current().add_window(wid)

    handle_focus(wid)


def unmanage(wid):
    if wid not in managed:
        return

    ws = managed[wid]
    ws.remove_window(wid)
    del managed[wid]

    global focus_history
    focus_history = [w for w in focus_history if w != wid]

    if focused == wid:
        if focus_history:
            handle_focus(focus_history.pop())


def show(wid):
    """Map the given window."""
    pwm.xcb.core.MapWindow(wid)


def hide(wid):
    """Unmap the given window."""
    pwm.xcb.core.UnmapWindow(wid)


def is_mapped(wid):
    """Return True if the window is mapped, otherwise False."""
    attr = pwm.xcb.core.GetWindowAttributes(wid).reply()
    return attr.map_state == xproto.MapState.Viewable


def change_attributes(wid, **kwargs):
    """Set attributes for the given window."""

    mask, values = pwm.xcb.attribute_mask(**kwargs)
    pwm.xcb.core.ChangeWindowAttributes(wid, mask, values)


def get_name(wid):
    """Get the window name."""

    name = pwm.xcb.get_property_value(
        pwm.xcb.get_property(wid, xproto.Atom.WM_NAME).reply())

    return name or ""


def configure(wid, **kwargs):
    """Configure the window and set the given variables.

    Arguments can be: x, y, width, height
    """

    workspace = pwm.workspaces.current()

    if "x" in kwargs:
        kwargs["x"] = int(workspace.x + kwargs["x"])
    if "y" in kwargs:
        kwargs["y"] = int(workspace.y + kwargs["y"])

    if "width" in kwargs:
        kwargs["width"] = int(kwargs["width"] - 2*config.window.border)
    if "height" in kwargs:
        kwargs["height"] = int(kwargs["height"] - 2*config.window.border)

    kwargs["borderwidth"] = config.window.border

    mask, values = pwm.xcb.configure_mask(**kwargs)
    pwm.xcb.core.ConfigureWindow(wid, mask, values)


def get_geometry(wid):
    """Get geometry information for the given window.

    Return a tuple(x, y, width, height).
    """

    geo = pwm.xcb.core.GetGeometry(wid).reply()
    return (geo.x, geo.y, geo.width, geo.height)


def get_wm_protocols(wid):
    """Return the protocols supported by this window."""

    return pwm.xcb.get_property_value(
        pwm.xcb.get_property(wid, "WM_PROTOCOLS").reply())


def kill(wid):
    """Kill the window with wid."""

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


def handle_focus(wid):
    """Focus the window with the given wid.

    events.focus_changed will be fired with the new focused window as
    parameter. If no window was focused or the window was not found
    the event will be fired with None as parameter.
    """

    global focused

    win = wid if wid in managed else None

    if focused == win:
        return

    if focused:
        _handle_focus(focused, False)

    focused = win
    if focused:
        _handle_focus(focused, True)

    pwm.events.focus_changed(win)


def _handle_focus(wid, focused):
    """Set border color and input focus according to focus."""

    border = None
    if focused:
        border = pwm.color.get_pixel(config.window.focused)
    else:
        border = pwm.color.get_pixel(config.window.unfocused)

    change_attributes(wid, borderpixel=border)

    if focused:
        pwm.xcb.core.SetInputFocus(xproto.InputFocus.PointerRoot,
                                   wid,
                                   xproto.Time.CurrentTime)

        global focus_history
        focus_history.append(wid)


@contextmanager
def no_enter_notify_event():
    """Prevent all managed windows from sending EnterNotifyEvent."""

    eventmask = MANAGED_EVENT_MASK
    eventmask &= ~xproto.EventMask.EnterWindow

    for wid in managed:
        change_attributes(wid, eventmask=eventmask)

    yield

    for wid in managed:
        change_attributes(wid, eventmask=MANAGED_EVENT_MASK)
