# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest
from unittest.mock import patch

from pwm.config import config
import pwm.layout
import pwm.workspaces
import test.util as util


class TestTiling(unittest.TestCase):
    def setUp(self):
        util.setup()
        self.tiling = pwm.layout.Tiling(pwm.workspaces.current())

        self.wid = [util.create_window(manage=False) for wid in range(10)]

    def tearDown(self):
        util.tear_down()

    def test_init(self):
        self.assertEqual(len(self.tiling.columns), 1)
        self.assertEqual(self.tiling.columns[0].size, 1.0)
        self.assertEqual(len(self.tiling.columns[0].windows), 0)

    def test_add_window(self):
        wid = self.wid[0]
        self.tiling.add_window(wid)

        self.assertEqual(len(self.tiling.columns[0].windows), 1)
        self.assertEqual(self.tiling.columns[0].windows[0].wid, wid)

    def test_add_window_set_column(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.assertEqual(self.tiling.path(self.wid[1]), (1, 0))

    def test_add_window_set_row(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.add_window(self.wid[2], 0, 1)
        self.assertEqual(self.tiling.path(self.wid[2]), (0, 1))

    def test_add_window_set_last_row(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.add_window(self.wid[2], 0, -1)
        self.assertEqual(self.tiling.path(self.wid[2]), (0, 2))

    def test_remove_window(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.remove_window(self.wid[0])
        self.assertEqual(len(self.tiling.columns[0].windows), 0)

    def test_remove_window_remove_column(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.tiling.remove_window(self.wid[1])
        self.assertEqual(len(self.tiling.columns), 1)

    def test_remove_window_remove_last_column(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.remove_window(self.wid[0])
        self.assertEqual(len(self.tiling.columns), 1)

    def test_path(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.tiling.add_window(self.wid[2], 1)
        self.assertEqual(self.tiling.path(self.wid[2]), (1, 1))

    def test_move_up(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])

        self.tiling.move(self.wid[1], "up")
        self.assertEqual(self.tiling.path(self.wid[1]), (0, 0))
        self.assertEqual(self.tiling.path(self.wid[0]), (0, 1))

    def test_move_up_top(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.move(self.wid[0], "up")
        self.assertEqual(self.tiling.path(self.wid[0]), (0, 0))

    def test_move_down(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])

        self.tiling.move(self.wid[0], "down")
        self.assertEqual(self.tiling.path(self.wid[1]), (0, 0))
        self.assertEqual(self.tiling.path(self.wid[0]), (0, 1))

    def test_move_down_bottom(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])

        self.tiling.move(self.wid[1], "down")
        self.assertEqual(self.tiling.path(self.wid[1]), (0, 1))

    def test_move_left(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.move(self.wid[0], "left")
        self.assertEqual(self.tiling.path(self.wid[0]), (0, 0))
        self.assertEqual(self.tiling.path(self.wid[1]), (1, 0))

    def test_move_left_at_border(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.tiling.move(self.wid[0], "left")
        self.assertEqual(self.tiling.path(self.wid[0]), (0, 0))

    def test_move_left_merge(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.tiling.move(self.wid[1], "left")
        self.assertEqual(self.tiling.path(self.wid[0]), (0, 0))
        self.assertEqual(self.tiling.path(self.wid[1]), (0, 1))
        self.assertEqual(len(self.tiling.columns), 1)

    def test_move_left_merge_remove_column(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.tiling.move(self.wid[1], "left")
        self.assertEqual(len(self.tiling.columns), 1)

    def test_move_left_resize_rows(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.add_window(self.wid[2])
        self.tiling.add_window(self.wid[3], 1)
        self.tiling.add_window(self.wid[4], 1)

        self.tiling.move(self.wid[3], "left")
        path = self.tiling.path(self.wid[3])

        self.assertEqual(self.tiling.columns[path[0]].windows[path[1]].size,
                         0.25)
        self.assertEqual(self.tiling.columns[1].windows[0].size, 1.0)

    def test_move_left_resize_columns(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.move(self.wid[0], "left")

        self.assertEqual(self.tiling.columns[0].size, 0.5)
        self.assertEqual(self.tiling.columns[1].size, 0.5)

    def test_move_right(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.move(self.wid[0], "right")
        self.assertEqual(self.tiling.path(self.wid[0]), (1, 0))
        self.assertEqual(self.tiling.path(self.wid[1]), (0, 0))

    def test_move_right_at_border(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.tiling.move(self.wid[1], "right")
        self.assertEqual(self.tiling.path(self.wid[1]), (1, 0))

    def test_move_right_merge(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.tiling.move(self.wid[0], "right")
        self.assertEqual(self.tiling.path(self.wid[0]), (0, 1))
        self.assertEqual(self.tiling.path(self.wid[1]), (0, 0))

    def test_move_right_merge_remove_column(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.tiling.move(self.wid[0], "right")
        self.assertEqual(len(self.tiling.columns), 1)

    def test_move_right_resize_rows(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.add_window(self.wid[2])
        self.tiling.add_window(self.wid[3])
        self.tiling.add_window(self.wid[4], 1)

        self.tiling.move(self.wid[3], "right")
        path = self.tiling.path(self.wid[3])

        self.assertEqual(self.tiling.columns[path[0]].windows[path[1]].size,
                         0.5)
        self.assertEqual(self.tiling.columns[0].windows[0].size, 1.0/3)

    def test_move_right_resize_columns(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.move(self.wid[1], "right")

        self.assertEqual(self.tiling.columns[0].size, 0.5)
        self.assertEqual(self.tiling.columns[1].size, 0.5)

    def test_relative_above_topmost(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.assertEqual(self.tiling.relative(self.wid[0], "above"),
                         self.wid[0])

    def test_above(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.add_window(self.wid[2])
        self.assertEqual(self.tiling.relative(self.wid[1], "above"),
                         self.wid[0])

    def test_below_bottommost(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.assertEqual(self.tiling.relative(self.wid[1], "below"),
                         self.wid[1])

    def test_below(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.add_window(self.wid[2])
        self.assertEqual(self.tiling.relative(self.wid[1], "below"),
                         self.wid[2])

    def test_left_leftmost(self):
        self.tiling.add_window(self.wid[0])
        self.assertEqual(self.tiling.relative(self.wid[0], "left"),
                         self.wid[0])

    def test_left(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.assertEqual(self.tiling.relative(self.wid[1], "left"),
                         self.wid[0])

    def test_left_uneven(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.tiling.add_window(self.wid[2], 1)
        self.assertEqual(self.tiling.relative(self.wid[2], "left"),
                         self.wid[0])

    def test_right_rightmost(self):
        self.tiling.add_window(self.wid[0])
        self.assertEqual(self.tiling.relative(self.wid[0], "right"),
                         self.wid[0])

    def test_right(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)
        self.assertEqual(self.tiling.relative(self.wid[0], "right"),
                         self.wid[1])

    def test_right_uneven(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])
        self.tiling.add_window(self.wid[2], 1)
        self.assertEqual(self.tiling.relative(self.wid[0], "right"),
                         self.wid[2])

    def test_make_row_space_one(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.make_row_space(0, 0.3)
        self.assertEqual(self.tiling.columns[0].windows[0].size, 0.7)

    def test_make_row_space_two(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])

        column = self.tiling.columns[0]
        column.windows[0].size = 0.8
        column.windows[1].size = 0.2

        self.tiling.make_row_space(0, 0.4)
        self.assertAlmostEqual(column.windows[0].size, 0.8-(0.8*0.4))
        self.assertAlmostEqual(column.windows[1].size, 0.2-(0.2*0.4))

    def test_distribute_free_row_space(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])

        column = self.tiling.columns[0]
        column.windows[0].size = 0.6
        column.windows[1].size = 0.2

        self.tiling.distribute_free_row_space(0)
        self.assertAlmostEqual(column.windows[0].size, 0.6+(0.2*0.6/0.8))
        self.assertAlmostEqual(column.windows[1].size, 0.2+(0.2*0.2/0.8))

    def test_make_column_space_one(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.make_column_space(0.3)
        self.assertEqual(self.tiling.columns[0].size, 0.7)

    def test_make_column_space_two(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)

        columns = self.tiling.columns
        columns[0].size = 0.8
        columns[1].size = 0.2

        self.tiling.make_column_space(0.4)
        self.assertAlmostEqual(columns[0].size, 0.8-(0.8*0.4))
        self.assertAlmostEqual(columns[1].size, 0.2-(0.2*0.4))

    def test_distribute_free_column_space(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)

        columns = self.tiling.columns
        columns[0].size = 0.6
        columns[1].size = 0.2

        self.tiling.distribute_free_column_space()
        self.assertAlmostEqual(columns[0].size, 0.6+(0.2*0.6/0.8))
        self.assertAlmostEqual(columns[1].size, 0.2+(0.2*0.2/0.8))

    def test_resize_column(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1], 1)

        self.tiling.columns[0].size = 0.5
        self.tiling.columns[1].size = 0.5

        self.tiling.resize(self.wid[0], (0.3, 0))
        self.assertAlmostEqual(self.tiling.columns[0].size, 0.8)
        self.assertAlmostEqual(self.tiling.columns[1].size, 0.2)

    def test_resize_column_single(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.resize(self.wid[0], (0.3, 0))
        self.assertAlmostEqual(self.tiling.columns[0].size, 1.0)

    def test_resize_row(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.add_window(self.wid[1])

        windows = self.tiling.columns[0].windows
        windows[0].size = 0.5
        windows[0].size = 0.5

        self.tiling.resize(self.wid[0], (0.0, 0.3))
        self.assertAlmostEqual(windows[0].size, 0.8)
        self.assertAlmostEqual(windows[1].size, 0.2)

    def test_resize_row_single(self):
        self.tiling.add_window(self.wid[0])
        self.tiling.resize(self.wid[0], (0, 0.3))
        self.assertAlmostEqual(self.tiling.columns[0].windows[0].size, 1.0)


class TestFloating(unittest.TestCase):
    def setUp(self):
        util.setup()
        self.floating = pwm.layout.Floating(pwm.workspaces.current())

    def tearDown(self):
        util.tear_down()

    def test_add_window(self):
        wid = util.create_window(floating=True)
        self.floating.add_window(wid)
        self.assertIn(wid, self.floating.windows)

    def test_remove_window(self):
        wid = util.create_window(floating=True)
        self.floating.add_window(wid)
        self.floating.remove_window(wid)
        self.assertNotIn(wid, self.floating.windows)

    def test_delta(self):
        self.assertEqual(self.floating._delta("left", 10), (-10, 0))
        self.assertEqual(self.floating._delta("right", 10), (10, 0))
        self.assertEqual(self.floating._delta("up", 10), (0, -10))
        self.assertEqual(self.floating._delta("down", 10), (0, 10))

    def test_move(self):
        wid = util.create_window(floating=True)

        def _test_move(direction, relpos):
            x, y = 0, 0
            pwm.windows.configure(wid, x=x, y=y)
            self.floating.move(wid, direction)
            nx, ny, _, _ = pwm.windows.get_geometry(wid)
            self.assertEqual((nx, ny),
                             (round(x+relpos[0]), round(y+relpos[1])))

        speedx = config.window.move_speed*self.floating.workspace.width
        speedy = config.window.move_speed*self.floating.workspace.height
        _test_move("right", (speedx, 0))
        _test_move("left", (-speedx, 0))
        _test_move("up", (0, -speedy))
        _test_move("down", (0, speedy))

    def test_resize(self):
        wid = util.create_window(floating=True)
        _, _, width, height = pwm.windows.get_geometry(wid)

        self.floating.resize(wid, (0.02, 0.03))

        _, _, new_width, new_height = pwm.windows.get_geometry(wid)
        ws = pwm.workspaces.current()
        self.assertEqual(
            (new_width, new_height),
            (round(width+ws.width*0.02), round(height+ws.height*0.03)))


class TestFullscreen(unittest.TestCase):
    def setUp(self):
        util.setup()
        self.fullscreen = pwm.layout.Fullscreen(pwm.workspaces.current())

    def tearDown(self):
        util.tear_down()

    def test_add_window(self):
        wid = util.create_window()
        self.fullscreen.add_window(wid)
        self.assertIn(wid, self.fullscreen.windows)

    def test_remove_window(self):
        wid = util.create_window()
        self.fullscreen.add_window(wid)
        self.fullscreen.remove_window(wid)
        self.assertNotIn(wid, self.fullscreen.windows)

    def test_add_window_flag(self):
        wid = util.create_window()
        self.fullscreen.add_window(wid)
        self.assertTrue(pwm.windows.managed[wid].fullscreen)

    def test_remove_window_flag(self):
        wid = util.create_window()
        self.fullscreen.add_window(wid)
        self.fullscreen.remove_window(wid)
        self.assertFalse(pwm.windows.managed[wid].fullscreen)

    def test_add_window_configure(self):
        wid = util.create_window()

        with patch.object(pwm.windows, "configure") as conf:
            self.fullscreen.add_window(wid)

        conf.assert_called_once()
