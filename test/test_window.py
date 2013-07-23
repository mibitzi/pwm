# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import xcb.xproto as xproto

import pwm.xcb
import pwm.workspaces
import pwm.window


class TestWindow(unittest.TestCase):
    def setUp(self):
        pwm.xcb.connect()
        pwm.workspaces.setup()

        # TODO: create real window to test with
        self.window = pwm.window.Window(0)

    def tearDown(self):
        pwm.workspaces.destroy()
        pwm.xcb.disconnect()

    def test_configure(self):
        self.window.configure(x=100, y=200, width=300, height=400)

        self.assertEqual(self.window.x, 100)
        self.assertEqual(self.window.y, 200)
        self.assertEqual(self.window.width, 300)
        self.assertEqual(self.window.height, 400)

    def test_show(self):
        self.window.show()

        self.assertTrue(self.window.visible)

        # TODO: create a real window to test
        #attr = pwm.xcb.core.GetWindowAttributes(self.window.wid).reply()
        #self.assertEqual(attr.map_state, xproto.MapState.Viewable)

    def test_hide(self):
        self.window.hide()

        self.assertFalse(self.window.visible)

        # TODO: create a real window to test
        #attr = pwm.xcb.core.GetWindowAttributes(self.window.wid).reply()
        #self.assertEqual(attr.map_state, xproto.MapState.Unmapped)

    def test_handle_focus(self):
        self.window.handle_focus(True)
        self.assertTrue(self.window.focused)

        self.window.handle_focus(False)
        self.assertFalse(self.window.focused)
