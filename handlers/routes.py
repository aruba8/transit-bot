from .basehandler import BaseHandler
import requests
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


class RoutesHandler(BaseHandler):
    resource = 'routes.json'

    def get_routs_by_stop_number(self, stop_number):
        params = self._build_params(**{'stop': stop_number})
        r = requests.get(self.api_url + self.resource, params=params)
        return r.text

    def _build_url(self):
        return self.api_url + self.resource

    def _build_params(self, **kwargs):
        params = self.init_params
        for key, value in kwargs.items():
            params[key] = value
        return params
