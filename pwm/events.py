# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import select
import logging

import pwm
from pwm.ffi.xcb import xcb, XcbError
import pwm.xcbutil
import pwm.windows
import pwm.workspaces
import pwm.keybind
import pwm.systray
import pwm.menu


class Event(set):
    """Simple event class based on a set."""

    def fire(self, *args, **kargs):
        """Call all handlers."""

        # Iterate over a copy to enable manipulation during firing
        for handler in self.copy():
            handler(*args, **kargs)

    __call__ = fire

# handler(window)
focus_changed = Event()

# handler(window)
window_property_changed = Event()

# handler(window)
window_unmapped = Event()

# handler(window)
window_exposed = Event()

# handler(index)
workspace_switched = Event()


def poll():
    while True:
        try:
            event = xcb.core.poll_for_event()
            if not event:
                break
            handle(event)
        except XcbError:
            logging.exception("XCB Error")


def loop():
    fd = xcb.core.get_file_descriptor()

    try:
        while not pwm.shutdown:
            # Wait until there is actually something to do, then poll
            select.select([fd], [], [])
            poll()
            xcb.core.flush()

    except (KeyboardInterrupt, SystemExit):
        pass


def handle(event):
    etype = event.response_type & ~0x80

    if etype == xcb.MAP_REQUEST:
        event = xcb.ffi.cast("xcb_map_request_event_t*", event)
        pwm.windows.manage(event.window)

    elif etype == xcb.MAP_NOTIFY:
        event = xcb.ffi.cast("xcb_map_notify_event_t*", event)
        handle_focus(event.window)

    elif etype == xcb.UNMAP_NOTIFY:
        event = xcb.ffi.cast("xcb_unmap_notify_event_t*", event)
        handle_unmap(event.window)

    elif etype == xcb.DESTROY_NOTIFY:
        event = xcb.ffi.cast("xcb_destroy_notify_event_t*", event)
        handle_unmap(event.window)

    elif etype == xcb.EXPOSE:
        event = xcb.ffi.cast("xcb_expose_event_t*", event)
        window_exposed(event.window)

    elif etype == xcb.ENTER_NOTIFY:
        event = xcb.ffi.cast("xcb_enter_notify_event_t*", event)
        handle_focus(event.event)

    elif etype == xcb.PROPERTY_NOTIFY:
        event = xcb.ffi.cast("xcb_property_notify_event_t*", event)

        if event.atom == pwm.xcbutil.get_atom("_XEMBED_INFO"):
            pwm.systray.handle_property_notify(event)
        else:
            win = event.window
            if win in pwm.windows.managed:
                window_property_changed(win)

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
        if event.type == pwm.xcbutil.get_atom("_NET_SYSTEM_TRAY_OPCODE"):
            pwm.systray.handle_client_message(event)


def handle_focus(wid):
    if wid in pwm.windows.managed:
        pwm.windows.handle_focus(wid)
        pwm.workspaces.current().handle_focus(wid)


def handle_unmap(wid):
    if wid in pwm.windows.managed:
        if pwm.windows.ignore_unmaps.get(wid, 0) == 0:
            pwm.windows.unmanage(wid)
            window_unmapped(wid)
        else:
            pwm.windows.ignore_unmaps[wid] -= 1

    elif wid in pwm.systray.clients:
        pwm.systray.handle_unmap(wid)
