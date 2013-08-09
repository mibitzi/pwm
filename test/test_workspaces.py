# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest
from unittest.mock import create_autospec, patch

from pwm.ffi.xcb import xcb
import pwm.bar
import pwm.workspaces
import pwm.windows
from pwm.config import config
import test.util as util


class TestWorkspace(unittest.TestCase):
    def setUp(self):
        util.setup()
        self.workspace = pwm.workspaces.current()
        self.workspace.tiling = create_autospec(self.workspace.tiling)
        self.workspace.floating = create_autospec(self.workspace.floating)
        self.workspace.fullscreen = create_autospec(self.workspace.fullscreen)

        self.tiling = self.workspace.tiling
        self.tiling.path.return_value = (0, 0)
        self.floating = self.workspace.floating
        self.fullscreen = self.workspace.fullscreen

    def tearDown(self):
        util.tear_down()

    def test_geometry(self):
        self.assertEqual(self.workspace.x, 0)
        self.assertEqual(self.workspace.y, pwm.bar.primary.height)
        self.assertEqual(self.workspace.width, xcb.screen.width_in_pixels)
        self.assertEqual(
            self.workspace.height,
            xcb.screen.height_in_pixels - pwm.bar.primary.height)

    def test_add_window_fullscreen(self):
        wid = util.create_window(manage=False, fullscreen=True)
        self.workspace.add_window(wid)
        self.fullscreen.add_window.assert_called_once_with(wid)

    def test_add_window_floating(self):
        wid = util.create_window(floating=True)
        self.floating.add_window.assert_called_once_with(wid)

    def test_add_window_tiling_empty(self):
        window = util.create_window()
        self.tiling.add_window.assert_called_once_with(window, 0, -1)

    def test_add_window_tiling_below_focus(self):
        wid = util.create_window()
        util.create_window(floating=True)

        self.tiling.add_window.reset_mock()
        with patch.object(self.tiling, "path", return_value=(1, 2)) as path:
            window = util.create_window()

        path.assert_called_once_with(wid)
        self.tiling.add_window.assert_called_once_with(window, 1, 3)

    def test_add_window_added(self):
        window = util.create_window()
        self.assertIn(window, self.workspace.windows)

    def test_add_window_map_if_current(self):
        window = util.create_window()
        self.assertTrue(pwm.windows.is_mapped(window))

    def test_add_window_dont_map_if_not_current(self):
        window = util.create_window(manage=False)
        pwm.workspaces.switch(1)
        self.workspace.add_window(window)
        self.assertFalse(pwm.windows.is_mapped(window))

    def test_remove_window(self):
        win = util.create_window(manage=False)
        self.workspace.add_window(win)
        self.workspace.remove_window(win)
        self.assertNotIn(win, self.workspace.windows)

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
        self.assertEqual(pwm.windows.managed[wid].ignore_unmaps, 1)

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

    def test_toggle_floating_floating(self):
        wid = util.create_window(floating=True)
        self.workspace.toggle_floating(wid)
        self.floating.remove_window.assert_called_once_with(wid)
        self.tiling.add_window.assert_called_once_with(wid)

    def test_toggle_floating_tiling(self):
        wid = util.create_window()
        self.workspace.toggle_floating(wid)
        self.tiling.remove_window.assert_called_once_with(wid)
        self.floating.add_window.assert_called_once_with(wid)

    def test_toggle_focus_layer(self):
        wid_float = util.create_window(floating=True)
        util.create_window()

        with patch.object(pwm.windows, "focus") as focus:
            self.workspace.toggle_focus_layer()

        focus.assert_called_once_with(wid_float)

    def test_toggle_fullscreen_add(self):
        wid = util.create_window()

        with patch.object(self.workspace, "add_fullscreen") as add:
            self.workspace.toggle_fullscreen(wid)

        add.assert_called_once_with(wid)

    def test_toggle_fullscreen_remove(self):
        wid = util.create_window()
        pwm.windows.managed[wid].fullscreen = True

        with patch.object(self.workspace, "remove_fullscreen") as rem:
            self.workspace.toggle_fullscreen(wid)

        rem.assert_called_once_with(wid)

    def test_add_fullscreen(self):
        wid = util.create_window()
        self.workspace.add_fullscreen(wid)
        self.fullscreen.add_window.assert_called_once_with(wid)

    def test_add_fullscreen_remove(self):
        wid = util.create_window(floating=True)

        with patch.object(self.workspace, "_proxy_layout") as proxy:
            self.workspace.add_fullscreen(wid)
        proxy.assert_called_once_with("remove_window", wid)

    def test_remove_fullscreen(self):
        wid = util.create_window(fullscreen=True)
        self.workspace.remove_fullscreen(wid)
        self.fullscreen.remove_window.assert_called_once_with(wid)

    def test_remove_fullscreen_add_tiling(self):
        wid = util.create_window(fullscreen=True)
        self.tiling.reset_mock()
        self.workspace.remove_fullscreen(wid)
        self.tiling.add_window.assert_called_once_with(wid)

    def test_remove_fullscreen_add_floating(self):
        wid = util.create_window(floating=True, fullscreen=True)
        self.floating.reset_mock()
        self.workspace.remove_fullscreen(wid)
        self.floating.add_window.assert_called_once_with(wid)


class TestWorkspaces(unittest.TestCase):
    def setUp(self):
        util.setup()

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

    def test_switch(self):
        pwm.workspaces.switch(1)
        self.assertEqual(pwm.workspaces.current(),
                         pwm.workspaces.workspaces[1])

    def test_switch_focus(self):
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

    def test_send_window_to(self):
        wid = util.create_window()
        pwm.workspaces.send_window_to(wid, 1)
        self.assertIn(wid, pwm.workspaces.workspaces[1].windows)

    def test_send_window_to_ignore_unmap(self):
        wid = util.create_window()
        pwm.workspaces.send_window_to(wid, 1)
        self.assertEqual(pwm.windows.managed[wid].ignore_unmaps, 1)

    def test_send_window_to_focus(self):
        wid = util.create_window()
        pwm.workspaces.send_window_to(wid, 1)
        self.assertIsNone(pwm.windows.focused)

    def test_send_window_to_unmap(self):
        wid = util.create_window()
        pwm.workspaces.send_window_to(wid, 1)
        self.assertFalse(pwm.windows.is_mapped(wid))
