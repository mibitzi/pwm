# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import pwm.xcb
import pwm.workspaces
import pwm.windows


class TestWindow(unittest.TestCase):
    def setUp(self):
        pwm.xcb.connect()
        pwm.workspaces.setup()

        # TODO: create real window to test with
        pwm.windows.handle_map_request(pwm.xcb.screen.root)
        (self.window, _) = pwm.windows.find(pwm.xcb.screen.root)

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

    def test_handle_unmap_notification(self):
        pwm.windows.handle_unmap_notification(self.window)
        win, ws = pwm.windows.find(self.window.wid)
        self.assertIsNone(win)
        self.assertNotIn(win, pwm.workspaces.current().windows)

    def test_handle_focus(self):
        # TODO: create real windows to test
        pwm.windows.handle_focus(self.window.wid)
        self.assertEqual(pwm.windows.focused, self.window)

    def test_find(self):
        win, _ = pwm.windows.find(self.window.wid)
        self.assertEqual(win, self.window)
