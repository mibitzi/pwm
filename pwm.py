#!/usr/bin/env python2
# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import logging

import pwm.xcb
import pwm.events
import pwm.workspaces


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    pwm.xcb.connect()
    pwm.xcb.setup_screens()

    pwm.workspaces.add(pwm.workspaces.Workspace())

    pwm.events.loop()

    pwm.xcb.disconnect()
