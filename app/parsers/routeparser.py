import datetime


class RouteParser:
    """ RouteParser to parse json """

    def __init__(self, src_json):
        if src_json == None or src_json == '':
            raise RouteParserException('src_json is None or empty')
        if type(src_json) is not dict:
            raise RouteParserException('src_json is not a valid json')

        self.src_json = src_json
        self._query_time_string = self.src_json['query-time']
        self.query_time = datetime.datetime.strptime(self._query_time_string, '%Y-%m-%dT%H:%M:%S')
        self.routes_list = self.get_routes()

    def get_routes(self):
        return self.src_json['routes']


class RouteMessage:
    def __init__(self, route_number, route_name, route_coverage):
        self.route_number = route_number
        self.route_name = route_name
        self.route_coverage = route_coverage


class RouteParserException(Exception):
    def __init__(self, args):
        Exception.__init__(self, args)
