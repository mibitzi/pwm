# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest
from unittest.mock import patch

import pwm.rules
import pwm.windows
from pwm.config import config


class TestRules(unittest.TestCase):
    def setUp(self):
        config.load(default=True)

    def test_floating(self):
        rule = pwm.rules.Rule("class", "Vlc", floating=True)

        with patch.object(config, "rules", [rule]):
            with patch.object(pwm.windows, "get_wm_class",
                              return_value="Vlc"):
                self.assertTrue(pwm.rules.floating(0))
