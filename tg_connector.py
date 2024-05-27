import telebot
from telebot import types 
import time
import os
from dotenv import load_dotenv
load_dotenv()

class TG_CONNECTOR():
    def __init__(self) -> None:
        self.bot = telebot.TeleBot(os.getenv("TG_TOKEN", ""))
        self.menu_markup = self.create_menu()
        self.last_message = None
  
    def create_menu(self):
        menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton("START")
        button2 = types.KeyboardButton("GO")
        button3 = types.KeyboardButton("STOP")
        button4 = types.KeyboardButton("SEARCH_COINS")
        button5 = types.KeyboardButton("SETTINGS")    
        menu_markup.add(button1, button2, button3, button4, button5)        
        return menu_markup

    def connector_func(self, message, response_message):
        retry_number = 3
        decimal = 1.1       
        for i in range(retry_number):
            try:
                self.bot.send_message(message.chat.id, response_message)                
                return message.text
            except Exception as ex:
                print(ex)
                time.sleep(1.1 + i*decimal)                   
        return None