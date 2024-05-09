from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import subprocess
import re
import time

# Define the start command handler
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("GitHub", callback_data='github')],
        [InlineKeyboardButton("Ping", callback_data='ping')],
        [InlineKeyboardButton("Ping URL", callback_data='pingurl')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome! Please choose an option:', reply_markup=reply_markup)

# Define the callback query handler
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'github':
        githubs = ['github.com/larsycoding', 'github.com/larssyy', 'github.com/codelarssyy', 'github.com/larsylab-org']
        query.edit_message_text('\n'.join(githubs))
    elif query.data == 'ping':
        ping_result = subprocess.run(['ping', '-c', '1', 'google.com'], capture_output=True, text=True)
        ping_time = re.search(r'time=([0-9.]+) ms', ping_result.stdout)
        if ping_time:
            query.edit_message_text(f'Ping: {ping_time.group(1)} ms')
        else:
            query.edit_message_text('Failed to get ping.')
    elif query.data == 'pingurl':
        query.edit_message_text('Please enter the URL you want to ping.')

# Define the ping URL command handler
def ping_url(update: Update, context: CallbackContext) -> None:
    url = context.args[0]
    ping_result = subprocess.run(['ping', '-c', '5', url], capture_output=True, text=True)
    ping_times = re.findall(r'time=([0-9.]+) ms', ping_result.stdout)
    if ping_times:
        average_ping = sum(map(float, ping_times)) / len(ping_times)
        update.message.reply_text(f'Average Ping to {url}: {average_ping} ms')
    else:
        update.message.reply_text('Failed to ping the URL.')

# Define the uptime command handler
def uptime(update: Update, context: CallbackContext) -> None:
    uptime_seconds = int(time.time() - context.bot.start_time)
    uptime_string = time.strftime('%H:%M:%S', time.gmtime(uptime_seconds))
    update.message.reply_text(f'Bot Uptime: {uptime_string}')

# Define the main function
def main() -> None:
    updater = Updater("7080171542:AAFC5jcxsl7m-8panGWvP90q5n5Xot5siWg")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("pingurl", ping_url))
    dispatcher.add_handler(CommandHandler("uptime", uptime))

    updater.bot.start_time = time.time()  # Initialize bot start time

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
