# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import pwm.xcb
import pwm.workspaces

connected = False


def setup():
    # To increase test speed we only want to connect once
    global connected
    if not connected:
        pwm.xcb.connect()
        pwm.xcb.setup_screens()
        connected = True

    pwm.workspaces.setup()


def tear_down():
    pwm.workspaces.destroy()
