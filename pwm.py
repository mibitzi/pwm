#!/usr/bin/env python3
# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import logging
import os
import sys

import pwm
from pwm.config import config
from pwm.ffi.xcb import xcb
import pwm.xcbutil
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

    xcb.connect()
    pwm.xcbutil.setup_root_window()
    pwm.workspaces.setup()
    pwm.bar.setup()

    pwm.keybind.update_keyboard_mapping()
    pwm.config.setup_keys()
    pwm.events.loop()

    logging.info("Shutting down...")
    pwm.bar.destroy()
    pwm.workspaces.destroy()
    xcb.core.disconnect()


    if pwm.restart:
        logging.info("Restarting...")
        os.execv(sys.argv[0], sys.argv)

if __name__ == "__main__":
    main()
