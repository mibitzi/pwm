# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from pwm.config import config
import pwm.windows


class Rule:
    def __init__(self, prop, value, floating=False, workspace=None):
        self.prop = prop
        self.value = value.lower()
        self.floating = floating
        self.workspace = workspace


def _find_rules(wid):
    def _lower(s):
        return s.lower() if s else None

    for rule in config.rules:
        if ((rule.prop == "class" and
             rule.value == _lower(pwm.windows.get_property(
                 wid, "WM_CLASS"))) or
            (rule.prop == "role" and
             rule.value == _lower(pwm.windows.get_property(
                 wid, "WM_WINDOW_ROLE"))) or
            (rule.prop == "name" and
             rule.value == _lower(pwm.windows.get_name(wid)))):
            yield rule


def floating(wid):
    """Return true if this window has a floating rule."""

    for rule in _find_rules(wid):
        if rule.floating:
            return True
    return False
