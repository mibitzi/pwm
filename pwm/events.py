# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import logging
import functools

from pwm.ffi.xcb import xcb, XcbError
import pwm.atom
import pwm.windows
import pwm.workspaces
import pwm.keybind
import pwm.systray
import pwm.menu
import pwm.worker


shutdown = False


class Event(set):
    """Simple event class based on a set."""

    def fire(self, *args, **kargs):
        """Call all handlers."""

        # Iterate over a copy to enable manipulation during firing
        for handler in self.copy():
            handler(*args, **kargs)

    __call__ = fire


class HandlerList:
    """A list of event handlers."""
    def __init__(self):
        self.handlers = []

    def add(self, event, handler):
        self.handlers.append((event, handler))
        event.add(handler)

    def destroy(self):
        for event, handler in self.handlers:
            event.remove(handler)
        self.handlers = []


# handler(window)
focus_changed = Event()

# handler(window)
window_name_changed = Event()

# handler(window)
window_unmapped = Event()

# handler(window)
window_exposed = Event()

# handler(index)
workspace_switched = Event()


def loop():
    while not shutdown:
        try:
            ev = xcb.core.wait_for_event()
            if ev:
                pwm.worker.tasks.put(functools.partial(_handle, ev))
        except XcbError:
            logging.exception("XCB Error")


def _handle(event):
    etype = event.response_type & ~0x80

    if etype == xcb.MAP_REQUEST:
        event = xcb.ffi.cast("xcb_map_request_event_t*", event)
        pwm.windows.manage(event.window)

    elif etype == xcb.UNMAP_NOTIFY:
        event = xcb.ffi.cast("xcb_unmap_notify_event_t*", event)
        handle_unmap(event.window)

    elif etype == xcb.DESTROY_NOTIFY:
        event = xcb.ffi.cast("xcb_destroy_notify_event_t*", event)
        handle_unmap(event.window)

    elif etype == xcb.CONFIGURE_REQUEST:
        event = xcb.ffi.cast("xcb_configure_request_event_t*", event)
        logging.debug("CONFIGURE_REQUEST {}".format(event.window))
        handle_configure_request(event)

    elif etype == xcb.EXPOSE:
        event = xcb.ffi.cast("xcb_expose_event_t*", event)
        window_exposed(event.window)

    elif etype == xcb.ENTER_NOTIFY:
        event = xcb.ffi.cast("xcb_enter_notify_event_t*", event)
        if event.event in pwm.windows.managed:
            pwm.windows.focus(event.event)

    elif etype == xcb.PROPERTY_NOTIFY:
        event = xcb.ffi.cast("xcb_property_notify_event_t*", event)
        handle_property_notify(event)

    elif etype == xcb.MAPPING_NOTIFY:
        event = xcb.ffi.cast("xcb_mapping_notify_event_t*", event)
        pwm.keybind.update_keyboard_mapping(event)

    elif etype == xcb.KEY_PRESS:
        event = xcb.ffi.cast("xcb_key_press_event_t*", event)
        if pwm.menu.active:
            pwm.menu.handle_key_press_event(event)
        else:
            pwm.config.handle_key_press_event(event)

    elif etype == xcb.CLIENT_MESSAGE:
        event = xcb.ffi.cast("xcb_client_message_event_t*", event)
        if event.type == pwm.atom.get("_NET_SYSTEM_TRAY_OPCODE"):
            pwm.systray.handle_client_message(event)
        elif event.type == pwm.atom.get("_NET_WM_STATE"):
            handle_wm_state(event)

    xcb.free(event)


def handle_unmap(wid):
    if wid in pwm.windows.managed:
        if pwm.windows.managed[wid].ignore_unmaps == 0:
            pwm.windows.unmanage(wid)
            window_unmapped(wid)
        else:
            pwm.windows.managed[wid].ignore_unmaps -= 1

    elif wid in pwm.systray.clients:
        pwm.systray.handle_unmap(wid)


def handle_configure_request(event):
    # See the spec for more about this event:
    # http://tronche.com/gui/x/icccm/sec-4.html#s-4.1.5

    managed = event.window in pwm.windows.managed

    if managed:
        ws = pwm.windows.managed[event.window].workspace
        floating = pwm.windows.managed[event.window].floating
    else:
        ws = None
        floating = False

    if not managed or floating:
        # The window is either not managed or a floating one, so there is no
        # reason not to obey the request.
        kwargs = {}
        if event.value_mask & xcb.CONFIG_WINDOW_X:
            kwargs["x"] = event.x

        if event.value_mask & xcb.CONFIG_WINDOW_Y:
            kwargs["y"] = event.y

        if event.value_mask & xcb.CONFIG_WINDOW_WIDTH:
            kwargs["width"] = event.width

        if event.value_mask & xcb.CONFIG_WINDOW_HEIGHT:
            kwargs["height"] = event.height

        # Note that we don't want to set border_width or stack_mode for managed
        # windows, even if requested.
        if not managed:
            if event.value_mask & xcb.CONFIG_WINDOW_STACK_MODE:
                kwargs["stackmode"] = event.stack_mode
            if event.value_mask & xcb.CONFIG_WINDOW_SIBLING:
                kwargs["sibling"] = event.sibling
            if event.value_mask & xcb.CONFIG_WINDOW_BORDER_WIDTH:
                kwargs["borderwidth"] = event.border_width

        # Note that the requested values are in absolute coordinates.
        pwm.windows.configure(event.window, absolute=True, **kwargs)
    else:
        # Just notify the client about its actual geometry.
        ws.tiling.arrange(event.window)


def handle_property_notify(event):
    if event.atom == pwm.atom.get("_XEMBED_INFO"):
        pwm.systray.handle_property_notify(event)
    elif event.atom in (xcb.ATOM_WM_NAME, pwm.atom.get("_NET_WM_NAME")):
        wid = event.window
        if wid in pwm.windows.managed:
            window_name_changed(wid)


def handle_wm_state(event):
    msgtype = event.data.data32[1]
    type_fullscreen = pwm.atom.get("_NET_WM_STATE_FULLSCREEN")
    type_urgent = pwm.atom.get("_NET_WM_STATE_DEMANDS_ATTENTION")

    logging.debug("{} for {}".format(pwm.atom.get_name(msgtype), event.window))

    if event.format != 32 or msgtype not in (type_fullscreen, type_urgent):
        return

    wid = event.window
    if wid not in pwm.windows.managed:
        return

    action = event.data.data32[0]

    if msgtype == type_fullscreen:
        isfull = pwm.windows.managed[wid].fullscreen

        if (action == pwm.atom._NET_WM_STATE_TOGGLE or
                (isfull and action == pwm.atom._NET_WM_STATE_REMOVE) or
                (not isfull and action == pwm.atom._NET_WM_STATE_ADD)):
            pwm.windows.managed[wid].workspace.toggle_fullscreen(wid)

    elif msgtype == type_urgent:
        pass
