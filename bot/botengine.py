# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
from telegram import Updater
import logging
from config import bot_token
from handlers.stops import StopsHandler
from handlers.routes import RoutesHandler
import json
from mako.template import Template
from parsers.scheduleparser import ScheduleParser, ScheduleMessage
from handlers.helper import validate_stop_number

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)
job_queue = None


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def help(bot, update):
    message_tmpl = Template(filename='templates/help.txt')
    bot.sendMessage(update.message.chat_id, text=message_tmpl.render())


def schedule(bot, update, args):
    schedule_command(bot, update, args)


def sch(bot, update, args):
    schedule_command(bot, update, args)


def schedule_command(bot, update, args):
    if len(args) == 0 or not validate_stop_number(args[0]):
        help(bot, update)
        return

    chat_id = update.message.chat_id
    stop_number = int(args[0])
    stop = StopsHandler()
    resp = stop.get_schedule_by_stop_number(stop_number, None, None, None, None)
    jobj = json.loads(resp)

    parser = ScheduleParser(jobj)
    message_tmpl = Template(filename='templates/schedule.txt')

    _routes = parser.get_routes()
    buses = parser.get_scheduled_buses(_routes)
    sorted_buses = parser.sort_buses_by_estimated_arrival(buses)
    messages = []
    for bus in sorted_buses[:5]:
        messages.append(ScheduleMessage(bus_name=bus['info']['route_name'],
                                        bus_number=bus['info']['route_number'],
                                        estimated_arrival_time_string=bus['times']['arrival']['estimated']))
    message = message_tmpl.render(messages=messages)
    bot.sendMessage(chat_id, text=message)


def routes(bot, update, args):
    chat_id = update.message.chat_id
    stop_number = int(args[0])
    routes_handler = RoutesHandler()
    resp = routes_handler.get_routs_by_stop_number(stop_number)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    global job_queue

    updater = Updater(bot_token)
    job_queue = updater.job_queue

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("schedule", schedule)
    dp.addTelegramCommandHandler("sch", schedule)
    dp.addTelegramCommandHandler("routes", routes)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
