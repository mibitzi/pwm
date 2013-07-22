# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import pwm.xcb
import pwm.workspaces
import pwm.window


class TestWindow(unittest.TestCase):
    def setUp(self):
        pwm.xcb.connect()
        pwm.workspaces.setup()
        self.window = pwm.window.Window(0)

    def tearDown(self):
        pwm.xcb.disconnect()

    def test_configure(self):
        self.window.configure(x=100, y=200, width=300, height=400)

        self.assertEqual(self.window.x, 100)
        self.assertEqual(self.window.y, 200)
        self.assertEqual(self.window.width, 300)
        self.assertEqual(self.window.height, 400)

    def test_handle_focus(self):
        self.window.handle_focus(True)
        self.assertTrue(self.window.focused)

        self.window.handle_focus(False)
        self.assertFalse(self.window.focused)
