#!/usr/bin/env python
# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import logging
import os
import sys

import pwm
from pwm.config import config
from pwm.ffi.xcb import xcb
import pwm.xcbutil
import pwm.events
import pwm.bar
import pwm.systray
import pwm.workspaces
import pwm.keybind


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt='%m-%d %H:%M:%S')

    logging.info("Startup...")

    loglevel = config.loglevel.upper()
    if loglevel != "INFO":
        logging.getLogger().setLevel(getattr(logging, loglevel))
        logging.info("Changed to loglevel %s" % loglevel)

    xcb.connect()
    pwm.xcbutil.setup_root_window()
    pwm.workspaces.setup()
    pwm.bar.setup()
    pwm.systray.setup()
    pwm.keybind.update_keyboard_mapping()
    pwm.config.setup_keys()

    logging.info("Entering main event loop...")
    pwm.events.loop()

    logging.info("Shutting down...")
    pwm.systray.destroy()
    pwm.bar.destroy()
    pwm.workspaces.destroy()
    xcb.core.disconnect()

    if pwm.restart:
        logging.info("Restarting...")
        os.execv(sys.argv[0], sys.argv)

if __name__ == "__main__":
    main()
