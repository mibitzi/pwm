# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import pwm.config
import pwm.commands


class TestCommands(unittest.TestCase):

    def test_key(self):
        key = pwm.config.Key("", pwm.commands.test, 33, a=66)
        ret = key.call()

        self.assertEqual(ret[0], (33,))
        self.assertEqual(ret[1]["a"], 66)
