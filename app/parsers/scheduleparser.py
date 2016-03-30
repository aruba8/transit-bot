""" contains parsers for schedule json"""

import datetime


class ScheduleParser:
    """ ScheduleParser parse json returned by transit API"""
    def __init__(self, src_json):
        if src_json is None or src_json == '':
            raise ScheduleParserException('src_json is None or empty')
        if type(src_json) is not dict:
            raise ScheduleParserException('src_json is not a valid json')

        self.src_json = src_json
        self._query_time_string = self.src_json['query-time']
        self.query_time = datetime.datetime.strptime(self._query_time_string, '%Y-%m-%dT%H:%M:%S')
        self.routes_list = self.get_routes()
        self.buses = self.get_scheduled_buses(self.routes_list)
        self.sorted_buses = self.sort_buses_by_estimated_arrival(self.buses)

    def get_routes(self):
        routes_list = self.src_json['stop-schedule']['route-schedules']
        return routes_list

    def get_scheduled_buses(self, routes_list):
        buses = []
        for sch_stop in routes_list:
            stop_buses = sch_stop['scheduled-stops']
            bus_info = self.get_route_info(sch_stop)
            for bus in stop_buses:
                bus['info'] = bus_info
                buses.append(bus)
        return buses

    def sort_buses_by_estimated_arrival(self, buses):
        buses.sort(key=lambda x: x['times']['arrival']['estimated'], reverse=False)
        return buses

    def get_route_info(self, route):
        route_name = route['route']['name']
        route_number = route['route']['number']
        return {'route_name': route_name, 'route_number': route_number}


class ScheduleMessage:
    def __init__(self, bus_number, bus_name, estimated_arrival_time_string, query_time):
        self._query_time = query_time
        self.bus_number = bus_number
        self.bus_name = bus_name
        self.estimated_arrival_time = datetime.datetime.strptime(
            estimated_arrival_time_string, '%Y-%m-%dT%H:%M:%S')

    def get_time_before_arrive(self):
        query_time = self._query_time
        time_diff = self.estimated_arrival_time - query_time
        return round(time_diff.seconds / 60)

    def get_formatted_arrival_time(self):
        return self.estimated_arrival_time.strftime('%I:%M %p')


class ScheduleParserException(Exception):
    def __init__(self, args):
        Exception.__init__(self, args)
