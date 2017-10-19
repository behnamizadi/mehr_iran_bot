# -*- coding: utf-8 -*-
import logging
import telegram
import time
from telegram import (KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup, ReplyKeyboardRemove)
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
	,HOGHOOGHI_MOSHAREKAT,EMTIAZI,TADAVOM,ANGIZESH,BAVAR,VASIGHE,CHOOSE_HAGHIGHI \
	=range(16)

KEYBOARD_MAIN = ReplyKeyboardMarkup([
    [KeyboardButton(text=_("/start")),KeyboardButton(text=_("about_us"))],
		], resize_keyboard = True)

def typing(bot, chatid):
	bot.send_chat_action(chat_id=chatid, action=telegram.ChatAction.TYPING)
	time.sleep(1.5)
	return

def start(bot, update):
	logger.info("function: start")
	keyboard = [[
		InlineKeyboardButton(_("haghighi"), callback_data=str(HAGHIGHI))],
		[InlineKeyboardButton(_("hoghooghi"), callback_data=str(HOGHOOGHI))]]
	reply_markup = InlineKeyboardMarkup(keyboard,resize_keyboard=True)
	typing(bot, update.message.chat_id)
	update.message.reply_text(_("wellcome"), reply_markup=reply_markup)
	return START
	
def choose_shakhsiat(bot, update):
	query=update.callback_query
	choose=query.data
	if choose==str(HAGHIGHI):
		haghighi(bot,update)
	if choose==str(HOGHOOGHI):
		hoghooghi(bot,update)
	

def haghighi(bot, update):
	logger.info("function: start")
	keyboard = [
		[InlineKeyboardButton(_("emtiazi"), callback_data=str(EMTIAZI))],
		[InlineKeyboardButton(_("peyvand1"), callback_data=str(PEYVAND1)),
		InlineKeyboardButton(_("peyvand2"), callback_data=str(PEYVAND2))],
		[InlineKeyboardButton(_("tadavom"), callback_data=str(TADAVOM)),
		InlineKeyboardButton(_("angizesh"), callback_data=str(ANGIZESH))],
		[InlineKeyboardButton(_("bavar"), callback_data=str(BAVAR))],
		[InlineKeyboardButton(_("vasighe"), callback_data=str(VASIGHE))]
		]
	reply_markup = InlineKeyboardMarkup(keyboard,resize_keyboard=True)
	query = update.callback_query
	chat_id=query.from_user.id
	typing(bot, chat_id)
	bot.send_message(text=_("choose_plan"),chat_id=chat_id,reply_markup=reply_markup)
	return CHOOSE_HAGHIGHI
                          
def hoghooghi(bot, update):
	query = update.callback_query
	chat_id=query.from_user.id
	typing(bot, chat_id)
	logger.info("hoghooghi	")
	bot.send_message(text=_("enter_mablagh"),
                          chat_id=query.from_user.id,reply_markup=KEYBOARD_MAIN)

def peyvand(bot,update):
	typing(bot, update)
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
            START: [CallbackQueryHandler(choose_shakhsiat)
            ],

            HAGHIGHI: [MessageHandler(Filters.text, peyvand)],

			HOGHOOGHI: [MessageHandler(Filters.text,error)],
        },

        fallbacks=[CommandHandler('cancel', cancel),
					CommandHandler('start',start)
					
					]
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
