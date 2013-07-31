# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import select
import logging
import xcb
import xcb.xproto as xp

import pwm
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

# handler(index)
workspace_switched = Event()


def poll():
    while True:
        try:
            event = pwm.xcb.conn.poll_for_event()
            if not event:
                break
            handle(event)
        except xcb.Error:
            logging.exception("XCB Error")


def loop():
    fd = pwm.xcb.conn.get_file_descriptor()

    try:
        while not pwm.shutdown:
            # Wait until there is actually something to do, then poll
            select.select([fd], [], [])
            poll()
            pwm.xcb.conn.flush()

    except (KeyboardInterrupt, SystemExit):
        pass


def handle(event):
    etype = type(event)

    if etype == xp.MapRequestEvent:
        pwm.windows.manage(event.window)

    elif etype == xp.MapNotifyEvent:
        handle_focus(event.window)

    elif etype == xp.UnmapNotifyEvent:
        if event.event != pwm.xcb.screen.root:
            handle_unmap(event.window)

    elif etype == xp.DestroyNotifyEvent:
        handle_unmap(event.window)

    elif etype == xp.EnterNotifyEvent:
        handle_focus(event.event)

    elif etype == xp.PropertyNotifyEvent:
        win = event.window
        if win in pwm.windows.managed:
            window_property_changed(win)

    elif etype == xp.MappingNotifyEvent:
        pwm.keybind.update_keyboard_mapping(event)

    elif etype == xp.KeyPressEvent:
        pwm.config.handle_key_press_event(event)

    else:
        logging.debug("Unhandled event: %s" % event.__class__.__name__)


def handle_focus(wid):
    if wid in pwm.windows.managed:
        pwm.windows.handle_focus(wid)
        pwm.workspaces.current().handle_focus(wid)


def handle_unmap(wid):
    if wid in pwm.windows.managed:
        pwm.windows.unmanage(wid)
        window_unmapped(wid)
