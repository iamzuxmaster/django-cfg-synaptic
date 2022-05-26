import requests
from json import load

def strings(user_language):
    with open('titles/strings.json', 'r', encoding='UTF-8') as file:
        data = load(file)
    return data[user_language]

def select_language():
    # Please note Unused language
    text = "🇺🇿 Iltimos tilni tanlang...\n"
    text += "🇷🇺 Пожалуйста выберите язык...\n"
    text += "🇺🇸 Please select a language...\n"
    # ? Ex: text += "🇹🇷 Lütfen bir dil seçin" 
    return text

class Errors: 
    """
    Error messages is here
    """
    pass