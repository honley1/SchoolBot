from aiogram import Bot, Dispatcher
from config import token
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(token)
dp = Dispatcher(bot, storage=storage)
