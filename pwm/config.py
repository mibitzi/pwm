# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import logging
from importlib.machinery import SourceFileLoader

import pwm.keybind
from pwm.ffi.xcb import xcb

config = None
grabbed_keys = {}


class Config:
    def __init__(self):
        self.data = None

    def load(self):
        self.data = SourceFileLoader("config", "config.py").load_module()

    def __getattr__(self, name):
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
        try:
            key[1]()
        except:
            logging.exception("Command error")


config = Config()
