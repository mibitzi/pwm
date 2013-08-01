# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

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
        self.assertEqual(len(self.layout.columns), 1)

    def test_move_left_resize_rows(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.add_window(self.wid[2])
        self.layout.add_window(self.wid[3], 1)
        self.layout.add_window(self.wid[4], 1)

        self.layout.move_left(self.wid[3])
        path = self.layout.path(self.wid[3])

        self.assertEqual(self.layout.columns[path[0]].windows[path[1]].size,
                         0.25)
        self.assertEqual(self.layout.columns[1].windows[0].size, 1.0)

    def test_move_left_resize_columns(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.move_left(self.wid[0])

        self.assertEqual(self.layout.columns[0].size, 0.5)
        self.assertEqual(self.layout.columns[1].size, 0.5)

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

    def test_move_right_resize_rows(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.add_window(self.wid[2])
        self.layout.add_window(self.wid[3])
        self.layout.add_window(self.wid[4], 1)

        self.layout.move_right(self.wid[3])
        path = self.layout.path(self.wid[3])

        self.assertEqual(self.layout.columns[path[0]].windows[path[1]].size,
                         0.5)
        self.assertEqual(self.layout.columns[0].windows[0].size, 1.0/3)

    def test_move_right_resize_columns(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.move_right(self.wid[1])

        self.assertEqual(self.layout.columns[0].size, 0.5)
        self.assertEqual(self.layout.columns[1].size, 0.5)

    def test_above_topmost(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.assertEqual(self.layout.above(self.wid[0]), self.wid[0])

    def test_above(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.add_window(self.wid[2])
        self.assertEqual(self.layout.above(self.wid[1]), self.wid[0])

    def test_below_bottommost(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.assertEqual(self.layout.below(self.wid[1]), self.wid[1])

    def test_below(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.add_window(self.wid[2])
        self.assertEqual(self.layout.below(self.wid[1]), self.wid[2])

    def test_left_leftmost(self):
        self.layout.add_window(self.wid[0])
        self.assertEqual(self.layout.left(self.wid[0]), self.wid[0])

    def test_left(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.assertEqual(self.layout.left(self.wid[1]), self.wid[0])

    def test_left_uneven(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.layout.add_window(self.wid[2], 1)
        self.assertEqual(self.layout.left(self.wid[2]), self.wid[0])

    def test_right_rightmost(self):
        self.layout.add_window(self.wid[0])
        self.assertEqual(self.layout.right(self.wid[0]), self.wid[0])

    def test_right(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)
        self.assertEqual(self.layout.right(self.wid[0]), self.wid[1])

    def test_right_uneven(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])
        self.layout.add_window(self.wid[2], 1)
        self.assertEqual(self.layout.right(self.wid[0]), self.wid[2])

    def test_make_row_space_one(self):
        self.layout.add_window(self.wid[0])
        self.layout.make_row_space(0, 0.3)
        self.assertEqual(self.layout.columns[0].windows[0].size, 0.7)

    def test_make_row_space_two(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])

        column = self.layout.columns[0]
        column.windows[0].size = 0.8
        column.windows[1].size = 0.2

        self.layout.make_row_space(0, 0.4)
        self.assertAlmostEqual(column.windows[0].size, 0.8-(0.8*0.4))
        self.assertAlmostEqual(column.windows[1].size, 0.2-(0.2*0.4))

    def test_distribute_free_row_space(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])

        column = self.layout.columns[0]
        column.windows[0].size = 0.6
        column.windows[1].size = 0.2

        self.layout.distribute_free_row_space(0)
        self.assertAlmostEqual(column.windows[0].size, 0.6+(0.2*0.6/0.8))
        self.assertAlmostEqual(column.windows[1].size, 0.2+(0.2*0.2/0.8))

    def test_make_column_space_one(self):
        self.layout.add_window(self.wid[0])
        self.layout.make_column_space(0.3)
        self.assertEqual(self.layout.columns[0].size, 0.7)

    def test_make_column_space_two(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)

        columns = self.layout.columns
        columns[0].size = 0.8
        columns[1].size = 0.2

        self.layout.make_column_space(0.4)
        self.assertAlmostEqual(columns[0].size, 0.8-(0.8*0.4))
        self.assertAlmostEqual(columns[1].size, 0.2-(0.2*0.4))

    def test_distribute_free_column_space(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)

        columns = self.layout.columns
        columns[0].size = 0.6
        columns[1].size = 0.2

        self.layout.distribute_free_column_space()
        self.assertAlmostEqual(columns[0].size, 0.6+(0.2*0.6/0.8))
        self.assertAlmostEqual(columns[1].size, 0.2+(0.2*0.2/0.8))

    def test_resize_column(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1], 1)

        self.layout.columns[0].size = 0.5
        self.layout.columns[1].size = 0.5

        self.layout.resize(self.wid[0], (0.3, 0))
        self.assertAlmostEqual(self.layout.columns[0].size, 0.8)
        self.assertAlmostEqual(self.layout.columns[1].size, 0.2)

    def test_resize_column_single(self):
        self.layout.add_window(self.wid[0])
        self.layout.resize(self.wid[0], (0.3, 0))
        self.assertAlmostEqual(self.layout.columns[0].size, 1.0)

    def test_resize_row(self):
        self.layout.add_window(self.wid[0])
        self.layout.add_window(self.wid[1])

        windows = self.layout.columns[0].windows
        windows[0].size = 0.5
        windows[0].size = 0.5

        self.layout.resize(self.wid[0], (0.0, 0.3))
        self.assertAlmostEqual(windows[0].size, 0.8)
        self.assertAlmostEqual(windows[1].size, 0.2)

    def test_resize_row_single(self):
        self.layout.add_window(self.wid[0])
        self.layout.resize(self.wid[0], (0, 0.3))
        self.assertAlmostEqual(self.layout.columns[0].windows[0].size, 1.0)
