# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from contextlib import contextmanager
from functools import wraps
from collections import defaultdict
import struct

from pwm.ffi.xcb import xcb
from pwm.config import config
import pwm.xutil
import pwm.events
import pwm.workspaces
import pwm.color
import pwm.match


managed = {}
focused = None
properties = defaultdict(dict)
geometry = {}


# Some UnmapNotifyEvents, like those generated when switching workspaces have
# to be ignored. Every window has a key in ignore_unmaps with a value
# indicating how many future UnmapNotifyEvents have to be ignored.
ignore_unmaps = defaultdict(int)

MANAGED_EVENT_MASK = (xcb.EVENT_MASK_ENTER_WINDOW |
                      xcb.EVENT_MASK_FOCUS_CHANGE |
                      xcb.EVENT_MASK_PROPERTY_CHANGE)


def create(x, y, width, height, mask=None):
    """Create a new window and return its id."""

    wid = xcb.core.generate_id()

    if not mask:
        mask = xcb.mask([(xcb.CW_BACK_PIXEL, xcb.screen.black_pixel),
                         (xcb.CW_EVENT_MASK, xcb.EVENT_MASK_EXPOSURE)])

    xcb.core.create_window(
        xcb.screen.root_depth,
        wid,
        xcb.screen.root,
        x, y,
        width,
        height,
        0,  # border
        xcb.WINDOW_CLASS_INPUT_OUTPUT,
        xcb.screen.root_visual,
        *mask)

    return wid


def destroy(wid):
    """Destroy the window."""
    xcb.core.destroy_window(wid)


def manage(wid, only_if_mapped=False):
    if wid in managed:
        return

    attr = xcb.core.get_window_attributes(wid).reply()

    if only_if_mapped and attr.map_state != xcb.MAP_STATE_VIEWABLE:
        return

    # Don't manage windows with the override_redirect flag.
    if attr.override_redirect:
        return

    update_properties(wid)
    update_geometry(wid)

    change_attributes(wid, [(xcb.CW_EVENT_MASK, MANAGED_EVENT_MASK)])

    pwm.workspaces.current().add_window(wid)
    ignore_unmaps[wid] = 0
    managed[wid] = pwm.workspaces.current()

    focus(wid)


def unmanage(wid):
    if wid not in managed:
        return

    ws = managed[wid]
    ws.remove_window(wid)
    if wid in ignore_unmaps:
        del ignore_unmaps[wid]
    del managed[wid]
    del properties[wid]
    del geometry[wid]

    if focused == wid:
        focus(pwm.workspaces.current().top_focus_priority())


def manage_existing():
    """Go through all existing windows and manage them."""

    # Get the tree of windows whose parent is the root window (= all)
    reply = xcb.core.query_tree(xcb.screen.root).reply()
    children = xcb.query_tree_children(reply)

    for i in range(xcb.query_tree_children_length(reply)):
        manage(children[i], True)


def should_float(wid):
    """Try to determine if a window should be placed on the floating layer."""

    if pwm.match.floating(wid):
        return True

    # Check the _NET_WM_WINDOW_TYPE property to determine the type of this
    # window.
    # See the specification for more info:
    # http://standards.freedesktop.org/wm-spec/wm-spec-latest.html

    wintype = pwm.xutil.get_property_reply_value(wid, "_NET_WM_WINDOW_TYPE")

    if not wintype:
        return False

    for wt in wintype:
        if (wt == pwm.xutil.get_atom("_NET_WM_WINDOW_TYPE_DIALOG") or
                wt == pwm.xutil.get_atom("_NET_WM_WINDOW_TYPE_UTILITY") or
                wt == pwm.xutil.get_atom("_NET_WM_WINDOW_TYPE_TOOLBAR") or
                wt == pwm.xutil.get_atom("_NET_WM_WINDOW_TYPE_SPLASH")):

            return True

    return False


def update_properties(wid):
    normal_hints = pwm.xutil.get_wm_normal_hints(wid)
    properties[wid]["normal_hints"] = normal_hints


def update_geometry(wid):
    # We only want the geometry if this window is floating
    if wid not in managed or wid in managed[wid].floating.windows:
        geometry[wid] = get_geometry(wid)


def is_mapped(wid):
    """Return True if the window is mapped, otherwise False."""
    attr = xcb.core.get_window_attributes(wid).reply()
    return attr.map_state == xcb.MAP_STATE_VIEWABLE


def change_attributes(wid, masks):
    """Set attributes for the given window."""
    xcb.core.change_window_attributes(wid, *xcb.mask(masks))


def get_name(wid):
    """Get the window name."""

    name = pwm.xutil.get_property_reply_value(wid, "_NET_WM_NAME")

    if not name:
        name = pwm.xutil.get_property_reply_value(wid, xcb.ATOM_WM_NAME)

    return name or ""


def get_wm_class(wid):
    return pwm.xutil.get_property_reply_value(wid, "WM_CLASS")


def get_wm_window_role(wid):
    return pwm.xutil.get_property_reply_value(wid, "WM_WINDOW_ROLE")


def get_wm_protocols(wid):
    """Return the protocols supported by this window."""
    return pwm.xutil.get_property_reply_value(wid, "WM_PROTOCOLS")


