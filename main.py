# -*- coding: utf-8 -*-
import logging
import telegram
import time
from telegram import (KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
	ConversationHandler,CallbackQueryHandler,InlineQueryHandler,ChosenInlineResultHandler)
import gettext
import os
from handlers import Handlers

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('messages', localedir, fallback=True)
_ = translate.gettext


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level='INFO')
logger = logging.getLogger(__name__)

KEYBOARD_MAIN = InlineKeyboardMarkup([
    [InlineKeyboardButton(_("start"),callback_data="start"),InlineKeyboardButton(_("aboutus"),callback_data="about_us")],
		], resize_keyboard = True)

def callbackHandler(bot, update):
	global handlers
	getattr(Handlers,update.callback_query.data)(bot,update)



STATE=0
		



def main():
	logger.info("starting ... ")
	#read telegram api token from file
	f = open(".token", "r") 
	token=f.read()
	f.close()
	updater = Updater(token.rstrip("\n\r"))
	updater.dispatcher.add_handler(CallbackQueryHandler(callbackHandler))
	updater.dispatcher.add_handler(CommandHandler('start',Handlers.start))
	updater.dispatcher.add_handler(MessageHandler(Filters.text, Handlers.echo))

	if(updater):
		logger.info("token read scuccesfull!")
    # log all errors
	updater.dispatcher.add_error_handler(Handlers.error)

    # Start the Bot
	updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
