# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from contextlib import contextmanager
from functools import wraps
import struct

from pwm.ffi.xcb import xcb
from pwm.config import config
import pwm.atom
import pwm.events
import pwm.workspaces
import pwm.color
import pwm.rules


managed = {}
focused = None

MANAGED_EVENT_MASK = (xcb.EVENT_MASK_ENTER_WINDOW |
                      xcb.EVENT_MASK_FOCUS_CHANGE |
                      xcb.EVENT_MASK_PROPERTY_CHANGE)


class Info:
    def __init__(self):
        # Some UnmapNotifyEvents, like those generated when switching
        # workspaces, have to be ignored. This indicates how many future
        # UnmapNotifyEvents have to be ignored.
        self.ignore_unmaps = 0

        self.floating = False
        self.fullscreen = False
        self.urgent = False
        self.workspace = None
        self.geometry = None


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

    info = Info()
    managed[wid] = info

    info.floating = should_float(wid)
    update_geometry(wid, force=True)

    state = get_property(wid, "_NET_WM_STATE")
    if state and pwm.atom.get("_NET_WM_STATE_FULLSCREEN") in state:
        info.fullscreen = True

    change_attributes(wid, [(xcb.CW_EVENT_MASK, MANAGED_EVENT_MASK)])

    pwm.workspaces.current().add_window(wid)
    info.workspace = pwm.workspaces.current()

    focus(wid)


def unmanage(wid):
    if wid not in managed:
        return

    ws = managed[wid].workspace
    ws.remove_window(wid)
    del managed[wid]

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

    if pwm.rules.floating(wid):
        return True

    # Check the _NET_WM_WINDOW_TYPE property to determine the type of this
    # window.
    # See the specification for more info:
    # http://standards.freedesktop.org/wm-spec/wm-spec-latest.html

    wintype = get_property(wid, "_NET_WM_WINDOW_TYPE")

    if not wintype:
        return False

    for wt in wintype:
        if (wt == pwm.atom.get("_NET_WM_WINDOW_TYPE_DIALOG") or
                wt == pwm.atom.get("_NET_WM_WINDOW_TYPE_UTILITY") or
                wt == pwm.atom.get("_NET_WM_WINDOW_TYPE_TOOLBAR") or
                wt == pwm.atom.get("_NET_WM_WINDOW_TYPE_SPLASH")):

            return True

    return False


def update_geometry(wid, force=False):
    # We only want the geometry if this window is floating
    if force or managed[wid].floating:
        managed[wid].geometry = get_geometry(wid)


def is_mapped(wid):
    """Return True if the window is mapped, otherwise False."""
    attr = xcb.core.get_window_attributes(wid).reply()
    return attr.map_state == xcb.MAP_STATE_VIEWABLE


def change_attributes(wid, masks):
    """Set attributes for the given window."""
    xcb.core.change_window_attributes(wid, *xcb.mask(masks))


def get_name(wid):
    """Get the window name."""

    name = get_property(wid, "_NET_WM_NAME")

    if not name:
        name = get_property(wid, xcb.ATOM_WM_NAME)

    return name or ""


def get_property(wid, atom):
    """Get a property of this window."""

    if isinstance(atom, str):
        atom = pwm.atom.get(atom)

    reply =  xcb.core.get_property(False, wid, atom,
                                   xcb.GET_PROPERTY_TYPE_ANY, 0,
                                   2 ** 32 - 1).reply()

    # We want to turn the value into something useful.
    # In particular, if the format of the reply is 8, then assume that it is a
    # string. Moreover, it could be a list of null terminated strings.
    # Otherwise, the format must be a list of integers.

    value = xcb.get_property_value(reply)

    if reply.format == 8:
        value = xcb.ffi.cast("char*", value)

        #if 0 in value[:-1]:
        #    ret = []
        #    s = []
        #    for o in value:
        #        if o == 0:
        #            ret.append(''.join(s))
        #            s = []
        #        else:
        #            s.append(chr(o))
        #else:
        ret = xcb.ffi.string(value, reply.value_len).decode("UTF-8")

        return ret
    elif reply.format in (16, 32):
        value = xcb.ffi.cast("uint%d_t*" % reply.format, value)
        return [value[i] for i in range(reply.value_len)]

    return None


