# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import pwm.xcb
import pwm.workspaces
import pwm.window


class TestWorkspace(unittest.TestCase):
    def setUp(self):
        pwm.xcb.connect()
        pwm.xcb.setup_screens()
        pwm.workspaces.setup()

        self.window = pwm.window.Window(0)
        self.workspace = pwm.workspaces.current()

        self.workspace.add_window(self.window)

    def tearDown(self):
        pwm.workspaces.destroy()
        pwm.xcb.disconnect()

    def test_setup(self):
        # setup() was already called in the setup for this testcase

        self.assertEqual(len(pwm.workspaces.workspaces), 1)
        self.assertEqual(pwm.workspaces.current(),
                         pwm.workspaces.workspaces[0])

        self.assertTrue(pwm.workspaces.current().active)

    def test_destroy(self):
        pwm.workspaces.destroy()
        self.assertEqual(len(pwm.workspaces.workspaces), 0)

    def test_add(self):
        pwm.workspaces.add(pwm.workspaces.Workspace())
        self.assertEqual(len(pwm.workspaces.workspaces), 2)

    def test_geometry(self):
        self.assertEqual(self.workspace.x, 0)
        self.assertEqual(self.workspace.y, self.workspace.bar.height)
        self.assertEqual(self.workspace.width, pwm.xcb.screen.width_in_pixels)
        self.assertEqual(
            self.workspace.height,
            pwm.xcb.screen.height_in_pixels - self.workspace.bar.height)

    def test_add_window(self):
        self.assertEqual(len(self.workspace.windows), 1)
        self.assertTrue(self.window in self.workspace.windows)

    def test_remove_window(self):
        self.workspace.remove_window(self.window)

        self.assertEqual(len(self.workspace.windows), 0)

    def test_focus(self):
        # Don't focus windows from other workspaces
        self.workspace.remove_window(self.window)
        self.workspace.focus(self.window)
        self.assertIsNone(self.workspace.focused)
        self.assertFalse(self.window.focused)

        # But focus windows from the current workspace
        self.workspace.add_window(self.window)
        self.workspace.focus(self.window)
        self.assertEqual(self.workspace.focused, self.window)
        self.assertTrue(self.window.focused)

    def test_find_window(self):
        (win, ws) = pwm.workspaces.find_window(self.window.wid)

        self.assertEqual(win, self.window)
        self.assertEqual(ws, self.workspace)

    def test_show(self):
        self.workspace.show()

        self.assertTrue(self.workspace.active)
        self.assertTrue(self.window.visible)
        self.assertTrue(self.workspace.bar.visible)

    def test_hide(self):
        self.workspace.hide()

        self.assertFalse(self.workspace.active)
        self.assertFalse(self.window.visible)
        self.assertFalse(self.workspace.bar.visible)
