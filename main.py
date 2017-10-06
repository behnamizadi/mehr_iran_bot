# -*- coding: utf-8 -*-
import logging
from telegram import (InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
ConversationHandler,CallbackQueryHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def start(bot, update):
	keyboard = [[InlineKeyboardButton("💹تسهیلات با معدل حساب", callback_data='1'),
    InlineKeyboardButton("❤طرح پیوند مهر", callback_data='2')],
	[InlineKeyboardButton("💰طرح وثیقه نقدی", callback_data='3')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(
"""به ربات راهنمای تسهیلات بانک قرض الحسنه مهر ایران خوش آمدید.
\n🌹🌹🌹🌹🌹
\n⚠این ربات هیچ گونه مسولیتی در قبال محاسبات انجام شده ندارد.⚠
\n⚠ربات در مرحله برنامه نویسی می باشد و اطلاعات آن قابل استناد نیست⚠
""", 
	reply_markup=reply_markup)

def button(bot, update):
	query = update.callback_query

	bot.edit_message_text(text="Selected: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
                          
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
