import logging
import telegram
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import signal
import sys

telegram_token = '5619442925:AAHbs0qPTffYZHZglbsEtBybJA-QG5BV4hg'
bot = telegram.Bot(token=telegram_token)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    user_id = update.message.chat_id
    user_data = context.user_data.get(user_id, {})
    if user_data.get("wallet_address"):
        context.bot.send_message(chat_id=user_id, text="You have already submitted your wallet address. You cannot use this bot anymore until the admin decides otherwise.")
    else:
        user_data["wallet_address"] = None
        context.user_data[user_id] = user_data
        context.bot.send_message(chat_id=user_id, text="Hello, to participate in Robin's AIRDROP, please follow the following steps:\n\n1. Follow our Telegram channel: https://t.me/RobinTokenRBN\n2. Follow Robin's Twitter profile:https://twitter.com/RobinToken__\n3. Submit your cryptocurrency wallet address in this format: /wallet wallet_address")

def wallet(update, context):
    user_id = update.message.chat_id
    user_data = context.user_data.get(user_id, {})
    if user_data.get("wallet_address"):
        context.bot.send_message(chat_id=user_id, text="You have already submitted your wallet address.")
    else:
        wallet_address = update.message.text.replace("/wallet ", "")
        user_data["wallet_address"] = wallet_address
        context.user_data[user_id] = user_data
        group_id = "@testbotairdroprobin"  # ID del gruppo
        message = f"The user {update.message.from_user.username} sent the following wallet address: {wallet_address}"
        try:
            bot.send_message(chat_id=group_id, text=message)
            bot.send_message(chat_id=user_id, text="Thank you for participating in Robin's AIRDROP! You will receive your token soon.")
        except telegram.error.TelegramError as e:
            logging.error(f"Error sending message: {e}")
            context.bot.send_message(chat_id=user_id, text="An error occurred while sending the message. Try later.")



def text_message(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Please use the /start and /wallet commands to participate in Robin's AIRDROP.")

def main():
    updater = Updater(telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("wallet", wallet))
    dispatcher.add_handler(MessageHandler(Filters.text, text_message))
    updater.start_polling()
    updater.idle()

def stop_bot(signal, frame):
    print('Bot stopped')
    updater.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, stop_bot)

if __name__ == '__main__':
    main()

