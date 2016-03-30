from config import api_key, api_url


class BaseHandler:
    api_key = api_key
    api_url = api_url
    init_params = {"api-key": api_key}
