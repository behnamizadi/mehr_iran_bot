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


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level='INFO')
logger = logging.getLogger(__name__)

START,HAGHIGHI,HAGHIGHI_MABLAGH,PEYVAND1 \
	,PEYVAND2,PEYVAND1_SALANEH,PEYVAND2_SALANEH,HOGHOOGHI,HOGHOOGHI_ETEBAR  \
	,HOGHOOGHI_MOSHAREKAT,EMTIAZI,TADAVOM,ANGIZESH,BAVAR,VASIGHE,CHOOSE_HAGHIGHI =range(16)

KEYBOARD_MAIN = ReplyKeyboardMarkup([
    [KeyboardButton(text=_("/start")),KeyboardButton(text=_("about_us"))],
		], resize_keyboard = True)


def callbackHandler(bot, update):
	st=States()
	getattr(States,update.callback_query.data)(st,bot,update)

def typing(bot, chatid):
	bot.send_chat_action(chat_id=chatid, action=telegram.ChatAction.TYPING)
	time.sleep(.1)

def start(bot, update):
		logger.info("function: start")
		keyboard = [[
			InlineKeyboardButton(_("haghighi"), callback_data='haghighi')],
			[InlineKeyboardButton(_("hoghooghi"), callback_data='hoghooghi')]]
		reply_markup = InlineKeyboardMarkup(keyboard,resize_keyboard=True)
		typing(bot, update.message.chat_id)
		update.message.reply_text(_("wellcome"), reply_markup=reply_markup)
		return START

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))
		
class States:
	def haghighi(self,bot, update):
		logger.info("function: haghighi")
		keyboard = [
			[InlineKeyboardButton(_("emtiazi"), callback_data='emtiazi')],
			[InlineKeyboardButton(_("peyvand1"), callback_data='peyvand1'),
			InlineKeyboardButton(_("peyvand2"), callback_data="peyvand2")],
			[InlineKeyboardButton(_("tadavom"), callback_data="tadavom"),
			InlineKeyboardButton(_("angizesh"), callback_data="angizesh")],
			[InlineKeyboardButton(_("bavar"), callback_data="bavar")],
				[InlineKeyboardButton(_("vasighe"), callback_data="vasighe")]
			]
		reply_markup = InlineKeyboardMarkup(keyboard,resize_keyboard=True)
		query = update.callback_query
		chat_id=query.from_user.id
		bot.sendMessage(chat_id,text=_("choose_plan_haghighi"),reply_markup=reply_markup)
		
							  
	def hoghooghi(self,bot, update):
		query = update.callback_query
		chat_id=query.from_user.id
		bot.sendMessage(text=_("hoghooghi_des"),
							  chat_id=query.from_user.id,reply_markup=KEYBOARD_MAIN)

	def emtiazi(self,bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		#typing(bot, update)
		query = update.callback_query
		bot.sendMessage(text=_("emtiazi_des"),
							  chat_id=query.from_user.id)
	def peyvand1(self,bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("peyvand1_des"),
							  chat_id=query.from_user.id)

	def peyvand2(self,bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("peyvand2_des"),
							  chat_id=query.from_user.id)
											   
	def tadavom(self,bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("tadavom_des"),
							  chat_id=query.from_user.id)
							  
	def angizesh(self,bot,update):
		query = update.callback_query
		bot.sendMessage(text=_("angizesh_des"),
							  chat_id=query.from_user.id)                                                                            
								 
	def bavar(self,bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("bavar_des"),
							  chat_id=query.from_user.id)                                                                            
														   
	def vasighe(self,bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("enter_mablagh"),
							  chat_id=query.from_user.id)                                                                            
								 
	def echo(self,bot, update):
		update.message.reply_text(update.message.text,parse_mode=telegram.ParseMode.HTML)


	def cancel(self,bot, update):
		user = update.message.from_user
		logger.info("User %s canceled the conversation." % user.first_name)
		update.message.reply_text('Bye! I hope we can talk again some day.',
								  reply_markup=ReplyKeyboardRemove())
		return ConversationHandler.END



def main():
	logger.info("starting ... ")
	#read telegram api token from file
	f = open(".token", "r") #opens file with name of "test.txt"
	token=f.read()
	f.close()
	updater = Updater(token.rstrip("\n\r"))
	updater.dispatcher.add_handler(CallbackQueryHandler(callbackHandler))
	updater.dispatcher.add_handler(CommandHandler('start',start))
	if(updater):
		logger.info("token read scuccesfull!")

    	
    # log all errors
	updater.dispatcher.add_error_handler(error)

    # Start the Bot
	updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
