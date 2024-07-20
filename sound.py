import keyboard

class Sound:
    __current_volume = None

    @staticmethod
    def current_volume():
        if Sound.__current_volume is None: return 0
        else: return Sound.__current_volume

    @staticmethod
    async def __set_current_volume(volume):
        if volume > 100: Sound.__current_volume = 100
        elif volume < 0: Sound.__current_volume = 0
        else: Sound.__current_volume = volume

    @staticmethod
    async def __track():
        if Sound.__current_volume == None:
            Sound.__current_volume = 0
            for i in range(0, 50):
                Sound.volume_up()

    @staticmethod
    async def volume_up():
        await Sound.__track()
        await Sound.__set_current_volume(Sound.current_volume() + 2)
        keyboard.send('volume up')

    @staticmethod
    async def volume_down():
        await Sound.__track()
        await Sound.__set_current_volume(Sound.current_volume() - 2)
        keyboard.send('volume down')

    @staticmethod
    async def volume_set(amount):
        await Sound.__track()

        if Sound.current_volume() > amount:
            for i in range(0, int((Sound.current_volume() - amount) / 2)):
                await Sound.volume_down()
        
        else:
            for i in range(0, int((amount - Sound.current_volume()) / 2)):
                await Sound.volume_up()
