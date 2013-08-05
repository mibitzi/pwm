# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import unittest
from unittest.mock import patch

import pwm
import pwm.commands
import pwm.spawn
import pwm.menu
import test.util as util


class TestCommands(unittest.TestCase):
    def setUp(self):
        util.setup()

    def tearDown(self):
        util.tear_down()

    def test_quit(self):
        pwm.commands.quit()
        self.assertTrue(pwm.shutdown)

    def test_restart(self):
        pwm.commands.restart()
        self.assertTrue(pwm.shutdown)
        self.assertTrue(pwm.restart)

    @patch.object(pwm.workspaces, "switch")
    def test_switch_workspace(self, switch):
        pwm.commands.switch_workspace(1)
        switch.assert_called_once_with(1)

    @patch.object(pwm.windows, "kill")
    def test_kill(self, kill):
        wid = util.create_window()
        pwm.commands.kill()
        kill.assert_called_once_with(wid)

    @patch.object(pwm.spawn, "spawn")
    def test_spawn(self, spawn):
        pwm.commands.spawn("firefox")
        spawn.assert_called_once_with("firefox")

    def test_move(self):
        wid = util.create_window()
        ws = pwm.workspaces.current()

        def _test_direction(direction):
            with patch.object(ws, "move_window") as move:
                pwm.commands.move(direction)

            move.assert_called_once_with(wid, direction)

        for d in ["up", "down", "left", "right"]:
            _test_direction(d)

    def test_focus(self):
        wid = util.create_window()
        ws = pwm.workspaces.current()

        def _test_focus(pos):
            with patch.object(ws, "focus_relative") as focus:
                pwm.commands.focus(pos)

            focus.assert_called_once_with(wid, pos)

        for pos in ["above", "below", "left", "right"]:
            _test_focus(pos)

    def test_resize(self):
        wid = util.create_window()
        ws = pwm.workspaces.current()

        with patch.object(ws, "resize_window") as resize:
            pwm.commands.resize((0.1, 0.1))

        resize.assert_called_once_with(wid, (0.1, 0.1))

    @patch.object(pwm.workspaces, "send_window_to")
    def test_send_to_workspace(self, send):
        wid = util.create_window()
        pwm.commands.send_to_workspace(1)
        send.assert_called_once_with(wid, 1)

    def test_toggle_floating(self):
        wid = util.create_window()
        ws = pwm.workspaces.current()

        with patch.object(ws, "toggle_floating") as toggle:
            pwm.commands.toggle_floating()
        toggle.assert_called_once_with(wid)

    @patch.object(pwm.menu, "show")
    def test_menu(self, menu):
        pwm.commands.menu()
        menu.assert_called_once_with()
