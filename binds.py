import pyautogui, keyboard, os

from aiogram import types, Bot
from asyncio import sleep
from webbrowser import open as webopen

from machine import WindowsMachine

class bindAPI:
    def __init__(self, bot: Bot, user: types.User) -> None:
        self.bot = bot
        self.user = user
        self.device = WindowsMachine(self.bot)

    def upload_file(self, file: str, filename: str | None = None):
        return types.FSInputFile(file, filename)

    async def setWait(self, duration: int):
        try: await sleep(duration)
        except Exception as e: return await self.bot.send_message(self.user.id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция setWait, длительность задержки = {duration}*\n{e}", parse_mode='Markdown')

    async def setCursor(self, x: int, y: int):
        try: pyautogui.moveTo(int(x), int(y))
        except Exception as e: return await self.bot.send_message(self.user.id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция setCursor, x = {x}, y = {y}*\n{e}", parse_mode='Markdown')

    async def writeKeyboard(self, text: str):
        try: keyboard.write(text, 0)
        except Exception as e: return await self.bot.send_message(self.user.id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция writeKeyboard, текст = {text}*\n{e}", parse_mode='Markdown')

    async def useKeyboard(self, combination: str):
        try: keyboard.send(combination)
        except Exception as e: return await self.bot.send_message(self.user.id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция useKeyboard, комбинация = {combination}*\n{e}", parse_mode='Markdown')

    async def openSite(self, url: str):
        try: webopen(url)
        except Exception as e: return await self.bot.send_message(self.user.id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция openSite, сайт = {url}*\n{e}", parse_mode='Markdown')

    async def sendMessage(self, sendId: int, text: str):
        try: await self.bot.send_message(sendId, text)
        except Exception as e: return await self.bot.send_message(self.user.id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция sendMessage, sendId = {sendId}, текст - {text}*\n{e}", parse_mode='Markdown')

    async def clickMouse(self, button: str):
        try:
            if button == 'r': pyautogui.click(button='right')
            elif button == 'l': pyautogui.click()
            else: return await self.bot.send_message(self.user.id, f"⚠️ Произошла ошибка при выполнении бинда: неизвестная кнопка! Доступные варианты - r или l\n*Функция clickMouse, button = {button}*\n{e}", parse_mode='Markdown')

        except Exception as e: return await self.bot.send_message(self.user.id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция clickMouse, button = {button}*\n{e}", parse_mode='Markdown')

    async def sendScreenshot(self, sendId: int):
        try:
            screenshots = await self.device.screenshot()
            upload_files = [types.InputMediaPhoto(media=self.upload_file(file)) for file in screenshots]
            await self.bot.send_media_group(sendId, upload_files)
            for screen in screenshots:
                os.remove(screen)
        
        except Exception as e: return await self.bot.send_message(self.user.id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция sendScreenshot, sendId = {sendId}*\n{e}", parse_mode='Markdown')
    
    async def useConsole(self, sendId: int, cmd: str):
        try:
            output = await self.device.console_cmd(cmd)
            if int(sendId) >= 1: await self.bot.send_message(sendId, output)    
        except Exception as e: return await self.bot.send_message(self.user.id, f"⚠️ Произошла ошибка при выполнении бинда! *Функция useConsole, команда = {cmd}, sendId = {sendId}*\n{e}", parse_mode='Markdown')
