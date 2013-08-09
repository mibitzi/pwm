# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

import pwm.xutil
import pwm.systray
import pwm.events
import test.util as util


class TestEvent(unittest.TestCase):
    def test_fire(self):
        cnt = 0

        def _handler():
            nonlocal cnt
            cnt += 1

        ev = pwm.events.Event()
        ev.add(_handler)
        ev()

        self.assertEqual(cnt, 1)


class TestHandlerList(unittest.TestCase):
    def test_add(self):

        def _handler():
            pass

        event = pwm.events.Event()
        hlist = pwm.events.HandlerList()
        hlist.add(event, _handler)
        self.assertIn((event, _handler), hlist.handlers)
        self.assertIn(_handler, event)

    def test_destroy(self):
        def _handler():
            pass

        event = pwm.events.Event()
        hlist = pwm.events.HandlerList()
        hlist.add(event, _handler)
        hlist.destroy()
        self.assertEqual(len(hlist.handlers), 0)
        self.assertNotIn(_handler, event)


class TestEvents(unittest.TestCase):
    def setUp(self):
        util.setup()

    def tearDown(self):
        util.tear_down()

    def test_handle_unmap(self):
        wid = util.create_window()

        with patch.object(pwm.windows, "unmanage") as unmanage:
            pwm.events.handle_unmap(wid)

        unmanage.assert_called_once_with(wid)

    def test_handle_unmap_ignore(self):
        wid = util.create_window()
        pwm.windows.managed[wid].ignore_unmaps = 1
        pwm.events.handle_unmap(wid)
        self.assertEqual(pwm.windows.managed[wid].ignore_unmaps, 0)

    def test_handle_configure_request_floating(self):
        wid = util.create_window(floating=True)
        event = MagicMock()
        event.window = wid

        with patch.object(pwm.windows, "configure") as conf:
            pwm.events.handle_configure_request(event)

        conf.assert_called_once()

    def test_handle_configure_request_tiling(self):
        wid = util.create_window()
        event = MagicMock()
        event.window = wid

        with patch.object(pwm.windows.managed[wid].workspace.tiling,
                          "arrange") as arr:
            pwm.events.handle_configure_request(event)

        arr.assert_called_once_with(wid)

    def test_handle_property_notify_xembed(self):
        event = MagicMock()
        event.atom = pwm.xutil.get_atom("_XEMBED_INFO")

        with patch.object(pwm.systray, "handle_property_notify") as handle:
            pwm.events.handle_property_notify(event)

        handle.assert_called_once_with(event)

    def test_handle_property_notify_name(self):
        wid = util.create_window()
        event = MagicMock()
        event.atom = pwm.xutil.get_atom("_NET_WM_NAME")
        event.window = wid

        with patch.object(pwm.events, "window_name_changed") as ev:
            pwm.events.handle_property_notify(event)

        ev.assert_called_once_with(wid)

    def _test_wm_state_fullscreen(self, wid, action):
        event = MagicMock()
        event.format = 32
        event.data.data32 = [action,
                             pwm.xutil.get_atom("_NET_WM_STATE_FULLSCREEN")]
        event.window = wid

        with patch.object(pwm.windows.managed[wid].workspace,
                          "toggle_fullscreen") as toggle:
            pwm.events.handle_wm_state(event)

        toggle.assert_called_once_with(wid)

    def test_handle_wm_state_add_fullscreen(self):
        wid = util.create_window()
        self._test_wm_state_fullscreen(wid, pwm.xutil._NET_WM_STATE_ADD)

    def test_handle_wm_state_remove_fullscreen(self):
        wid = util.create_window()
        pwm.windows.managed[wid].fullscreen = True
        self._test_wm_state_fullscreen(wid, pwm.xutil._NET_WM_STATE_REMOVE)

    def test_handle_wm_state_toggle_fullscreen(self):
        wid = util.create_window()
        self._test_wm_state_fullscreen(wid, pwm.xutil._NET_WM_STATE_TOGGLE)