def set_property(wid, atom, value, proptype=None):
    fmt = 0
    data = []
    datalen = 0

    if not isinstance(value, (list, tuple)):
        value = [value]

    if isinstance(value[0], str):
        fmt = 8
        data = b"\x00".join(val.encode("UTF-8") for val in value)
        datalen = len(data)

        if not proptype:
            proptype = pwm.atom.get("UTF8_STRING")

    elif isinstance(value[0], int):
        fmt = 32
        datalen = len(value)
        data = struct.pack("{}I".format(datalen), *value)

        if not proptype:
            # We just assume it's an atom, but it could also be something else.
            proptype = xcb.ATOM_ATOM

    if isinstance(atom, str):
        atom = pwm.atom.get(atom)

    xcb.core.change_property(xcb.PROP_MODE_REPLACE, wid, atom, proptype, fmt,
                             datalen, data)


def configure(wid, **kwargs):
    """Configure the window and set the given variables in relation to the
    workspace.

    Arguments can be: x, y, width, height, stackmode
    If absolute=True then the window will be configured in absolute coordinates
    and not in relation to the workspace.
    """

    workspace = pwm.workspaces.current()
    values = []
    abs_ = 0 if kwargs.get("absolute", False) else 1

    border = (kwargs["borderwidth"] if "borderwidth" in kwargs
              else config.window.border)
    values.append((xcb.CONFIG_WINDOW_BORDER_WIDTH, border))

    # We need to cast x and y in order to have correct handling for negative
    # values.
    if "x" in kwargs:
        values.append(
            (xcb.CONFIG_WINDOW_X,
             xcb.ffi.cast("uint32_t", int(workspace.x*abs_ + kwargs["x"]))))
    if "y" in kwargs:
        values.append(
            (xcb.CONFIG_WINDOW_Y,
             xcb.ffi.cast("uint32_t", int(workspace.y*abs_ + kwargs["y"]))))

    if "width" in kwargs:
        values.append((xcb.CONFIG_WINDOW_WIDTH,
                       max(0, int(kwargs["width"] - 2*border))))
    if "height" in kwargs:
        values.append((xcb.CONFIG_WINDOW_HEIGHT,
                       max(0, int(kwargs["height"] - 2*border))))

    if "stackmode" in kwargs:
        values.append((xcb.CONFIG_WINDOW_STACK_MODE, kwargs["stackmode"]))

    if "sibling" in kwargs:
        values.append((xcb.CONFIG_WINDOW_SIBLING, kwargs["sibling"]))

    xcb.core.configure_window(wid, *xcb.mask(values))

    if wid in managed and "noupdate" not in kwargs:
        if ("x" in kwargs or "y" in kwargs or
                "width" in kwargs or "height" in kwargs):
            update_geometry(wid)


def get_geometry(wid, absolute=False):
    """Get geometry information for the given window.

    Return a tuple(x, y, width, height).
    """

    geo = xcb.core.get_geometry(wid).reply()

    if not absolute:
        ws = pwm.workspaces.current()
        geo.x -= ws.x
        geo.y -= ws.y

    # Because borders are not included in width/height and because we
    # subtracted them when configuring we have to add them again.
    geo.width += 2*geo.border_width
    geo.height += 2*geo.border_width

    return (geo.x, geo.y, geo.width, geo.height)


def preferred_geometry(wid, workspace=None):
    """Return the preferd geometry for this window."""

    if not workspace:
        workspace = pwm.workspaces.current()

    # We will use the last known geometry.
    _, _, width, height = managed[wid].geometry

    # There should be some minimum size.
    width = max(10, width)
    height = max(10, height)

    # Just center the window.
    x = (workspace.width - width) / 2
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
    atom = pwm.atom.get("WM_DELETE_WINDOW")
    if atom in get_property(wid, "WM_PROTOCOLS"):
        event = create_client_message(
            wid,
            pwm.atom.get("WM_PROTOCOLS"),
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
        managed[wid].workspace.handle_focus(wid)

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

        # Focused floating windows should always be at the top.
        if managed[wid].floating:
            configure(wid, stackmode=xcb.STACK_MODE_ABOVE)

        # Focusing a window should remove its urgency flag
        if managed[wid].urgent:
            managed[wid].urgent = False


def toggle_urgent(wid):
    urgent = not managed[wid].urgent

    if urgent:
        border = pwm.color.get_pixel(config.window.urgent)
    else:
        border = pwm.color.get_pixel(config.window.unfocused)

    change_attributes(wid, [(xcb.CW_BORDER_PIXEL, border)])

    managed[wid].urgent = urgent

    if urgent:
        pwm.events.window_urgent_set(wid)


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

    The function will receive 2 additional parameters, the focused window and
    its workspace.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        focused = pwm.windows.focused
        if focused:
            func(focused, managed[focused].workspace, *args, **kwargs)
    return wrapper
