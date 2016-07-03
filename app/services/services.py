import json

from app.handlers.routes import RoutesHandler
from app.handlers.stops import StopsHandler
from app.parsers.routeparser import RouteParser, RouteMessage
from app.parsers.scheduleparser import ScheduleParser, ScheduleMessage


class StopService:
    def __init__(self):
        self.stop_handler = StopsHandler()

    def get_messages_by_stop_number(self, stop_number):
        resp = self.stop_handler.get_schedule(stop_number, None, None, None, None)
        jobj = json.loads(resp)
        parser = ScheduleParser(jobj)
        sorted_buses = parser.sorted_buses
        messages = []
        for bus in sorted_buses[:5]:
            messages.append(ScheduleMessage(bus_name=bus['info']['route_name'],
                                            bus_number=bus['info']['route_number'],
                                            estimated_arrival_time_string=bus['times']['arrival']['estimated'],
                                            query_time=parser.query_time))
        return messages

    def get_stop_name(self, stop_number):
        resp = self.stop_handler.get_schedule(stop_number, None, None, None, None)
        if resp == 'Stop Schedule Not Found':
            return None
        json_object = json.loads(resp)
        stop_name = json_object['stop-schedule']['stop']['name']
        return stop_name


class RouteService:
    def __init__(self):
        self.routes_handler = RoutesHandler()

    def get_route_messages_by_stop_number(self, stop_number):
        resp = self.routes_handler.get_routs_by_stop_number(stop_number)
        parser = RouteParser(json.loads(resp))
        routes_list = parser.routes_list
        messages = []
        for route in routes_list:
            messages.append(RouteMessage(route_number=route['number'],
                                         route_name=route['name'],
                                         route_coverage=route['coverage']))
        return messages
