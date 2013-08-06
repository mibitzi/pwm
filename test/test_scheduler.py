# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest

import pwm.scheduler


class TestState(unittest.TestCase):
    def setUp(self):
        pwm.scheduler.setup()

    def tearDown(self):
        pwm.scheduler.destroy()

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
