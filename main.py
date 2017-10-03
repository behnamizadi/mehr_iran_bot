from telegram.ext import Updater, CommandHandler

def start(bot, update):
    update.message.reply_text('Hello World!')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))
    print "new update\n\r"

f = open(".token", "r") #opens file with name of "test.txt"
token=f.read()
print token
updater = Updater(token.rstrip("\n\r"))
f.close()

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
