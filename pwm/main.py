#!/usr/bin/env python3
# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import argparse
import logging
import os
import sys

import pwm
from pwm.config import config
from pwm.ffi.xcb import xcb
import pwm.xutil
import pwm.events
import pwm.bar
import pwm.menu
import pwm.systray
import pwm.workspaces
import pwm.keybind
import pwm.state
import pwm.worker


restart = False


def main():
    """The entry point for pwm."""

    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--loglevel", help="the level of log verbosity",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR",
                                 "CRITICAL"])
    parser.add_argument("-r", "--restore",
                        help="automatically set when restarting",
                        action="store_true")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt='%m-%d %H:%M:%S')

    logging.info("Startup...")

    logging.info("Loading config...")
    config.load()

    # Loglevel passed via the command line has higher priority
    loglevel = config.loglevel
    if args.loglevel:
        loglevel = args.loglevel

    loglevel = loglevel.upper()
    if loglevel != "INFO":
        logging.info("Changing loglevel to %s..." % loglevel)
        logging.getLogger().setLevel(loglevel)

    xcb.connect()
    pwm.xutil.setup_root_window()
    pwm.workspaces.setup()
    pwm.bar.setup()
    pwm.menu.setup()
    pwm.systray.setup()
    pwm.keybind.update_keyboard_mapping()
    pwm.config.setup_keys()

    # Restore has to be placed after the setups, otherwise the restored values
    # will be overwritten again.
    if args.restore:
        logging.info("Restoring state...")
        pwm.state.restore()

    pwm.windows.manage_existing()

    logging.info("Entering main event loop...")
    eventloop = pwm.events.initiate_loop()
    pwm.widgets.start()

    # The worker will run until it receives a shutdown signal
    pwm.worker.process_tasks()

    eventloop.join(1)

    logging.info("Shutting down...")

    if restart:
        pwm.state.store()

    pwm.widgets.destroy()
    pwm.systray.destroy()
    pwm.menu.destroy()
    pwm.bar.destroy()
    pwm.workspaces.destroy()
    xcb.core.disconnect()

    if restart:
        logging.info("Restarting...")

        # Make sure to pass the restore flag
        if not args.restore:
            sys.argv.append("-r")

        os.execv(sys.argv[0], sys.argv)

if __name__ == "__main__":
    main()
