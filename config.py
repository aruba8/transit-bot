import os
from configparser import ConfigParser

env = os.getenv('BOT_ENVIRON')

api_url = 'http://api.winnipegtransit.com/v2/'
api_key = 'test-api-key'
bot_token = 'test-bot-token'

if env != 'test':
    config_parser = ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), 'api.ini')

    config_parser.read(config_file)

    api_key = config_parser.get("secret", "api-key")
    bot_token = config_parser.get("secret", "bot-token")

bot_api_url = 'https://api.telegram.org/bot' + bot_token + '/'
