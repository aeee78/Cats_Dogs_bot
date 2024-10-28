import os
import requests
from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


bot = TeleBot(token=BOT_TOKEN)
CAT_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_URL = 'https://api.thedogapi.com/v1/images/search'


def get_cat_image():
    response = requests.get(CAT_URL).json()
    return response[0].get('url')


def get_dog_image():
    response = requests.get(DOG_URL).json()
    return response[0].get('url')


@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_cat_image())


@bot.message_handler(commands=['newdog'])
def new_dog(message):
    chat = message.chat
    bot.send_photo(chat.id, get_dog_image())


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_newcat = types.KeyboardButton('/newcat')
    button_newdog = types.KeyboardButton('/newdog')
    button_start = types.KeyboardButton('/start')

    keyboard.add(button_newcat, button_newdog, button_start)

    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Посмотри, кого я тебе нашёл',
        reply_markup=keyboard,
    )

    bot.send_photo(chat.id, get_cat_image())


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я CatsDogsBot!')


bot.polling()
