# -*- coding: utf-8 -*-
import logging
import telegram
import time
from telegram import (InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
	ConversationHandler,CallbackQueryHandler,InlineQueryHandler,ChosenInlineResultHandler)
import gettext
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('messages', localedir, fallback=True)
_ = translate.gettext


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

START,HAGHIGHI,HAGHIGHI_MABLAGH,PEYVAND1 \
	,PEYVAND2,PEYVAND1_SALANEH,PEYVAND2_SALANEH,HOGHOOGHI,HOGHOOGHI_ETEBAR  \
	,HOGHOOGHI_MOSHAREKAT=range(10)


context=""
def start(bot, update):
	logger.info("function: start")
	keyboard = [[
		InlineKeyboardButton(_("haghighi"), callback_data=str(HAGHIGHI)),
		InlineKeyboardButton(_("hoghooghi"), callback_data=str(HOGHOOGHI))
		]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	time.sleep(1.5)
	update.message.reply_text(_("wellcome"), reply_markup=reply_markup)
	return START

def haghighi(bot, update):
	query = update.callback_query
	logger.info("haghigh")
	bot.send_message(text=_("enter_mablagh"),
                          chat_id=query.from_user.id)
                          
def hoghooghi(bot, update):
	logger.info("haghigh")
	bot.send_message(text=_("enter_mablagh"),
                          chat_id=update.message.chat_id)

def peyvand(bot,update):
	query = update.callback_query
	bot.send_message(text=_("enter_mablagh"),
                          chat_id=update.message.chat_id)
	                         
                          
def echo(bot, update):
	update.message.reply_text(update.message.text,parse_mode=telegram.ParseMode.HTML)


def cancel(bot, update):
	user = update.message.from_user
	logger.info("User %s canceled the conversation." % user.first_name)
	update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	logger.info("starting ... ")
	#read telegram api token from file
	f = open(".token", "r") #opens file with name of "test.txt"
	token=f.read()
	updater = Updater(token.rstrip("\n\r"))
	f.close()
	if(updater):
		logger.info("token read scuccesfull!")

    # Get the dispatcher to register handlers
	dp = updater.dispatcher	

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
	conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            START: [CallbackQueryHandler(haghighi),
				RegexHandler(str(HOGHOOGHI),hoghooghi)
            ],

            HAGHIGHI: [MessageHandler(Filters.text, peyvand)],

			HOGHOOGHI: [MessageHandler(Filters.text,error)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

	dp.add_handler(conv_handler)

    # log all errors
	dp.add_error_handler(error)

    # Start the Bot
	updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
