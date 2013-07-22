# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

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
    ename = event.__class__.__name__
    if ename.endswith("Event"):
        ename = ename[:-5]

    if ename == "MapRequest":
        w = pwm.window.Window(pwm.workspaces.current(), event.window)
        pwm.workspaces.current().add_window(w)
    elif ename == "UnmapNotify":
        w = pwm.workspaces.find_window(event.window)
        w.workspace.remove_window(w)
