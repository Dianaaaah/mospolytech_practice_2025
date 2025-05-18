import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from deep_translator import GoogleTranslator

BOT_TOKEN = '.'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.chat.id, "👋 Привет! Я твой бот-помощник!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == '👋 Поздороваться':
        remove_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите предложение", reply_markup=remove_markup)    
    else:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("🇬🇧Перевести на английский", callback_data=f'en|{message.text}'),
                  InlineKeyboardButton("🇷🇺Перевести на русский", callback_data=f'ru|{message.text}'),
                  InlineKeyboardButton("🇨🇳Перевести на китайский", callback_data=f'zh-CN|{message.text}'),
                  InlineKeyboardButton("🇩🇪Перевести на немецкий", callback_data=f'de|{message.text}'))
        bot.send_message(message.chat.id, "Выберите язык для перевода:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    target_language, original_text = call.data.split('|')
    translated = GoogleTranslator(source='auto', target=target_language).translate(original_text)
    bot.send_message(call.message.chat.id, f"Перевод: {translated}")
