#encoding = 'utf-8'

import telebot
import time
from datetime import datetime
import random


opb_token = 'YOUR TOKEN' #to obtein 'YOUR TOKEN' please proceed to https://romua1d.ru/kak-poluchit-token-bota-telegram-api/
bot = telebot.TeleBot(opb_token)
users = {}
colors = ['red', 'blue', 'pink', 'orange', 'black', 'yellow', 'green', 'violet']


def tracking_result(chat_id, user):
    sum_up = ''
    for period in users[user][2]:
        if len(period) > 2:
            sum_up += "с " + period[0] + ' до ' + period[2] + ':\n' + period[1] + '\n'
    users[user][2].clear()
    bot.send_message(chat_id, sum_up)
        

def tracking(chat_id, user):
    users[user][2].append([datetime.now().strftime("%H:%M:%S")])
    time.sleep(users[user][1])
    if users[user][1] > 0:
        users[user][2][-1].append(datetime.now().strftime("%H:%M"))
        bot.send_message(chat_id, 'what have you done during this period of time? text me "stop" if u want to see a sum-up')  
        tracking(chat_id, user)
    

@bot.message_handler(commands = ['start', 'help', 'day_tracker'])   
def get_text_messages(message):
    user = message.from_user.id
    if user not in users.keys():
        users[user] = ['free', 0, []]     
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Hello! Choose "help" command to get more information')
    elif message.text == '/help':
        bot.send_message(message.chat.id, 'u can begin to track every hour of ur life using our bot bla bla')
    elif message.text == '/day_tracker':
        users[user][0] = 'period'
        keyboard0 = telebot.types.ReplyKeyboardMarkup(True, True, True)
        keyboard0.row('0 10 0', '0 30 0', '1 0 0', '2 0 0')
        bot.send_message(message.chat.id, 'choose how often u want to send notes in the format 1 30 0, where first number goes for hours, second -- for minutes, third -- for seconds', reply_markup = keyboard0)         

        
@bot.message_handler(content_types = ['text'])
def action(message):
    user = message.from_user.id               
    if users[user][0] == 'period':
        try:
            periodlist = list(map(int, message.text.split()))
            period = 3600*periodlist[0] + 60*periodlist[1] + periodlist[2]
            if period == 0:
                bot.reply_to(message, "it doesn't have any sense...")
            else:
                bot.send_message(message.chat.id, 'great')
                users[user][1] = period
                users[user][0] = 'tracking'
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True, True)
                keyboard.row('stop')
                bot.send_message(message.chat.id,  'if u want to stop press stop', reply_markup = keyboard)
                tracking(message.chat.id, user)
        except:
            bot.reply_to(message, 'wrong format, try one more time')
    elif users[user][0] == 'tracking':
        if (message.text.lower() == 'stop' or message.text.lower() == 'стоп'):
            users[user][1] = 0
            users[user][0] = 'free'
            users[user][2][-1].append(datetime.now().strftime("%H:%M"))
            tracking_result(message.chat.id, user)
        else:
            if len(users[user][2][-1]) > 1:
                users[user][2][-1][-1] += '; ' + message.text
            else:
                users[user][2][-1].append(message.text)
        
        
bot.polling(none_stop = True, interval = 0)
