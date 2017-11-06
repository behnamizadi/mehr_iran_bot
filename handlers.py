# -*- coding: utf-8 -*-
import logging
import telegram
import time
from telegram import (KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
	ConversationHandler,CallbackQueryHandler,InlineQueryHandler,ChosenInlineResultHandler)
import gettext
import os
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level='INFO')
logger = logging.getLogger(__name__)
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('messages', localedir, fallback=True)
_ = translate.gettext

class Handlers:
	@staticmethod
	def textHandler(bot, update):
		if update.message.text==_("start"):
			Handlers.start(bot,update)
		if update.message.text==_("aboutus"):
			Handlers.aboutus(bot,update)
	
	@staticmethod
	def start(bot, update):
		logger.info("function: start")
		keyboard = [[
			InlineKeyboardButton(_("haghighi"), callback_data='haghighi')],
			[InlineKeyboardButton(_("hoghooghi"), callback_data='hoghooghi')]]
		reply_markup = InlineKeyboardMarkup(keyboard,resize_keyboard=True)
		Handlers.typing(bot, update.message.chat_id)
		KEYBOARD_MAIN = ReplyKeyboardMarkup([
			[InlineKeyboardButton(_("start"),callback_data="/start"),InlineKeyboardButton(_("aboutus"),callback_data="about_us")],
			], resize_keyboard = True)
		update.message.reply_text(_("welcome"), reply_markup=KEYBOARD_MAIN)
		update.message.reply_text(_("welcome2"), reply_markup=reply_markup)
	
	def aboutus(bot, update):
		update.message.reply_text(_("aboutus_des"))
	
	@staticmethod
	def haghighi(bot, update):
		STATE=2
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
		
		
	@staticmethod						  
	def hoghooghi(bot, update):
		keyboard = [
			[InlineKeyboardButton(_("etebar_jari"), callback_data='etebar_jari')],
			[InlineKeyboardButton(_("hemayati"), callback_data='hemayati')]
			]
		reply_markup = InlineKeyboardMarkup(keyboard,resize_keyboard=True)
		query = update.callback_query
		chat_id=query.from_user.id
		bot.sendMessage(text=_("hoghooghi_des"),
							  chat_id=query.from_user.id,reply_markup=reply_markup)

	@staticmethod
	def emtiazi(bot,update):
		global STATE
		STATE=5
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("emtiazi_des"),
							  chat_id=query.from_user.id)

		
	@staticmethod
	def peyvand1(bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("peyvand1_des"),
							  chat_id=query.from_user.id)
	
	@staticmethod
	def peyvand2(bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("peyvand2_des"),
							  chat_id=query.from_user.id)
	
	@staticmethod										   
	def tadavom(bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("tadavom_des"),
							  chat_id=query.from_user.id)
	@staticmethod						  
	def angizesh(bot,update):
		query = update.callback_query
		bot.sendMessage(text=_("angizesh_des"),
							  chat_id=query.from_user.id)                                                                            
	@staticmethod							 
	def bavar(bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("bavar_des"),
							  chat_id=query.from_user.id)                                                                            
	@staticmethod													   
	def vasighe(bot,update):
		query = update.callback_query
		chat_id=query.from_user.id
		query = update.callback_query
		bot.sendMessage(text=_("enter_mablagh"),
							  chat_id=query.from_user.id)                                                                            
	@staticmethod							 
	def echo(bot, update):
		update.message.reply_text(update.message.text,parse_mode=telegram.ParseMode.HTML)

	@staticmethod
	def cancel(bot, update):
		user = update.message.from_user
		logger.info("User %s canceled the conversation." % user.first_name)
		update.message.reply_text('Bye! I hope we can talk again some day.',
								  reply_markup=ReplyKeyboardRemove())
		return ConversationHandler.END
	
	@staticmethod
	def typing( bot, chatid):
		bot.send_chat_action(chat_id=chatid, action=telegram.ChatAction.TYPING)
		time.sleep(.1)
	
	@staticmethod
	def error(bot, update, error):
		logger.warn('Update "%s" caused error "%s"' % (update, error))

