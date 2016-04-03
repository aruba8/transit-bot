import datetime
import json
from unittest import TestCase

from app.parsers.scheduleparser import ScheduleParser, ScheduleParserException


class ScheduleParserTest(TestCase):
    def setUp(self):
        with open('tests/testdata/schedule.json') as json_src:
            self.schedule_json = json.load(json_src)
        self.schedule_parser = ScheduleParser(self.schedule_json)

        with open('tests/testdata/schedule2.json') as json_src:
            self.schedule_json2 = json.load(json_src)

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

    def test_sorted_buses(self):
        parser = ScheduleParser(self.schedule_json2)
        sorted_buses = parser.sorted_buses
        for i in range(len(sorted_buses)):
            if i < len(sorted_buses) - 1:
                bus1 = sorted_buses[i]
                bus2 = sorted_buses[i + 1]
                bus1_arr_time = datetime.datetime.strptime(bus1['times']['arrival']['estimated'], '%Y-%m-%dT%H:%M:%S')
                bus2_arr_time = datetime.datetime.strptime(bus2['times']['arrival']['estimated'], '%Y-%m-%dT%H:%M:%S')
                self.assertTrue(bus1_arr_time < bus2_arr_time)


from app.parsers.scheduleparser import ScheduleMessage


class ScheduleMessageTest(TestCase):
    def setUp(self):
        self.now = datetime.datetime.strptime('2016-03-26T16:22:18', '%Y-%m-%dT%H:%M:%S')
        self.message = ScheduleMessage(123, 'Test bus name', '2016-03-26T17:57:18', self.now)

    def test_get_formatted_arrival_time(self):
        self.assertEqual(self.message.bus_name, 'Test bus name')
        self.assertEqual(self.message.bus_number, 123)
        self.assertEqual(self.message.get_time_before_arrive(), 95)
        self.assertEqual(self.message.get_formatted_arrival_time(), '05:57 PM')


from  app.parsers.routeparser import RouteParser


class RouteParserTest(TestCase):
    def setUp(self):
        with open('tests/testdata/routes.json') as json_src:
            self.route_json = json.load(json_src)
        self.route_parser = RouteParser(self.route_json)

    def test_routes(self):
        routes = self.route_parser.get_routes()
        self.assertEqual(len(routes), 4)

    def test_query_time(self):
        self.assertEqual(self.route_parser.query_time, datetime.datetime(2016, 4, 3, 13, 31, 35))
