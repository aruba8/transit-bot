from unittest import TestCase
from parsers.scheduleparser import ScheduleParser, ScheduleParserException
import json


class ScheduleParserTest(TestCase):
    def setUp(self):
        with open('tests/testdata/schedule.json') as json_src:
            self.schedule_json = json.load(json_src)
        self.schedule_parser = ScheduleParser(self.schedule_json)

    def testExceptionNone(self):
        try:
            ScheduleParser(None)
            self.fail()
        except ScheduleParserException:
            self.assertRaises(ScheduleParserException)

    def testExceptionEmpty(self):
        try:
            ScheduleParser('')
            self.fail()
        except ScheduleParserException:
            self.assertRaises(ScheduleParserException)

    def testExceptionNotJson(self):
        try:
            ScheduleParser('RRRR')
            self.fail()
        except ScheduleParserException:
            self.assertRaises(ScheduleParserException)

    def test_get_routes(self):
        routes = self.schedule_parser.get_routes()
        self.assertEqual(len(routes), 1)

    def test_get_scheduled_buses(self):
        routes = self.schedule_parser.get_routes()
        sch_buses = self.schedule_parser.get_scheduled_buses(routes)
        self.assertEqual(len(sch_buses), 4)
        self.assertEqual(sch_buses[0]['info']['route_number'], 79)
        self.assertEqual(sch_buses[0]['info']['route_name'], 'Route 79 Charleswood')


from parsers.scheduleparser import ScheduleMessage
import datetime

class ScheduleMessageTest(TestCase):
    def setUp(self):
        self.now = datetime.datetime.strptime('2016-03-26T16:22:18', '%Y-%m-%dT%H:%M:%S')
        self.message = ScheduleMessage(123, 'Test bus name', '2016-03-26T17:57:18', self.now)

    def test_get_formatted_arrival_time(self):
        self.assertEqual(self.message.bus_name, 'Test bus name')
        self.assertEqual(self.message.bus_number, 123)
        self.assertEqual(self.message.get_time_before_arrive(), 95)
        self.assertEqual(self.message.get_formatted_arrival_time(), '05:57 PM')



