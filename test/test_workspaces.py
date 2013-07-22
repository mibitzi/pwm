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
        pwm.xcb.setup_screens()
        pwm.workspaces.setup()

        self.window = pwm.window.Window(0)
        self.workspace = pwm.workspaces.current()

    def tearDown(self):
        pwm.xcb.disconnect()

    def test_geometry(self):
        self.assertEqual(self.workspace.x, 0)
        self.assertEqual(self.workspace.y, self.workspace.bar.height)
        self.assertEqual(self.workspace.width, pwm.xcb.screen.width_in_pixels)
        self.assertEqual(
            self.workspace.height,
            pwm.xcb.screen.height_in_pixels - self.workspace.bar.height)

    def test_focus(self):
        self.workspace.focus(self.window)
        self.assertIsNone(self.workspace.focused)
        self.assertFalse(self.window.focused)

        self.workspace.add_window(self.window)
        self.workspace.focus(self.window)
        self.assertEqual(self.workspace.focused, self.window)
        self.assertTrue(self.window.focused)
