# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

from __future__ import division, absolute_import, print_function

import unittest

import test.util as util
import pwm.scheduler


class TestState(unittest.TestCase):
    def setUp(self):
        util.setup()

    def tearDown(self):
        util.tear_down()

    def test_add(self):
        pwm.scheduler.add(lambda: None, 1)
        self.assertEqual(len(pwm.scheduler.queue), 1)

    def test_remove(self):
        func = lambda: None
        pwm.scheduler.add(func, 1)
        pwm.scheduler.remove(func)
        self.assertEqual(len(pwm.scheduler.queue), 0)

    def test_process_next(self):
        counter = 0

        def func():
            nonlocal counter
            counter += 1

        pwm.scheduler.add(func, 0)
        pwm.scheduler.process_next()
        self.assertEqual(counter, 1)

    def test_process_next_add(self):
        func = lambda: None
        pwm.scheduler.add(func, 0)
        pwm.scheduler.process_next()
        self.assertEqual(pwm.scheduler.queue[0].func, func)
