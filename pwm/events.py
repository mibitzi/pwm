# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import logging
import xcb.xproto as xp

import pwm.xcb
import pwm.window
import pwm.workspaces


def loop():
    try:
        while True:
            event = pwm.xcb.conn.poll_for_event()
            handle(event)
            pwm.xcb.conn.flush()
    except (KeyboardInterrupt, SystemExit):
        pass


def handle(event):
    if isinstance(event, xp.MapRequestEvent):
        #if event.window == pwm.workspaces.current().bar.wid:
        #    logging.debug("ExposeEvent on bar")
        #    pwm.workspaces.current().bar.show()

        w = pwm.workspaces.current().find_window(event.window)

        if w is None:
            w = pwm.window.Window(event.window)
            pwm.workspaces.current().add_window(w)
        #else:
        #    logging.debug("ExposeEvent on existing window")
        #    w.show()

    elif isinstance(event, xp.UnmapNotifyEvent):
        result = pwm.workspaces.find_window(event.window)
        if result is not None:
            w, workspace = result
            workspace.remove_window(w)

    elif isinstance(event, xp.EnterNotifyEvent):
        w = pwm.workspaces.current().find_window(event.event)
        if w:
            pwm.workspaces.current().focus(w)

    elif isinstance(event, xp.PropertyNotifyEvent):
        w = pwm.workspaces.current().find_window(event.window)
        if w:
            pwm.workspaces.current().handle_property_notify(w)
