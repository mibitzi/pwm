# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import unittest

import pwm.layout
import pwm.workspaces
import test.util as util


class TestLayout(unittest.TestCase):
    def setUp(self):
        util.setup()
        self.layout = pwm.layout.Layout(pwm.workspaces.current())

        self.wid = [util.create_window(manage=False) for wid in range(10)]

    def tearDown(self):
        util.tear_down()

    def test_init(self):
        self.assertEqual(len(self.layout.columns), 1)
        self.assertEqual(self.layout.columns[0].size, 1.0)
        self.assertEqual(len(self.layout.columns[0].windows), 0)

    def test_add_window(self):
        wid = self.wid[0]
        self.layout.add_window(wid)

        self.assertEqual(len(self.layout.columns[0].windows), 1)
        self.assertEqual(self.layout.columns[0].windows[0].wid, wid)

    def test_add_window_set_column(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.assertEqual(self.layout.path(self.wid[1]), (1, 0))

    def test_add_window_set_row(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.add_window(self.wid[2], 0, 1)
        self.assertEqual(self.layout.path(self.wid[2]), (0, 1))

    def test_add_window_set_last_row(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.add_window(self.wid[2], 0, -1)
        self.assertEqual(self.layout.path(self.wid[2]), (0, 2))

    def test_remove_window(self):
        self.layout.add_window(self.wid[0])
        self.layout.remove_window(self.wid[0])
        self.assertEqual(len(self.layout.columns[0].windows), 0)

    def test_remove_window_remove_column(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.layout.remove_window(self.wid[1])
        self.assertEqual(len(self.layout.columns), 1)

    def test_remove_window_remove_last_column(self):
        self.layout.add_window(self.wid[0])
        self.layout.remove_window(self.wid[0])
        self.assertEqual(len(self.layout.columns), 1)

    def test_path(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.layout.add_window(self.wid[2], 1)
        self.assertEqual(self.layout.path(self.wid[2]), (1, 1))

    def test_move_up(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])

        self.layout.move_up(self.wid[1])
        self.assertEqual(self.layout.path(self.wid[1]), (0, 0))
        self.assertEqual(self.layout.path(self.wid[0]), (0, 1))

    def test_move_up_top(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.move_up(self.wid[0])
        self.assertEqual(self.layout.path(self.wid[0]), (0, 0))

    def test_move_down(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])

        self.layout.move_down(self.wid[0])
        self.assertEqual(self.layout.path(self.wid[1]), (0, 0))
        self.assertEqual(self.layout.path(self.wid[0]), (0, 1))

    def test_move_down_bottom(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])

        self.layout.move_down(self.wid[1])
        self.assertEqual(self.layout.path(self.wid[1]), (0, 1))

    def test_move_left(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.move_left(self.wid[0])
        self.assertEqual(self.layout.path(self.wid[0]), (0, 0))
        self.assertEqual(self.layout.path(self.wid[1]), (1, 0))

    def test_move_left_at_border(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.layout.move_left(self.wid[0])
        self.assertEqual(self.layout.path(self.wid[0]), (0, 0))

    def test_move_left_merge(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.layout.move_left(self.wid[1])
        self.assertEqual(self.layout.path(self.wid[0]), (0, 0))
        self.assertEqual(self.layout.path(self.wid[1]), (0, 1))
        self.assertEqual(len(self.layout.columns), 1)

    def test_move_left_merge_remove_column(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.layout.move_left(self.wid[1])

    def test_move_right(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.move_right(self.wid[0])
        self.assertEqual(self.layout.path(self.wid[0]), (1, 0))
        self.assertEqual(self.layout.path(self.wid[1]), (0, 0))

    def test_move_right_at_border(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.layout.move_right(self.wid[1])
        self.assertEqual(self.layout.path(self.wid[1]), (1, 0))

    def test_move_right_merge(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.layout.move_right(self.wid[0])
        self.assertEqual(self.layout.path(self.wid[0]), (0, 1))
        self.assertEqual(self.layout.path(self.wid[1]), (0, 0))

    def test_move_right_merge_remove_column(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.layout.move_right(self.wid[0])
        self.assertEqual(len(self.layout.columns), 1)
