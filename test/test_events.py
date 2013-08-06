# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest

import pwm.events


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
