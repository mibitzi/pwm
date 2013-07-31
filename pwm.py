#!/usr/bin/env python3
# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import logging

from pwm.config import config
from pwm.ffi.xcb import xcb
#import pwm.xcb
import pwm.events
#import pwm.bar
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
    setup_root_window()
    #pwm.xcb.setup_root_window()
    pwm.workspaces.setup()
    #pwm.bar.setup()

    pwm.keybind.update_keyboard_mapping()
    pwm.config.setup_keys()
    pwm.events.loop()

    logging.info("Exiting")
    #pwm.bar.destroy()
    pwm.workspaces.destroy()
    xcb.core.disconnect()


def setup_root_window():
    mask_values = (xcb.EVENT_MASK_STRUCTURE_NOTIFY |
                   xcb.EVENT_MASK_SUBSTRUCTURE_NOTIFY |
                   xcb.EVENT_MASK_SUBSTRUCTURE_REDIRECT |
                   xcb.EVENT_MASK_ENTER_WINDOW |
                   xcb.EVENT_MASK_LEAVE_WINDOW)

    cookie = xcb.core.change_window_attributes_checked(
        xcb.screen.root,
        *xcb.mask([(xcb.CW_EVENT_MASK, mask_values)]))

    cookie.check()

if __name__ == "__main__":
    main()
