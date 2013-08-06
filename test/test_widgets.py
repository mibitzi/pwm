# Copyright (c) 2013 Michael Bitzi
# Licensed under the MIT license http://opensource.org/licenses/MIT

import unittest
import time

import pwm.widgets
import test.util as util


class TestWidgets(unittest.TestCase):
    def setUp(self):
        util.setup()

    def tearDown(self):
        util.tear_down()

    def test_time(self):
        self.assertEqual(pwm.widgets.time("%H-%M", "#ff00ff"),
                         ("#ff00ff", time.strftime("%H-%M")))
