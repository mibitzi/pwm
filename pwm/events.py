# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import logging
import xcb
import xcb.xproto as xp

import pwm.xcb
import pwm.windows
import pwm.workspaces
import pwm.keybind


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


def loop():
    while True:
        try:
            event = pwm.xcb.conn.poll_for_event()
            handle(event)
            pwm.xcb.conn.flush()
        except xcb.Error:
            logging.exception("XCB Error")
        except (KeyboardInterrupt, SystemExit):
            break


def handle(event):
    if isinstance(event, xp.MapRequestEvent):
        pwm.windows.manage(event.window)

    elif isinstance(event, xp.MapNotifyEvent):
        handle_focus(event.window)

    elif isinstance(event, xp.UnmapNotifyEvent):
        if event.event != pwm.xcb.screen.root:
            handle_unmap(event.window)

    elif isinstance(event, xp.DestroyNotifyEvent):
        handle_unmap(event.window)

    elif isinstance(event, xp.EnterNotifyEvent):
        handle_focus(event.event)

    elif isinstance(event, xp.PropertyNotifyEvent):
        win = event.window
        if win in pwm.windows.managed:
            window_property_changed(win)

    elif isinstance(event, xp.MappingNotifyEvent):
        pwm.keybind.update_keyboard_mapping(event)

    elif isinstance(event, xp.KeyPressEvent):
        pwm.config.handle_key_press_event(event)

    elif event:
        logging.debug("Unhandled event: %s" % event.__class__.__name__)


def handle_focus(wid):
    if wid in pwm.windows.managed:
        pwm.windows.handle_focus(wid)
        pwm.workspaces.current().handle_focus(wid)


def handle_unmap(wid):
    if wid in pwm.windows.managed:
        pwm.windows.unmanage(wid)
        window_unmapped(wid)
