import requests
import logging
from .basehandler import BaseHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


class StopsHandler(BaseHandler):
    pre_resource = 'stops/'
    post_json_resource = '/schedule.json'

    def get_schedule_by_stop_number(self, stop_number, start, end, route, max_results_per_route=2):
        params = self._build_params(
            **{'start': start, 'end': end, 'route': route, 'max-results-per-route': max_results_per_route})
        url = self._build_schedule_url(stop_number)
        rj = requests.get(url, params=params)
        return rj.text

    def _build_schedule_url(self, stop_number):
        return self.api_url + self.pre_resource + str(stop_number) + self.post_json_resource

    def _build_params(self, **kwargs):
        params = self.init_params
        for key, value in kwargs.items():
            if key == 'max_results_per_route':
                params['max-results-per-route'] = value
            else:
                params[key] = value
        return params
