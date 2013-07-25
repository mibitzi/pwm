# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import pwm.commands


class TestCommands(unittest.TestCase):
    def setUp(self):
        pwm.xcb.connect()
        pwm.workspaces.setup()

    def tearDown(self):
        pwm.workspaces.destroy()
        pwm.xcb.disconnect()

    def test_switch_workspace(self):
        pwm.commands.switch_workspace(1)

        self.assertEqual(pwm.workspaces.current(),
                         pwm.workspaces.workspaces[1])
