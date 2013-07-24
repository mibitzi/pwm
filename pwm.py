#!/usr/bin/env python2
# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import logging

from pwm.config import config
import pwm.xcb
import pwm.events
import pwm.workspaces


def main():
    loglevel = config["loglevel"].upper()

    if loglevel != "INFO":
        logging.basicConfig(level=getattr(logging, loglevel, None))
        logging.info("Changed to loglevel %s" % loglevel)

    pwm.xcb.connect()
    pwm.xcb.setup_screens()
    pwm.workspaces.setup()

    pwm.events.loop()

    pwm.xcb.disconnect()

if __name__ == "__main__":
    main()
