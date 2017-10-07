# -*- coding: utf-8 -*-
import logging
import telegram
from telegram import (InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
ConversationHandler,CallbackQueryHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
context=""
def start(bot, update):
	keyboard = [[InlineKeyboardButton("💹تسهیلات با معدل حساب", callback_data='1'),
    InlineKeyboardButton("❤طرح پیوند مهر", callback_data='2')],
	[InlineKeyboardButton("💰طرح وثیقه نقدی", callback_data='3')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(
"""به ربات راهنمای تسهیلات بانک قرض الحسنه مهر ایران خوش آمدید.
🌹🌹🌹🌹🌹
\n⚠این ربات هیچ گونه مسولیتی در قبال محاسبات انجام شده ندارد.⚠
\n⚠ربات در مرحله برنامه نویسی می باشد و اطلاعات آن قابل استناد نیست⚠
""", reply_markup=reply_markup)

def button(bot, update):
	global context
	query = update.callback_query
	if query.data == '1':
		context='1'
		keyboard=[[
			InlineKeyboardButton('peyvand1',callback_data='11'),
			InlineKeyboardButton('peyvand2',callback_data='12'),
			InlineKeyboardButton('peyvand3',callback_data='13')
		
		]]
		reply_markup = InlineKeyboardMarkup(keyboard)
		bot.send_message(text="context: %s" % context,
                          chat_id=query.message.chat_id,reply_markup=reply_markup)
                          
def echo(bot, update):
	update.message.reply_text(update.message.text)

f = open(".token", "r") #opens file with name of "test.txt"
token=f.read()
print token
updater = Updater(token.rstrip("\n\r"))
f.close()
updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.start_polling()
updater.idle()
