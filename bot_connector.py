from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

with open(file='Besm1Firstbot.sig', mode='r', encoding='cp1251') as f:
    api = f.read()
bot = Bot(token=api)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
