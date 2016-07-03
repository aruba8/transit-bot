import logging

from mako.template import Template
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardHide
from telegram.ext import Updater
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import Filters, MessageHandler

from app.handlers.helper import validate_stop_number
from app.services.services import StopService, RouteService
from config import bot_token

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def help_func(bot, update):
    message_tmpl = Template(filename='app/templates/help.txt')
    bot.sendMessage(update.message.chat_id, text=message_tmpl.render())


def start_command(bot, update):
    message_tmpl = Template(filename='app/templates/start.txt')
    bot.sendMessage(update.message.chat_id, text=message_tmpl.render())


def schedule(bot, update, args):
    schedule_command(bot, update, args)


def schedule_command(bot, update, args):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    if len(args) == 0 or not validate_stop_number(args[0]):
        help_func(bot, update)
        return
    chat_id = update.message.chat_id
    stop_number = int(args[0])
    stop_service = StopService()
    message_tmpl = Template(filename='app/templates/schedule.txt')
    text = message_tmpl.render(messages=stop_service.get_messages_by_stop_number(stop_number))
    bot.sendMessage(chat_id, text=text)


def routes(bot, update, args):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    if len(args) == 0 or not validate_stop_number(args[0]):
        help_func(bot, update)
        return
    chat_id = update.message.chat_id
    stop_number = int(args[0])
    stop_service = RouteService()
    messages = stop_service.get_route_messages_by_stop_number(stop_number)
    message_tmpl = Template(filename='app/templates/route.txt')
    text = message_tmpl.render(messages=messages)
    bot.sendMessage(chat_id, text=text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def echo(bot, update):
    stop_number = update.message.text
    if validate_stop_number(stop_number):
        stop_service = StopService()
        stop_name = stop_service.get_stop_name(stop_number)
        if stop_name is None:
            bot.sendMessage(chat_id=update.message.chat_id, text='Stop #' + stop_number + ' not found')
            return
        custom_keyboard = [[InlineKeyboardButton(text='info', callback_data='info|' + stop_number),
                            InlineKeyboardButton(text='schedule', callback_data='schedule|' + stop_number)]]
        reply_markup = InlineKeyboardMarkup(inline_keyboard=custom_keyboard)
        bot.sendMessage(chat_id=update.message.chat_id, text='Stop #' + stop_number + ' @ ' + stop_name,
                        reply_markup=reply_markup)
    else:
        reply_markup = ReplyKeyboardHide()
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.",
                        reply_markup=reply_markup)


def answer_query(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot.sendChatAction(chat_id=chat_id, action=ChatAction.TYPING)
    parts = dict(enumerate(query.data.split('|', 1)))
    answer_type = parts[0]
    stop_number = parts.get(1)
    stop_service = StopService()
    route_service = RouteService()
    if answer_type == 'info':
        messages = route_service.get_route_messages_by_stop_number(stop_number)
        if len(messages) == 0:
            bot.sendMessage(chat_id=chat_id, text='No info for today')
            return
        message_tmpl = Template(filename='app/templates/route.txt')
        text = message_tmpl.render(messages=messages)
        bot.sendMessage(chat_id=chat_id, text=text)
    if answer_type == 'schedule':
        messages = stop_service.get_messages_by_stop_number(stop_number)
        if len(messages) == 0:
            bot.sendMessage(chat_id=chat_id, text='No schedule for today')
            return
        message_tmpl = Template(filename='app/templates/schedule.txt')
        text = message_tmpl.render(messages=messages)
        bot.sendMessage(chat_id=chat_id, text=text)


def unknown(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    reply_markup = ReplyKeyboardHide()
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.",
                    reply_markup=reply_markup)


def main():
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    unknown_handler = MessageHandler([Filters.command], unknown)
    echo_handler = MessageHandler([Filters.text], echo)
    help_handler = CommandHandler('help', help_func)
    schedule_handler = CommandHandler("schedule", schedule)
    short_schedule_handler = CommandHandler("s", schedule, pass_args=True)
    routes_handler = CommandHandler("i", routes, pass_args=True)

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(echo_handler)
    dp.add_handler(help_handler)
    dp.add_handler(schedule_handler)
    dp.add_handler(short_schedule_handler)
    dp.add_handler(routes_handler)
    dp.add_handler(unknown_handler)
    dp.add_handler(CallbackQueryHandler(answer_query))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