def configure(wid, **kwargs):
    """Configure the window and set the given variables in relation to the
    workspace.

    Arguments can be: x, y, width, height, stackmode
    """

    workspace = pwm.workspaces.current()
    values = [(xcb.CONFIG_WINDOW_BORDER_WIDTH, config.window.border)]

    # We need to cast x and y in order to have correct handling for negative
    # values.
    if "x" in kwargs:
        values.append(
            (xcb.CONFIG_WINDOW_X,
             xcb.ffi.cast("uint32_t", int(workspace.x + kwargs["x"]))))
    if "y" in kwargs:
        values.append(
            (xcb.CONFIG_WINDOW_Y,
             xcb.ffi.cast("uint32_t", int(workspace.y + kwargs["y"]))))

    if "width" in kwargs:
        values.append((xcb.CONFIG_WINDOW_WIDTH,
                       int(kwargs["width"] - 2*config.window.border)))
    if "height" in kwargs:
        values.append((xcb.CONFIG_WINDOW_HEIGHT,
                       int(kwargs["height"] - 2*config.window.border)))

    if "stackmode" in kwargs:
        values.append((xcb.CONFIG_WINDOW_STACK_MODE, kwargs["stackmode"]))

    xcb.core.configure_window(wid, *xcb.mask(values))
    update_geometry(wid)


def get_absolute_geometry(wid):
    """Get geometry information for the given window.

    Return a tuple(x, y, width, height).
    """

    geo = xcb.core.get_geometry(wid).reply()
    return (geo.x, geo.y, geo.width, geo.height)


def get_geometry(wid):
    """Get geometry information for the given window.

    Return a tuple(x, y, width, height).
    """

    ws = pwm.workspaces.current()
    geo = xcb.core.get_geometry(wid).reply()
    return (geo.x-ws.x, geo.y-ws.y, geo.width, geo.height)


def preferred_geometry(wid, workspace=None):
    """Return the preferd geometry for this window."""

    if not workspace:
        workspace = pwm.workspaces.current()

    hints = properties[wid]["normal_hints"]
    width, height = 0, 0
    x, y = 0, 0
    geo = geometry[wid]

    if hints.flags & xcb.ICCCM_SIZE_HINT_US_SIZE:
        width, height = hints.width, hints.height
    else:
        _, _, width, height = geo

    if (hints.flags & xcb.ICCCM_SIZE_HINT_US_POSITION or
            hints.flags & xcb.ICCCM_SIZE_HINT_P_POSITION):
        x, y = hints.x, hints.y
    else:
        x, y, _, _ = geo

    width = max(10, width)
    height = max(10, height)

    if x <= 0 or x >= workspace.width - width:
        x = (workspace.width - width) / 2
    if y <= 0 or y >= workspace.height - height:
        y = (workspace.height - height) / 2

    return x, y, width, height


def create_client_message(wid, atom, *data):
    vals = [
        xcb.CLIENT_MESSAGE,
        32,  # Format
        0,  # Sequence
        wid,
        atom
    ]

    # Every X11 event is 32 bytes long, of which 20 bytes (5 ints) are data.
    # We need to fill up the bytes which *data did not use with zeros.
    for i in range(5):
        vals.append(data[i] if i < len(data) else 0)

    return struct.pack("BBHII5I", *vals)


def kill(wid):
    """Kill the window with wid."""

    # Check if the window supports WM_DELETE_WINDOW, otherwise kill it
    # the hard way.
    atom = pwm.xutil.get_atom("WM_DELETE_WINDOW")
    if atom in get_wm_protocols(wid):
        event = create_client_message(
            wid,
            pwm.xutil.get_atom("WM_PROTOCOLS"),
            atom,
            xcb.CURRENT_TIME)

        xcb.core.send_event(False, wid, xcb.EVENT_MASK_NO_EVENT, event)

    else:
        xcb.core.kill_client(wid)


def focus(wid):
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
        managed[wid].handle_focus(wid)

    pwm.events.focus_changed(win)


def _handle_focus(wid, focused):
    """Set border color and input focus according to focus."""

    border = None
    if focused:
        border = pwm.color.get_pixel(config.window.focused)
    else:
        border = pwm.color.get_pixel(config.window.unfocused)

    change_attributes(wid, [(xcb.CW_BORDER_PIXEL, border)])

    if focused:
        xcb.core.set_input_focus(xcb.INPUT_FOCUS_POINTER_ROOT,
                                 wid,
                                 xcb.TIME_CURRENT_TIME)

        if managed[wid].windows[wid]["floating"]:
            configure(wid, stackmode=xcb.STACK_MODE_ABOVE)


@contextmanager
def no_enter_notify_event():
    """Prevent all managed windows from sending EnterNotifyEvent."""

    eventmask = MANAGED_EVENT_MASK
    eventmask &= ~xcb.EVENT_MASK_ENTER_WINDOW
    for wid in managed:
        change_attributes(wid, [(xcb.CW_EVENT_MASK, eventmask)])

    yield

    for wid in managed:
        change_attributes(wid, [(xcb.CW_EVENT_MASK, MANAGED_EVENT_MASK)])


def only_if_focused(func):
    """A decorator to call the function only if there is a focused window.

    The wrapped function will receive 2 additional parameters, the focused
    window and its workspace.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        focused = pwm.windows.focused
        if focused:
            func(focused, managed[focused], *args, **kwargs)
    return wrapper
