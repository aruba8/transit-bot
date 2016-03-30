import unittest

from app.handlers.helper import validate_stop_number
from app.handlers.stops import StopsHandler


class StopsHandlerTest(unittest.TestCase):
    def setUp(self):
        self.stop_handler = StopsHandler()

    def test_build_url(self):
        self.assertEqual(self.stop_handler._build_schedule_url(123),
                         'http://api.winnipegtransit.com/v2/stops/123/schedule.json')


class HelperTest(unittest.TestCase):
    def test_validate_stop_number(self):
        self.assertTrue(validate_stop_number(10005))
        self.assertFalse(validate_stop_number(111113))
        self.assertFalse(validate_stop_number(1111))
