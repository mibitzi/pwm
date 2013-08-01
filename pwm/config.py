# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import imp
import logging

import pwm.keybind
from pwm.ffi.xcb import xcb

config = None
grabbed_keys = {}


class Config:
    def __init__(self):
        self.loaded = False
        self.data = None

    def load(self):
        self.loaded = True
        self.data = imp.load_source("config", "config.py")

    def __getattr__(self, name):
        if not self.loaded:
            self.load()

        return getattr(self.data, name)


def setup_keys():
    """Parse and grab all keys defined in the configuration."""

    for key in config.keys:
        keystr = key[0]
        mods, keycode = pwm.keybind.parse_keystring(keystr)

        if mods != 0 and keycode:
            pwm.keybind.grab_key(xcb.screen.root, mods, keycode)

            grabbed_keys[(mods, keycode)] = key
        else:
            # This is not a critical error, we just can't respond to that key
            logging.error("Could not parse keybinding: {}".format(keystr))


def handle_key_press_event(event):
    """Search for a command to handle this KeyPressEvent and call it."""

    # Strip out all trivial modifiers such as capslock or numlock.
    # Then check if the key was grabbed
    mods, keycode = event.state, event.detail
    mods = pwm.keybind.strip_trivial(mods)

    key = grabbed_keys.get((mods, keycode))
    if key:
        key[1]()


config = Config()
