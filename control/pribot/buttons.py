from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import json

def strings(user_language):
    with open('titles/buttons.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)

    return data[user_language]

def style():
    with open('titles/style.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
    return data

def back(user_language):
    text = strings(user_language=user_language)["back"]
    key = KeyboardButton(text=text)
    return key

def back_inline(user_language, callback_data):
    text = strings(user_language=user_language)["back"]
    key = InlineKeyboardButton(text=text, callback_data=callback_data)
    return key


def select_language():
    langs = [
        {
            "title": "🇺🇿 O'zbek",
            "code": "uz"
        },
        {
            "title": "🇷🇺 Русские",
            "code": "ru"
        },
        {
            "title": "🇺🇸 English",
            "code": "en"
        }
    ]
    keys = [
        [InlineKeyboardButton(text=i["title"], callback_data=i["code"])]
        for i in langs
    ]

    return InlineKeyboardMarkup(inline_keyboard=keys)