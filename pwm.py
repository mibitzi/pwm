#!/usr/bin/env python
# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import argparse
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
import pwm.state
import pwm.scheduler


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--loglevel", help="the level of log verbosity",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR",
                                 "CRITICAL"])
    parser.add_argument("-r", "--restore",
                        help="automatically set when restarting",
                        action="store_true")

    args = parser.parse_args()

    loglevel = config.loglevel
    if args.loglevel:
        loglevel = args.loglevel

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt='%m-%d %H:%M:%S')

    logging.info("Startup...")

    loglevel = loglevel.upper()
    if loglevel != "INFO":
        logging.getLogger().setLevel(loglevel)
        logging.info("Changed to loglevel %s" % loglevel)

    xcb.connect()
    pwm.xcbutil.setup_root_window()
    pwm.workspaces.setup()

    if args.restore:
        logging.info("Restoring state...")
        pwm.state.restore()

    pwm.scheduler.setup()
    pwm.bar.setup()
    pwm.systray.setup()
    pwm.keybind.update_keyboard_mapping()
    pwm.config.setup_keys()
    pwm.windows.manage_existing()
    pwm.scheduler.start()

    logging.info("Entering main event loop...")
    pwm.events.loop()

    logging.info("Shutting down...")

    if pwm.restart:
        pwm.state.store()

    pwm.scheduler.destroy()
    pwm.systray.destroy()
    pwm.bar.destroy()
    pwm.workspaces.destroy()
    xcb.core.disconnect()

    if pwm.restart:
        logging.info("Restarting...")
        if not args.restore:
            sys.argv.append("-r")
        os.execv(sys.argv[0], sys.argv)

if __name__ == "__main__":
    main()
