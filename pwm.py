#!/usr/bin/env python2
# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import logging

from pwm.config import config
import pwm.xcb
import pwm.events
import pwm.bar
import pwm.workspaces
import pwm.keybind


def main():
    loglevel = config.loglevel.upper()

    if loglevel != "INFO":
        logging.basicConfig(
            level=getattr(logging, loglevel, None),
            format='%(asctime)s:%(levelname)s:%(message)s',
            datefmt='%m-%d %H:%M:%S')
        logging.info("Changed to loglevel %s" % loglevel)

    pwm.xcb.connect()
    pwm.xcb.setup_root_window()
    pwm.workspaces.setup()
    pwm.bar.setup()

    pwm.keybind.update_keyboard_mapping()
    pwm.config.setup_keys()
    pwm.events.loop()

    logging.info("Exiting")
    pwm.bar.destroy()
    pwm.workspaces.destroy()
    pwm.xcb.disconnect()

if __name__ == "__main__":
    main()
