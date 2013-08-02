# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import unittest

from pwm.ffi.xcb import xcb
import pwm.bar
import pwm.workspaces
import pwm.windows
from pwm.config import config
import test.util as util


class TestWorkspaces(unittest.TestCase):
    def setUp(self):
        util.setup()
        self.workspace = pwm.workspaces.current()

    def tearDown(self):
        util.tear_down()

    def test_setup(self):
        # setup() was already called in setUp

        self.assertEqual(len(pwm.workspaces.workspaces), config.workspaces)
        self.assertEqual(pwm.workspaces.current(),
                         pwm.workspaces.workspaces[0])

    def test_destroy(self):
        pwm.workspaces.destroy()
        self.assertEqual(len(pwm.workspaces.workspaces), 0)

    def test_geometry(self):
        self.assertEqual(self.workspace.x, 0)
        self.assertEqual(self.workspace.y, pwm.bar.primary.height)
        self.assertEqual(self.workspace.width, xcb.screen.width_in_pixels)
        self.assertEqual(
            self.workspace.height,
            xcb.screen.height_in_pixels - pwm.bar.primary.height)

    def test_add_window(self):
        window = util.create_window()
        self.assertEqual(len(self.workspace.windows), 1)
        self.assertTrue(window in self.workspace.windows)

    def test_add_window_show(self):
        window = util.create_window()
        self.assertTrue(pwm.windows.is_mapped(window))

    def test_add_window_show_not_current(self):
        wid = util.create_window(manage=False)
        pwm.workspaces.workspaces[1].add_window(wid)
        self.assertFalse(pwm.windows.is_mapped(wid))

    def test_remove_window(self):
        win = util.create_window(manage=False)
        self.workspace.add_window(win)
        self.workspace.remove_window(win)
        self.assertEqual(len(self.workspace.windows), 0)

    def test_show(self):
        wid = util.create_window()

        self.workspace.hide()
        self.workspace.show()
        self.assertTrue(pwm.windows.is_mapped(wid))

    def test_hide(self):
        wid = util.create_window()
        self.workspace.hide()
        self.assertFalse(pwm.windows.is_mapped(wid))

    def test_hide_ignore_unmaps(self):
        wid = util.create_window()
        self.workspace.hide()
        self.assertEqual(pwm.windows.ignore_unmaps[wid], 1)

    def test_top_focus_priority(self):
        wid1 = util.create_window()
        wid2 = util.create_window()
        wid3 = util.create_window()

        self.workspace.handle_focus(wid1)
        self.workspace.handle_focus(wid2)
        self.workspace.handle_focus(wid3)
        self.assertEqual(self.workspace.top_focus_priority(), wid3)

        self.workspace.handle_focus(wid2)
        self.assertEqual(self.workspace.top_focus_priority(), wid2)

    def test_handle_focus(self):
        wid1 = util.create_window()
        wid2 = util.create_window()
        wid3 = util.create_window()

        self.workspace.handle_focus(wid1)
        self.assertEqual(self.workspace.windows, [wid2, wid3, wid1])

        self.workspace.handle_focus(wid3)
        self.assertEqual(self.workspace.windows, [wid2, wid1, wid3])

    def test_switch_workspace(self):
        pwm.workspaces.switch(1)
        self.assertEqual(pwm.workspaces.current(),
                         pwm.workspaces.workspaces[1])

    def test_switch_workspace_focus(self):
        util.create_window()
        pwm.workspaces.switch(1)

        self.assertEqual(pwm.windows.focused, None)

    def test_opened(self):
        # Create window on current workspace (idx=0)
        util.create_window()

        pwm.workspaces.switch(5)

        active = [i for i in pwm.workspaces.opened()]

        self.assertEqual(len(active), 2)
        self.assertEqual(active[0][0], 0)
        self.assertEqual(active[1][0], 5)
