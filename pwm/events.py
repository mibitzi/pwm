# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import logging
import xcb
import xcb.xproto as xp

import pwm.xcb
import pwm.window
import pwm.workspaces


class Event(set):
    """Simple event class based on a set."""

    def fire(self, *args, **kargs):
        """Fires this event and calls all handlers."""

        # Iterate over a copy to enable manipulation during firing
        for handler in self.copy():
            handler(*args, **kargs)

    __call__ = fire

# handler(window)
window_focused = Event()

# handler(window)
window_property_changed = Event()

# handler(window)
window_mapped = Event()

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
        w = pwm.window.Window(event.window)
        window_mapped(w)

    elif isinstance(event, xp.UnmapNotifyEvent):
        result = pwm.workspaces.find_window(event.window)
        if result is not None:
            window_unmapped(result[0])

    elif isinstance(event, xp.EnterNotifyEvent):
        w = pwm.workspaces.current().find_window(event.event)
        if w:
            window_focused(w)

    elif isinstance(event, xp.PropertyNotifyEvent):
        w = pwm.workspaces.current().find_window(event.window)
        if w:
            window_property_changed(w)
